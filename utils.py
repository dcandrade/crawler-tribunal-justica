def clear_string(word):
    import re
    blocklist = ["\t", "\n"]
   
    word = word.encode('ascii', errors='ignore').decode('utf-8') # Removing non ascii chars
    word = re.sub('\s+', ' ', word).strip() # Removing multiple spaces
    
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