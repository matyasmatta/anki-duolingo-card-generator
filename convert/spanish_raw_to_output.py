with open("convert/spanish.txt", "r") as f:
    world = f.readlines()
    result = list()
    for item in world[0].split(" "):
        try:
            item = int(item)
            pass
        except:
            result.append(item)
    print(result)
    result_string = " ".join(result)
print(result_string)

# Write the result strings to a text file
with open("convert/output_es.txt", "w") as f:
    for string in result_string:
        f.write(string)  # Write each string followed by a newline