def auto_str(obj) -> str:
    items = []
    for prop, value in obj.__dict__.items():
        item = f"{prop} = {value}"
        if len(item) > 440:
            item = f"{prop} = {value.__class__.__name__}(...)"
        items.append(item)
    return f"{obj.__class__.__name__}({', '.join(items)})"


def auto_dump(obj) -> str:
    items = []
    for prop, value in obj.__dict__.items():
        item = f"{prop} = {auto_dump(value)}"
        items.append(item)
    return f"{obj.__class__.__name__}({', '.join(items)})"
