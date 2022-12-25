from reqif.helpers.debug import auto_described


def test_01_debug() -> None:
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

    a = A()
    b = B()
    a.prop2 = b
    b.B2 = a

    a_str = str(a)
    a_repr = repr(a)

    assert a_str == (
        "A("
        'prop1 = "FOO", '
        "prop2 = B(...), "
        "prop3 = [3 elements], "
        "prop4 = {1 elements}, "
        "prop5 = b'123')"
    )
    assert a_str == a_repr


def test_02_debug() -> None:
    @auto_described(str_and_repr=True)
    class A:
        def __init__(self):
            self.prop1 = "FOO"
            self.prop2 = None
            self.prop3 = [1, 2, 3]
            self.prop4 = {"a": 123}
            self.prop5 = bytes("123", "utf-8")

    a = A()
    a_str = str(a)
    a_repr = repr(a)
    assert a_str == (
        "A("
        'prop1 = "FOO", '
        "prop2 = NoneType(...), "
        "prop3 = [3 elements], "
        "prop4 = {1 elements}, "
        "prop5 = b'123')"
    )
    assert a_str == a_repr
