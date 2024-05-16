from typing import List
from collections import namedtuple, defaultdict
from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher


class FuzzyTextMatcher(object):
    """
    FuzzyTextMatcher is a class for fuzzy text matching.
    """

    def __init__(
        self,
        list_of_strings: List[str],
        soft_similarity_cutoff: float = 0.5,
        hard_similarity_cutoff: float = 0.5,
        return_index: bool = False,
        search_bound: tuple = (-15, +15),
    ):
        """
        Initializes FuzzyTextMatcher with the provided parameters.

        Args:
            list_of_strings (List[str]): List of strings to match against.
            soft_similarity_cutoff (int): Minimum similarity score for a initial similarity matching. Range [0,1].
            hard_similarity_cutoff (int): Minimum similarity score for a the final similarity match. Range [0,1].
            return_index (bool): Flag to indicate if index of the in the original list_of_strings is needed to be returned.
            search_bound (tuple): Search boundary for matching. The search space will be updated based the boundary.
        """

        self.soft_similarity_cutoff = soft_similarity_cutoff*100
        self.hard_similarity_cutoff = hard_similarity_cutoff
        self.return_index = return_index
        self.search_bound = search_bound
        self._format_texts(list_of_strings)
        self.return_format = namedtuple(
            "MatchedText", ["index", "text", "similarity", "equality"]
        )

    def _format_texts(self, list_of_strings):
        """
        Formats the list of strings for efficient searching.

        Args:
            list_of_strings (List[str]): List of strings to format.
        """
        if self.return_index:
            self.text_to_index = defaultdict(list)
            for idx, _string in enumerate(list_of_strings):
                self.text_to_index[_string].append(idx)

        self.number_of_strings = len(list_of_strings)
        list_of_strings = sorted(list(set(list_of_strings)), key=lambda x: (len(x), x))
        L = 0
        index = {0: 0}
        for idx, string in enumerate(list_of_strings):
            l = len(string)
            if l != L:
                index[l] = idx
                L = l

        index[L + 1] = len(list_of_strings)

        self.texts = list_of_strings
        self.index = index
        self.max_length = len(list_of_strings[-1])

    def __call__(self, text: str, search_bound: tuple = None, topk: int = None):
        """
        Performs fuzzy text matching.

        Args:
            text (str): Text to match against.
            search_bound (tuple(int, int)): Search boundary for matching.
            topk (int): to return topk matches

        Returns:
            list: List of matched texts and their scores.
        """
        assert len(text) > 0, "Input text must be greater than zero"
        search_bound = search_bound if search_bound else self.search_bound

        if search_bound:
            l, r = self._get_search_bound(len(text), search_bound)
            texts = self.texts[l:r]
        else:
            texts = self.texts

        if self.return_index:
            return self._order_preserving_search(texts, text, topk)
        
        return self._unordered_search(texts, text, topk)

    def _unordered_search(self, texts: str, text: str, topk: int = None):
        """
        Performs unordered search for matching.

        Args:
            texts (str): List of texts to search within.
            text (str): Text to match against.
            topk (int): to return topk matches

        Returns:
            list: List of matched texts and their scores.
        """
        matched_texts_and_scores = list(
            zip(
                *process.extractWithoutOrder(
                    text,
                    texts,
                    scorer=fuzz.partial_ratio,
                    score_cutoff=self.soft_similarity_cutoff,
                )
            )
        )

        if not matched_texts_and_scores:
            return []

        matched_texts, similarity_scores = matched_texts_and_scores

        sm_scores = [
            self._get_sequence_matcher_score(matched_text, text)
            for matched_text in matched_texts
        ]

        scores = [(s1 + s2 * 2) / 300 for s1, s2 in zip(similarity_scores, sm_scores)]
        equality_scores = [
            self._get_length_equality_score(matched_text, text)
            for matched_text in matched_texts
        ]

        matched_texts = [
            self.return_format(-1, matched_text, round(score, 3), round(equality, 3))
            for matched_text, score, equality in zip(
                matched_texts, scores, equality_scores
            )
        ]

        if not topk:
            topk = len(matched_texts)

        return sorted(
            matched_texts, key=lambda t: (t.similarity, t.equality), reverse=True
        )[:topk]

    def _order_preserving_search(self, texts: str, text: str, topk: int = None):
        """
        Performs order-preserving search for matching.

        Args:
            texts (str): List of texts to search within.
            text (str): Text to match against.
            topk (int): to return topk matches

        Returns:
            list: Matched texts along with their indices and scores.
        """
        matched_texts_and_scores = list(zip(
            *process.extractWithoutOrder(
                text,
                texts,
                scorer=fuzz.partial_ratio,
                score_cutoff=self.soft_similarity_cutoff
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

        matched_texts = sorted(
            matched_texts, key=lambda t: (t.similarity, t.equality), reverse=True
        )

        matched_text_info = []

        for matched_text, score, equality in zip(matched_texts, scores, equality_scores):
            for idx in self.text_to_index[matched_text]:
                matched_text_info.append(self.return_format(
                    idx, matched_text, round(score, 3), round(equality, 3)
                ))
                if topk and len(matched_text_info) > topk:
                    break
        
        return matched_text_info

    def _get_sequence_matcher_score(self, texts, text):
        """
        Calculates sequence matcher score.

        Args:
            texts (str): Text to compare.
            text (str): Reference text.

        Returns:
            float: Sequence matcher score.
        """
        return SequenceMatcher(None, texts, text).ratio() * 100

    def _get_length_equality_score(self, text_a, text_b):
        """
        Calculates length equality score.

        Args:
            text_a (str): First text.
            text_b (str): Second text.

        Returns:
            float: Length equality score.
        """
        if not text_a or not text_b:
            return 0

        a, b = len(text_a), len(text_b)
        return 1 / max(a / b, b / a)

    def _get_search_bound(self, fuzzy_text_length: int, search_bound: tuple):
        """
        Calculates search boundary.

        Args:
            fuzzy_text_length (int): Length of the text to search.
            search_bound (tuple): Search boundary.

        Returns:
            tuple: Left and right indices of the search boundary.
        """
        l, r = search_bound
        l = max(fuzzy_text_length + l, 0)
        r = min(fuzzy_text_length + r, self.max_length)

        while l not in self.index:
            l = l - 1
        while r not in self.index:
            r = r + 1

        return self.index[l], self.index[r] + 1

    def _get_span(self, text, query_text):
        sq = SequenceMatcher(None, text, query_text)
        matching_blocks = list(sq.get_matching_blocks())[:-1]

        if matching_blocks:
            l = matching_blocks[0].a
            r = matching_blocks[-1].a+ matching_blocks[-1].size
            return (text[l:r], (l,r))
        return ('', (-1,-1))
    
    def get_span_from_matched_text(self, matched_text, query_text):
        return self._get_span(query_text, matched_text.text)
    
    def get_span_of_a_from_b(self, a, b):
        return self._get_span(b, a)


        


