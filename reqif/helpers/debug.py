def auto_describe_object(obj) -> str:
    items = []
    for prop, value in obj.__dict__.items():
        item = f"{prop} = {value}"
        items.append(item)
    return f"{obj.__class__.__name__}({', '.join(items)})"
