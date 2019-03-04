##### utility functions from markovify ###########

import re
import random

exceptions = ['c.']

def is_sentence_ender(word):
    if word in exceptions:
        return False
    if word[-1] in [ "?", "!" ]:
        return True
    if len(re.sub(r"[^A-Z]", "", word)) > 1:
        return True
    if word[-1] == ".":
        return True
    return False

def split_into_sentences(text):
    potential_end_pat = re.compile(r"".join([
        r"([\w\.'’&\]\)]+[\.\?!])", # A word that ends with punctuation
        r"([‘’“”'\"\)\]]*)", # Followed by optional quote/parens/etc
        r"(\s+(?![a-z\-–—]))", # Followed by whitespace + non-(lowercase or dash)
        ]), re.U)
    dot_iter = re.finditer(potential_end_pat, text)
    end_indices = [ (x.start() + len(x.group(1)) + len(x.group(2))) 
        for x in dot_iter
        if is_sentence_ender(x.group(1)) ]
    spans = zip([None] + end_indices, end_indices + [None])
    sentences = [text[start:end].strip() for start, end in spans]

    return sentences

##############################################

# read data

with open("data.txt", encoding="utf8") as f:
    text = f.read()

text = str(text).replace('\n', ' ')
sentences = split_into_sentences(text)

class Model:
    def __init__(self, sentences):
        self.model = {}
        self.starters = []

        for sentence in sentences:
            words = sentence.split(' ')
            self.starters.append(words[0])

            for i in range(len(words) - 1):
                word, nextWord = words[i], words[i + 1]

                if word in self.model:
                    self.model[word].append(nextWord)

                else:
                    self.model[word] = [nextWord]
    
    def generateSentences(self, n, maxLength=30):
        """
        generate n sentences and return
        a string containing them
        """

        if n < 1:
            return
        
        string = ''

        while n:
            prevWord = random.choice(self.starters)
            newSentence = prevWord + ' '
            sentenceFormed = False

            for _ in range(maxLength):
                
                newWord = random.choice(self.model[prevWord])
                newSentence += newWord
                print(newSentence)
                if newSentence[-1] in '.?!':
                    sentenceFormed = True
                    break
                
                newSentence += ' '
                prevWord = newWord
            
            if sentenceFormed:
                n -= 1
                string += newSentence + ' ' 
        
        return string

model = Model(sentences)
print(model.generateSentences(2))




         
            






