with open("buffer/raw.txt", "r") as f:
    world = f.readlines()
    result = [item.split(" ")[0] for item in world]
print(result)
result_string = " ".join(result)
print(result_string)

# Write the result strings to a text file
with open("buffer/output.txt", "w") as f:
    for string in result_string:
        f.write(string)  # Write each string followed by a newline