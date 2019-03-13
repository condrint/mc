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

with open("catcher.txt", encoding="utf8") as f:
    text = f.read()

text = str(text).replace('\n', ' ')
sentences = split_into_sentences(text)




class Model:
    def __init__(self, sentences, stateSize=2, overlap=1):
        self.model = {}
        self.starters = []
        self.stateSize = stateSize
        self.overlap = overlap

        if stateSize - 1 < overlap:
            print('Error overlap too big')
            return
        
        if stateSize < 2 or overlap < 1:
            print('Error overlap or state size too small')
            return

        for sentence in sentences:
            words = sentence.split(' ')

            # remove dialogue
            if "'" in sentence or '"' in sentence or "“" in sentence:
                continue

            self.starters.append(words[0])

            for i in range(len(words) - self.stateSize + 1):
                for j in range(i + 1, i + overlap + 1):
                    key, value = ' '.join(words[i:j]), ' '.join(words[j: i + self.stateSize]) 

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
                keyFound = False
                while not keyFound:
                    newStuff = ''
                    if not prevWord:
                        newSentence = ''
                        break
                    if prevWord in self.model:
                        keyFound = True
                        newStuff = random.choice(self.model[prevWord])
                    else:
                        listOfPrevWord = prevWord.split(' ')[::-1]
                        listOfPrevWord.pop()
                        prevWord = ' '.join(listOfPrevWord[::-1])

                if not newStuff:
                    break

                newSentence += newStuff

                if newSentence and newSentence[-1] in '.?!\'\"':
                    sentenceFormed = True
                    break
                
                newSentence += ' '
                if len(newSentence) < self.overlap:
                    prevWord = newStuff.split(' ')
                else:
                    prevWord = newStuff.split(' ')[-self.overlap]
            
            if sentenceFormed:
                n -= 1
                string += newSentence + ' ' 
        
        return string

model = Model(sentences, 5, 2)
print(model.generateSentences(2))




         
            






