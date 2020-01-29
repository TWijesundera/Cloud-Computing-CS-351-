# Thisara Wijesundera
# CS-351
# Capitalize every word in a sentence given as user input

if __name__ == "__main__":
    user_input = input("\nGive me a sentence and I'll capitalize it!\n")

    """ Slice and change the first letter to upper case and append the rest """
    sentence = [word[0].upper() + word[1:] for word in user_input.split()]

    print("\n{}".format(" ".join(sentence)))