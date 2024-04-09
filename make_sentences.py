import random
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import argparse
import time

def generate_model(text, num_sentences, temperature=0.7, top_k=50, max_length=50):
    """
    Generates num_sentences in English as continuations of the provided text.

    Args:
        text: The text to use as context for generation.
        num_sentences: Number of sentences to generate.
        temperature: Controls randomness (lower for more predictable output).
        top_k: Influences diversity of generated words (higher for more variety).

    Returns:
        A list of generated sentences.
    """
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2", padding_side='left')
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    sentences = []
    generated = model.generate(
        input_ids=tokenizer.encode(text, return_tensors="pt"),
        attention_mask=tokenizer(text, return_tensors="pt").attention_mask,
        do_sample=True,
        temperature=temperature,
        top_k=top_k,
        max_length=max_length,
        num_return_sequences=num_sentences
    )

    for i in range(num_sentences):
        sentence = tokenizer.decode(generated[i], skip_special_tokens=True)
        sentences.append(sentence.strip())
    return sentences

def generate_sentences(name, num, level, seed_iterations=4):
    match level:
        case "a1":
            with open(f"model/{level}.txt", "r") as f:
                data = f.read().split("\n")
            sentences = list()
            for i in range(seed_iterations):
                seed = data[random.randint(1,len(data)-1)]
                sentences += (generate_model(seed, num, temperature=0.8, top_k=20, max_length=20))
            sentences = [clean_sentence(sentence) for sentence in sentences]
            sentences = [item for item in sentences if (len(item) < 70 and '"' not in item)]
        case "b2":
            with open(f"model/{level}.txt", "r") as f:
                data = f.read().split("\n")
            seed = data[random.randint(1,len(data)-1)]
            sentences = generate_model(seed, num)
        case "c1":    
            with open(f"model/{level}.txt", "r") as f:
                data = f.read().split("\n")
            seed = data[random.randint(1,len(data)-1)]
            sentences = generate_model(seed, num)
    random.shuffle(sentences)
    with open(f"export/{name}.txt", "a") as f:
        for sentence in sentences:
            f.write(sentence+"\n")

def clean_sentence(item):
    chars = [". ", "?", "\n", "!"]
    for char in chars:
        item = item.split(char)[0]
    if item.split(" ")[0] in ("Where", "How", "What"):
        return (item + "?")
    else:
        if item[-1] != ".":
            return (item + ".")
        else:
            return item

def main():
    parser = argparse.ArgumentParser(description='Generate sentences in English.')
    parser.add_argument('seed_iterations', type=int, help='How seeds in total you want to use.')
    parser.add_argument('sentences_per_seed', type=int, help='How many sentences per seed should be generated.')
    parser.add_argument('cefr_level', type=str, help='CEFR language level of the sentences.')
    
    args = parser.parse_args()
    name = f"generated_sentences_{args.seed_iterations}_{args.sentences_per_seed}_{args.cefr_level}_{time.strftime('%Y%m%d-%H%M%S')}"


    generate_sentences(name, args.sentences_per_seed, args.cefr_level, seed_iterations=args.seed_iterations)
    print(f"Textfile '{name}.txt' has been created successfully in folder 'export'.")


if __name__ == "__main__":
    main()