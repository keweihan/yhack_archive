import s2t
import sentence
import sys
import experiment

def main():
    # record_len = int(input("Enter the amount of time for the recording"))

    sentence.sentenceDriver("./sentence_input.txt")

    # print("Making combined txt file")
    # f1 = open("./result_final.txt")
    # f2 = open("./short_sentences.txt")
    # l1 = f1.readlines()
    # l2 = f2.readlines()
    #
    # f3 = open("combined_result.txt", "w+")
    # f3.write("Before ")


    experiment.predict("./short_sentences.txt")

if __name__ == '__main__':
    main()
