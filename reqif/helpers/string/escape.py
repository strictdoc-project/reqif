# This code is taken from Python 3.7. The addition is escaping of the tab
# character.
def reqif_escape(string: str) -> str:
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    string = string.replace("&", "&amp;")  # Must be done first!
    string = string.replace("<", "&lt;")
    string = string.replace(">", "&gt;")
    string = string.replace('"', "&quot;")
    string = string.replace("'", "&#x27;")
    # Invisible tab character
    string = string.replace("\t", "&#9;")
    return string


def reqif_escape_title(string: str) -> str:
    # The only known reason for this method is the presence of &amp; in the
    # HEADER title of ReqIF files found at the ci.eclipse.org.
    string = string.replace("&", "&amp;")
    return string
