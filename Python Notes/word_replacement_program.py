def replace_word(word : str, 
                 replacement : str, 
                 sentence : str) -> str:
    return sentence.replace(word, replacement);

if __name__ == "__main__":
    print((res := replace_word(input("Enter the word to replace\n> "), 
                        input("Enter the Replacement\n> "), 
                        input("Enter the string\n> "))), "\n\nThe replaced sentence is:\n> ", res) 
    assert replace_word("j", "l", "Hejjo") == "Hello"
    assert replace_word("lol", "W", "Hello lol this is a massive lol") == "Hello W this is a massive W"
