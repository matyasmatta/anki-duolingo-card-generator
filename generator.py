import csv
from googletrans import Translator
import assess_level
import argparse
import time

class SourceFile:
    def __init__(self, source_lang, output_lang, source_location, source_format = "txt"):
        self.location = source_location
        self.format = source_format
        self.source_lang = source_lang
        self.output_lang = output_lang
        self.raw = self.extract_list()
        self.data = self.sentences()

    def extract_list(self):
        with open(self.location, 'r') as txt_file:
            lines = [line.strip() for line in txt_file.readlines()]   
        return lines
    
    def sentences(self):
        result = list()
        for item in self.raw:
            result.append(Sentence(item, self.source_lang, self.output_lang))
        return result

    def export(self):
        name = f"export_{time.strftime('%Y%m%d-%H%M%S')}.csv"
        with open(name, "w", newline='') as f:
            writer = csv.writer(f)
            for item in self.data:
                word_container_1 = ', '.join(f'{word}' for word in item.language_1_wordcontainer)
                word_container_2 = ', '.join(f'{word}' for word in item.language_2_wordcontainer)
                row = (item.language_1, word_container_1, item.language_2, word_container_2)
                writer.writerow(row)
        return name 

class Sentence:
    def __init__(self, raw, source_lang, output_lang):
        self.raw = raw
        self.source_lang = source_lang
        self.output_lang = output_lang
        self.language_1 = self.raw
        self.language_1_words = self.extract_words(self.language_1)
        self.language_2 = self.translate_sentence(self.language_1, self.source_lang, self.output_lang)
        self.language_2_words = self.extract_words(self.language_2)
        self.language_1_wordcontainer = self.generate_wordcontainer(self.language_1, self.source_lang)
        self.language_2_wordcontainer = self.generate_wordcontainer(self.language_2, self.output_lang)
    
    def translate_sentence(self, sentence, source_lang="de", output_lang="en"):
        translator = Translator()
        translation = translator.translate(sentence, src=source_lang, dest=output_lang)
        return translation.text
    
    def generate_wordcontainer(self, data, lang):
        # The Anki cardtype needs a few more words to confuse the player, by default 20% will be overflow words
        overflow_index = round(len(data.split(" "))*0.5)
        return assess_level.get_similar_words(assess_level.assess_sentence(data, lang), overflow_index, lang)
    
    def extract_words(self, data):
        return data.split(" ")

    def normalise(self, data):
        characters_to_replace = ['.', '?', '!', ',']
        self.normalised = data
        
        for char in characters_to_replace:
            self.normalised = self.normalised.replace(char, '')
    
        return self.normalised

def main():
    parser = argparse.ArgumentParser(description='Export language data to CSV file.')
    parser.add_argument('lang1', type=str, help='Language code for column 1 (e.g., "en")')
    parser.add_argument('lang2', type=str, help='Language code for column 2 (e.g., "de")')
    parser.add_argument('filename', type=str, help='Input filename containing language data')

    args = parser.parse_args()

    file = SourceFile(args.lang1, args.lang2, args.filename)
    name = file.export()
    print(f"CSV file '{name}' has been created successfully.")


if __name__ == "__main__":
   main()