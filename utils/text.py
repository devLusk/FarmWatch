def strip_timestamp(text):
    if not text:
        return ""

    if "] " in text:
        return text.split("] ", 1)[1]

    return text


def extract_current_honey(description):
    if not description:
        return None

    lines = description.split("\n")
    for line in lines:
        if "Current Honey:" in line:
            return line.split(":", 1)[1].strip()

    return None