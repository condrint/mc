##### utility functions from markovify ###########



    def test_sentence_output(self, words, max_overlap_ratio, max_overlap_total):
        """
        Given a generated list of words, accept or reject it. This one rejects
        sentences that too closely match the original text, namely those that
        contain any identical sequence of words of X length, where X is the
        smaller number of (a) `max_overlap_ratio` (default: 0.7) of the total
        number of words, and (b) `max_overlap_total` (default: 15).
        """
        # Reject large chunks of similarity
        overlap_ratio = int(round(max_overlap_ratio * len(words)))
        overlap_max = min(max_overlap_total, overlap_ratio)
        overlap_over = overlap_max + 1
        gram_count = max((len(words) - overlap_max), 1)
        grams = [ words[i:i+overlap_over] for i in range(gram_count) ]
        for g in grams:
            gram_joined = self.word_join(g)
            if gram_joined in self.rejoined_text:
                return False
        return True

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
        sentences = [ text[start:end].strip() for start, end in spans ]
    return sentences 

##############################################

