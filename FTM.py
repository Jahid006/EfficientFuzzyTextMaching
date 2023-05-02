from typing import List
from collections import namedtuple

from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher


class FuzzyTextMatcher(object):
    def __init__(
        self,
        list_of_strings: List[str],
        fuzzy_cutoff_score: int = 80,
        process_text: callable = lambda x: x
    ):
        self.fuzzy_cutoff_score = fuzzy_cutoff_score
        self.process_text = process_text
        self._format_texts(list_of_strings)
        self.return_format = namedtuple(
            'MatchedText',
            ['text', 'similarity', 'equality']
        )

    def _format_texts(self, list_of_strings):
        list_of_strings = sorted(list_of_strings, key=lambda x: (len(x), x))
        L = 0
        index = {0: 0}
        for idx, string in enumerate(list_of_strings):
            l = len(string)
            if l != L:
                index[l] = idx
                L = l

        index[L+1] = len(list_of_strings)

        self.texts = list_of_strings
        self.index = index
        self.max_length = len(list_of_strings[-1])

    def __call__(self, text: str, bound: tuple = (-1, +1)):

        assert len(text) > 0, 'Input text must be greater than zero'

        if bound:
            l, r = self._get_search_bound(len(text), bound)
            texts = self.texts[l: r]

        else:
            texts = self.texts

        matched_texts_and_scores = list(zip(
            *process.extractWithoutOrder(
                text,
                texts,
                scorer=fuzz.partial_ratio,
                score_cutoff=self.fuzzy_cutoff_score
            )
        ))

        if not matched_texts_and_scores:
            return []

        matched_texts, similarity_scores = matched_texts_and_scores

        sm_scores = [
            self._get_sequence_matcher_score(matched_text, text)
            for matched_text in matched_texts
        ]

        scores = [(s1+s2*2)/300 for s1, s2 in zip(similarity_scores, sm_scores)]
        equality_scores = [
            self._get_length_equality_score(matched_text, text)
            for matched_text in matched_texts
        ]

        matched_texts = [
            self.return_format(matched_text, round(score, 3), round(equality, 3))
            for matched_text, score, equality in zip(matched_texts, scores, equality_scores)
        ]

        return sorted(
            matched_texts,
            key=lambda t: (t.similarity, t.equality),
            reverse=True
        )

    def _get_sequence_matcher_score(self, texts, text):
        return SequenceMatcher(None, texts, text).ratio()*100

    def _get_length_equality_score(self, text_a, text_b):
        if not text_a or not text_b:
            return 0

        a, b = len(text_a), len(text_b)
        return 1/max(a/b, b/a)

    def _get_search_bound(self, fuzzy_text_length: int,  bound: tuple):
        l, r = bound
        l = max(fuzzy_text_length + l, 0)
        r = min(fuzzy_text_length + r, self.max_length)

        while (l not in self.index):
            l = l-1
        while (r not in self.index):
            r = r + 1

        return self.index[l], self.index[r] + 1


if __name__ == '__main__':
    list_of_strings = [
        'abc', 'abc', 'abc', 'abc', 'abc', 'abc', 'a', 'abbbbbbc', 'abbbbbb', 'abbbbb', 'abbbb', 'abb'
    ]
    list_of_strings = sorted(list_of_strings, key=lambda x: (len(x), x))

    ftm = FuzzyTextMatcher(
        list_of_strings=list_of_strings, fuzzy_cutoff_score=60
    )

    print(ftm('abbbbbbc'))
