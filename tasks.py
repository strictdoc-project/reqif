import os
import re

import invoke
from invoke import task


def one_line_command(string):
    return re.sub("\\s+", " ", string).strip()


def run_invoke_cmd(context, cmd) -> invoke.runners.Result:
    return context.run(
        cmd, env=None, hide=False, warn=False, pty=False, echo=True
    )


@task
def clean(context):
    find_command = one_line_command(
        """
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
    )

    find_result = run_invoke_cmd(context, find_command)
    find_result_stdout = find_result.stdout.strip()
    echo_command = one_line_command(
        f"""echo {find_result_stdout} | xargs rm -rfv"""
    )

    run_invoke_cmd(context, echo_command)


@task
def test_unit(context):
    run_invoke_cmd(
        context,
        one_line_command(
            """
        coverage run
            --rcfile=.coveragerc
            --branch
            -m pytest
            tests/unit/
        """
        ),
    )
    run_invoke_cmd(
        context,
        one_line_command(
            """
        coverage report --sort=cover
        """
        ),
    )


@task(test_unit)
def test_coverage_report(context):
    run_invoke_cmd(
        context,
        one_line_command(
            """
        coverage html
        """
        ),
    )


@task(clean)
def test_integration(context, focus=None, debug=False):
    cwd = os.getcwd()

    reqif_exec = f'python \\"{cwd}/reqif/cli/main.py\\"'

    focus_or_none = f"--filter {focus}" if focus else ""
    debug_opts = "-vv --show-all" if debug else ""

    command = one_line_command(
        f"""
        lit
        --param REQIF_EXEC="{reqif_exec}"
        -v
        {debug_opts}
        {focus_or_none}
        {cwd}/tests/integration
        """
    )
    run_invoke_cmd(context, command)


@task
def export_pip_requirements(context):
    run_invoke_cmd(
        context,
        one_line_command(
            """
        poetry
            export
                --dev
                --without-hashes
                --format requirements.txt
                > requirements.txt
        """
        ),
    )


# Support generation of Poetry managed setup.py file #761
# https://github.com/python-poetry/poetry/issues/761#issuecomment-689491920
@task
def install_local(context):
    run_invoke_cmd(
        context,
        one_line_command(
            """
                rm -rf dist/ && poetry build
            """
        ),
    )
    run_invoke_cmd(
        context,
        one_line_command(
            """
        tar -xvf dist/*.tar.gz --wildcards --no-anchored '*/setup.py' --strip=1
        """
        ),
    )
    run_invoke_cmd(
        context,
        one_line_command(
            """
        pip install -e .
        """
        ),
    )


@task
def lint_black_diff(context):
    command = one_line_command(
        """
        black . --color 2>&1
        """
    )
    result = run_invoke_cmd(context, command)

    # black always exits with 0, so we handle the output.
    if "reformatted" in result.stdout:
        print("invoke: black found issues")
        result.exited = 1
        raise invoke.exceptions.UnexpectedExit(result)


@task
def lint_pylint(context):
    command = one_line_command(
        """
        pylint
          --rcfile=.pylint.ini
          --disable=c-extension-no-member
          reqif/ tasks.py
        """  # pylint: disable=line-too-long
    )
    try:
        run_invoke_cmd(context, command)
    except invoke.exceptions.UnexpectedExit as exc:
        # pylint doesn't show an error message when exit code != 0, so we do.
        print(f"invoke: pylint exited with error code {exc.result.exited}")
        raise exc


@task
def lint_flake8(context):
    command = one_line_command(
        """
        flake8
            reqif/ tasks.py tests/unit/
            --statistics --max-line-length 80 --show-source
        """
    )
    run_invoke_cmd(context, command)


@task
def lint_mypy(context):
    run_invoke_cmd(
        context,
        one_line_command(
            """
        mypy reqif/
            --show-error-codes
            --disable-error-code=import
            --disable-error-code=no-untyped-call
        """  # --strict
        ),
    )


@task(
    lint_black_diff,
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
def release(context):
    command = one_line_command(
        """
            poetry publish --build
        """
    )
    run_invoke_cmd(context, command)


# https://github.com/github-changelog-generator/github-changelog-generator
# gem install github_changelog_generator
@task
def changelog(context, github_token):
    command = one_line_command(
        f"""
        github_changelog_generator
        --token {github_token}
        --user strictdoc-project
        --project reqif
        """
    )
    run_invoke_cmd(context, command)
