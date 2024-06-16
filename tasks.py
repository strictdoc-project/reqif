import inspect
import os
import re

import invoke
from invoke import task

# FIXME
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec


def one_line_command(string):
    return re.sub("\\s+", " ", string).strip()


def run_invoke_cmd(context, cmd) -> invoke.runners.Result:
    return context.run(
        one_line_command(cmd),
        env=None,
        hide=False,
        warn=False,
        pty=False,
        echo=True,
    )


@task
def clean(context):
    find_command = """
        find
            tests
            -type f \\(
                -name '*.script'
            \\)
            -or -type d \\(
                -name '*.dSYM' -or
                -name 'sandbox' -or
                -name 'Output' -or
                -name 'output'
            \\)
            -not -path "**Expected**"
            -not -path "**Input**"
    """

    find_result = run_invoke_cmd(context, find_command)
    find_result_stdout = find_result.stdout.strip()
    echo_command = f"""echo {find_result_stdout} | xargs rm -rfv"""

    run_invoke_cmd(context, echo_command)


@task(aliases=["tu"])
def test_unit(context):
    run_invoke_cmd(
        context,
        """
        coverage run
            --rcfile=.coveragerc
            --branch
            -m pytest
            tests/unit/
        """,
    )
    run_invoke_cmd(
        context,
        """
        coverage report --sort=cover
        """,
    )


@task(test_unit)
def test_coverage_report(context):
    run_invoke_cmd(
        context,
        """
        coverage html
        """,
    )


@task(clean, aliases=["ti"])
def test_integration(context, focus=None, debug=False):
    cwd = os.getcwd()

    reqif_exec = "python -m reqif.cli.main"

    focus_or_none = f"--filter {focus}" if focus else ""
    debug_opts = "-vv --show-all" if debug else ""

    command = f"""
            lit
            --param REQIF_EXEC="{reqif_exec}"
            -v
            {debug_opts}
            {focus_or_none}
            {cwd}/tests/integration
        """
    run_invoke_cmd(context, command)


@task
def lint_ruff_format(context):
    result: invoke.runners.Result = run_invoke_cmd(
        context,
        """
            ruff
                format
                *.py
                reqif/
                tests/unit
        """,
    )
    # Ruff always exits with 0, so we handle the output.
    if "reformatted" in result.stdout:
        print("invoke: ruff format found issues")  # noqa: T201
        result.exited = 1
        raise invoke.exceptions.UnexpectedExit(result)


@task
def lint_flake8(context):
    command = """
        flake8
            reqif/ tasks.py tests/unit/
            --ignore=E501,W503
            --statistics --max-line-length 80 --show-source
    """
    run_invoke_cmd(context, command)


@task
def lint_ruff_check(context, fix=True):
    argument_fix = "--fix" if fix else ""
    command = f"""
        ruff check . {argument_fix}
    """
    run_invoke_cmd(context, command)


@task(aliases=["lm"])
def lint_mypy(context):
    run_invoke_cmd(
        context,
        """
        mypy reqif/
            --show-error-codes
            --disable-error-code=import
            --disable-error-code=arg-type
            --disable-error-code=no-untyped-call
            --disable-error-code=no-untyped-def
            --disable-error-code=type-arg
            --disable-error-code=union-attr
            --strict
        """,
    )


@task(lint_ruff_format, lint_ruff_check, lint_flake8, lint_mypy, aliases=["l"])
def lint(_):
    pass


@task(test_unit, test_integration, aliases=["t"])
def test(_):
    pass


@task(lint, test, aliases=["c"])
def check(_):
    pass


@task
def release(context, username=None, password=None):
    """
    A release can be made to PyPI or test package index (TestPyPI):
    https://pypi.org/project/strictdoc/
    https://test.pypi.org/project/strictdoc/
    """

    # When a username is provided, we also need password, and then we don't use
    # tokens set up on a local machine.
    assert username is None or password is not None

    repository_argument_or_none = "" if username else ("--repository reqif_release")
    user_password = f"-u{username} -p{password}" if username is not None else ""
    command = f"""
        rm -rfv dist/ &&
        python3 -m build &&
            twine check dist/* &&
            twine upload dist/reqif-*.tar.gz
                {repository_argument_or_none}
                {user_password}
    """
    run_invoke_cmd(context, command)


@task
def release_local(context):
    run_invoke_cmd(
        context,
        """
        rm -rfv dist/ && pip install -e .
        """,
    )


# https://github.com/github-changelog-generator/github-changelog-generator
# gem install github_changelog_generator
@task
def changelog(context, github_token):
    command = f"""
        github_changelog_generator
        --token {github_token}
        --user strictdoc-project
        --project reqif
    """
    run_invoke_cmd(context, command)
