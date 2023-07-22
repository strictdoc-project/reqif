import os
import re

import invoke
from invoke import task


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


@task
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


@task(clean)
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
def lint_black_diff(context):
    command = """
        black . --color 2>&1
    """
    result = run_invoke_cmd(context, command)

    # black always exits with 0, so we handle the output.
    if "reformatted" in result.stdout:
        print("invoke: black found issues")  # noqa: T201
        result.exited = 1
        raise invoke.exceptions.UnexpectedExit(result)


@task
def lint_pylint(context):
    command = """
        pylint
          --rcfile=.pylint.ini
          --disable=c-extension-no-member
          reqif/ tasks.py
    """
    try:
        run_invoke_cmd(context, command)
    except invoke.exceptions.UnexpectedExit as exc:
        # pylint doesn't show an error message when exit code != 0, so we do.
        print(  # noqa: T201
            f"invoke: pylint exited with error code {exc.result.exited}"
        )
        raise exc


@task
def lint_flake8(context):
    command = """
        flake8
            reqif/ tasks.py tests/unit/
            --statistics --max-line-length 80 --show-source
    """
    run_invoke_cmd(context, command)


@task
def lint_ruff(context, fix=False):
    argument_fix = "--fix" if fix else ""
    command = f"""
        ruff . {argument_fix}
    """
    run_invoke_cmd(context, command)


@task
def lint_mypy(context):
    run_invoke_cmd(
        context,
        """
        mypy reqif/
            --show-error-codes
            --disable-error-code=import
            --disable-error-code=no-untyped-call
        """,  # --strict
    )


@task(
    lint_black_diff,
    lint_ruff,
    lint_pylint,
    lint_flake8,
    lint_mypy,
)
def lint(_):
    pass


@task(test_unit, test_integration)
def test(_):
    pass


@task(lint, test)
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

    repository_argument_or_none = (
        "" if username else ("--repository reqif_release")
    )
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
