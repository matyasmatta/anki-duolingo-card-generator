import csv

class SourceFile:
    def __init__(self, source_location, source_format = "txt"):
        self.location = source_location
        self.format = source_format
        self.raw = self.extract_list()
        self.data = self.sentences()

    def extract_list(self):
        with open(self.location, 'r') as txt_file:
            lines = [line.strip() for line in txt_file.readlines()]   
        return lines
    
    def sentences(self):
        result = list()
        for item in self.raw:
            result.append(Sentence(item))
        return result

class Sentence:
    def __init__(self, raw):
        self.raw = raw
        self.words = self.extract_words()
    
    def extract_words(self):
        return self.normalise().split(" ")

    def normalise(self):
        self.normalised = self.raw.replace(".", "")
        self.normalised = self.normalised.replace("?", "")
        self.normalised = self.normalised.replace("!", "")
        self.normalised = self.normalised.replace(",", "")
        return self.normalised

if __name__ == "__main__":
    file = SourceFile("sentences.txt")
    print(file.data)