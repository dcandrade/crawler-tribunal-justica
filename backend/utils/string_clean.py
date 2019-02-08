def clear_string(word, blocklist=['\t', '\n']):
    import re

    word = re.sub('\s+', ' ', word).strip()  # Removing multiple spaces
    word = re.sub(r'\\x[a-fA-F0-9]{2}', '', word)  # Removing unicode chars

    for item in blocklist:
        word = word.replace(item, "")

    return word


def clear_strings(words):
    result = []
    for word in words:
        clean_word = clear_string(word)
        if len(clean_word) > 0:
            result.append(clean_word)

    return result


# Dict key processor for avoiding mongodb conflicts
def process_key(key):
    return clear_string(key, blocklist=[':', '.'])
