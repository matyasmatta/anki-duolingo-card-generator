import statistics
import random

def import_word_list(lang):
    try:
        with open(f"language_packs/{lang}.txt", "r") as f:
            file_contents = f.read()
            return file_contents.split()
    except:
        raise Exception("Unsupported language, no language_pack map found!")

def normalise(data):
    characters_to_replace = ['.', '?', '!', ',']
    normalised = data
    
    for char in characters_to_replace:
        normalised = normalised.replace(char, '')

    return normalised

def assess_word(word, lang):
    try:
        index = import_word_list(lang).index(word)
    except:
        try:
            index = import_word_list(lang).index(normalise(word).lower())
        except:
            return None
    return round(index)

def assess_sentence(sentence, lang):
    indexes = [assess_word(word, lang) for word in normalise(sentence).split(" ")]
    indexes = [value for value in indexes if value is not None]
    try: 
        median = statistics.median(indexes) 
    except: 
        median = random.randint(1000,2000)
    return round(median)

def get_similar_words(index, num, lang):
    return [import_word_list(lang)[index+random.randint(-20,20)] for i in range(num)]

if __name__ == "__main__":
    print(assess_sentence("Die grüne Fuchs ist eine der schönsten."))
    print(get_similar_words(3000, 10, "de"))