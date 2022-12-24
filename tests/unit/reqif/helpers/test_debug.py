from reqif.helpers.debug import auto_described


@auto_described
class A:
    def __init__(self):
        self.prop1 = "FOO"
        self.prop2 = None
        self.prop3 = [1, 2, 3]
        self.prop4 = {"a": 123}
        self.prop5 = bytes("123", "utf-8")


@auto_described
class B:
    def __init__(self):
        self.B1 = "FOO"
        self.B2 = None


def test_01_debug() -> None:
    a = A()
    b = B()
    a.prop2 = b
    b.B2 = a
    assert (str(a)) == (
        "A("
        'prop1 = "FOO", '
        "prop2 = B(...), "
        "prop3 = [3 elements], "
        "prop4 = {1 elements}, "
        "prop5 = b'123')"
    )
