# Usage
``python generator.py {source-language: en} {target-language} {source-file}``

e.g. ``python generator.py en de sentences.txt``

## Currently supported langauges
English (en), German (de), Czech (cs)

> [!NOTE]
> Keep in mind Google Translate is currently used for the translation, therefore it is imperfect, I will update it with more translator options coming soon, for now Google is universal.

## Output
The script generates a CSV in format [Language1, WordContainerLang1, Language2, WordContainerLang2]. You can therefore generate en->de or de->en both ways just flipping the order. 

Generates ``export_{source_lang}_{target_lang}_{time}.csv`` in the export directory.

## Import into Anki
You must have [Note Type: Puzzle Sentences](https://ankiweb.net/shared/info/1522392024) installed to use the Puzzle Sentences+ notetype! (credit Present-Boat-2053)

For importing into Anki press Ctrl+Shift+I on Windows (File->Import) and use order 1-3-2 or 3-1-4:
![alt text](docs/obrazek-1.png)
