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
    def __init__(self, sentences, stateSize=2):
        self.model = {}
        self.starters = []
        self.stateSize = stateSize

        for sentence in sentences:
            words = sentence.split(' ')

            # remove dialogue
            if "'" in sentence or '"' in sentence or "“" in sentence:
                continue

            self.starters.append(words[0])
            for i in range(len(words) - self.stateSize + 1):
                key, value = words[i], ' '.join(words[i + 1: i + self.stateSize]) 

                if key in self.model:
                    self.model[key].append(value)

                else:
                    self.model[key] = [value]
    
    def generateSentences(self, n, maxLength=5):
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
                newStuff = random.choice(self.model[prevWord])
                newSentence += newStuff

                if newSentence[-1] in '.?!\'\"':
                    sentenceFormed = True
                    break
                
                newSentence += ' '
                prevWord = newStuff.split(' ')[-1]
            
            if sentenceFormed:
                n -= 1
                string += newSentence + ' ' 
        
        return string

model = Model(sentences, 4)
print(model.generateSentences(2))




         
            






