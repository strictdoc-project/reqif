# This function could be a separate package but keeping it within the project
# for simplicity.
__version__ = "0.0.1"


# Maybe there is a better way to generate __str__ and __repr__.
# But for now, this solution works good enough:
# https://stackoverflow.com/a/33800620/598057
def auto_described(cls):
    def __str__(self):
        return auto_str(self)

    def __repr__(self):
        return auto_str(self)

    cls.__str__ = __str__
    cls.__repr__ = __repr__
    return cls


def auto_str(obj: object) -> str:
    items = []

    # This is a rather defensive implementation that prevents auto_str from
    # breaking on the objects with recursive references:
    # Example: A -> B -> A.
    for prop, value in obj.__dict__.items():
        if type(value) == list:  # pylint: disable=unidiomatic-typecheck
            if len(value) == 0:
                item = f"{prop} = []"
            else:
                item = f"{prop} = [{len(value)} elements]"
        elif type(value) == dict:  # pylint: disable=unidiomatic-typecheck
            if len(value) == 0:
                item = f"{prop} = {{}}"
            else:
                item = f"{prop} = {{{len(value)} elements}}"
        elif isinstance(value, (list, dict, set)):
            item = f"{prop} = {value.__class__.__name__}({len(value)} elements)"
        elif isinstance(value, str):
            item = f'{prop} = "{value}"'
        elif isinstance(value, bytes):
            item = f"{prop} = {value!r}"
        elif isinstance(value, (int, float, bool)):
            item = f"{prop} = {value}"
        elif isinstance(value, object):
            item = f"{prop} = {value.__class__.__name__}(...)"
        else:
            item = f"{prop} = {value}"

        items.append(item)
    return f"{obj.__class__.__name__}({', '.join(items)})"
