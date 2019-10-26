from google.cloud import language_v1
from google.cloud.language_v1 import enums

import sentence_functions
import re
import string


class WordInfo:
    def __init__(self, lemma_input):
        self.lemma = lemma_input
        self.freq = 1 
        self.invfreq = 0 
        self.total_score = 0.0 #TODO: Formula here from paper 

class SimpleSentence:

    #Calls Google Cloud Syntax API on given "text_content"
    def sample_analyze_syntax(self, text_content):
        
        client = language_v1.LanguageServiceClient()
        type_ = enums.Document.Type.PLAIN_TEXT

        
        #Set Language
        language = "en"
        document = {"content": text_content, "type": type_, "language": language}

        # Available values: NONE, UTF8, UTF16, UTF32
        encoding_type = enums.EncodingType.UTF8

        response = client.analyze_syntax(document, encoding_type=encoding_type)

        return response

    #Initializes SimpleSentence with api syntax output
    def __init__(self, file_path):
        data = open(file_path, "r")
        #data_content = data.read()
        #data.close()
        #print(data_content)
        self.total_words = 0
        self.info = sentence_functions.sample_analyze_syntax(data.read())

        #Dictionary of unique words
        """
        placehold_object = WordInfo("NULL")
        self.lemma_WordInfo = {"NULL": placehold_object}   
        """
        self.lemma_WordInfo = {}
        self.sentence_output = 0.5
        self.return_sentences = [] # the returned sentences

    #Uses info object to add unique words to list
    def add_unique_words(self):
        for token in self.info.tokens:
            newWord = token.lemma

            #if word is already in dictionary, update information
            if newWord in self.lemma_WordInfo: 
                token_info = self.lemma_WordInfo[token.lemma]
                
                #TODO: update 
                token_info.freq += 1
                
            else:
                part_of_speech = token.part_of_speech
                if enums.PartOfSpeech.Tag(part_of_speech.tag).name != 'P': #TODO: Doesn't filter anything?
                    token_info = WordInfo(token.lemma)
                    self.lemma_WordInfo[token.lemma] = token_info

            self.total_words += 1
    
    #Goes through lemma_WordInfo and updates tf score. TODO: Add idf
    def calcScore(self):
        for x in self.lemma_WordInfo:
            #print(float(self.lemma_WordInfo[x].freq)) DEBUG
            #print(float(self.total_words))
            #print(float(self.lemma_WordInfo[x].freq)/float(self.total_words))
            self.lemma_WordInfo[x].total_score = float( float(self.lemma_WordInfo[x].freq ) / float(self.total_words)  )
        
    #TEST FUNCTION ONLY
    def outputDictionary(self):
        for x in self.lemma_WordInfo:
            print(x, end = '')
            print(" : ", end = ''),
            print(self.lemma_WordInfo[x].total_score)
            

        print(self.total_words)
        return 

    #Create new dictionary sentence_tf, where key is sentence and value is sum of tf of words
    def sentenceDictionary(self):
        
        #Initialize dictionary with sentences as keys and tf as 0
        self.sentence_tf = {}   
        for sentence in self.info.sentences:
            sentence_text = sentence.text
            
            #if word is already in dictionary, do nothing
            self.sentence_tf[sentence_text.content] = 0 
        
        #Split sentence key into words and find tf value for each word.
        word_lemma = sentence_functions.generate_word_lemma_dict(self.info)
        for sentence_key in self.sentence_tf:
            wordlist = re.findall(r'\w+', sentence_key)
            #print ("The list of words is : " +  str(wordlist)) DEBUG
            for word_input in wordlist:
                #self.lemma_WordInfo[]    <-don't need this right?
                lemma = word_lemma[word_input] #convert word to it's lemma to find tf
                self.sentence_tf[sentence_key] += self.lemma_WordInfo[lemma].total_score

        return_list = sorted(self.sentence_tf.values(), reverse=True)[:int(len(self.sentence_tf) * self.sentence_output)]
        for x in self.sentence_tf: # using key
            if self.sentence_tf[x] in return_list:
                self.return_sentences.append(x)

        ##TODO: Break up key string and update value based on their priority 

        inv_tf_sentence = {v: k for k, v in self.sentence_tf.items()}

        

    def outputResult(self):
        outF = open("short_sentences.txt", "w")
        for sentence_output in self.return_sentences:
            outF.write(sentence_output)
            outF.write("\n")



if __name__ == '__main__':

    #Create Object
    Simplify = SimpleSentence("sentence_input.txt")
    Simplify.add_unique_words()

    Simplify.calcScore()
    #Simplify.outputDictionary()
    Simplify.sentenceDictionary()

    Simplify.outputResult()


    


