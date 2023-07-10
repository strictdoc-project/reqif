from ... import __version__


class VersionCommand:
    @staticmethod
    def execute():
        print(__version__)  # noqa: T201
