def strip_markdown(text: str):
    text = text.replace('**', '')
    text = text.replace('__', '')
    text = text.replace('*', '')
    return text
