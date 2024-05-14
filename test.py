import unittest
from fuzzy_text_matcher import FuzzyTextMatcher


class TestFuzzyTextMatcher(unittest.TestCase):

    def test_unordered_search(self):
        matcher = FuzzyTextMatcher(["apple", "banana", "orange"])
        matches = matcher("app")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].text, "apple")

    def test_order_preserving_search(self):
        matcher = FuzzyTextMatcher(["apple", "banana", "orange"], preserve_order=True)
        matches = matcher("app")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].index, 0)  # Matches with 'apple'

    def test_empty_input_text(self):
        matcher = FuzzyTextMatcher(["apple", "banana", "orange"])
        with self.assertRaises(AssertionError):
            matcher("")

    def test_empty_text_list(self):
        matcher = FuzzyTextMatcher([])
        matches = matcher("apple")
        self.assertEqual(matches, [])

    def test_similarity_cutoff(self):
        matcher = FuzzyTextMatcher(["apple", "banana", "orange"], similarity_cutoff=90)
        matches = matcher("appl")
        self.assertEqual(matches, [])  # No match above 90% similarity

    def test_search_bound(self):
        matcher = FuzzyTextMatcher(["apple", "banana", "orange"])
        matches = matcher("apple", search_bound=(0, 0))
        self.assertEqual(len(matches), 1)  # Matches with 'apple'

    def test_process_text(self):
        def process(text):
            return text.upper()

        matcher = FuzzyTextMatcher(["apple", "banana", "orange"], process_text=process)
        matches = matcher("APPLE")
        self.assertEqual(len(matches), 1)  # Matches with 'apple'

    def test_length_equality_score(self):
        matcher = FuzzyTextMatcher(["apple", "banana", "orange"])
        score = matcher._get_length_equality_score("apple", "banana")
        self.assertAlmostEqual(score, 0.571, delta=0.001)  # Length ratio: 5/6

    def test_sequence_matcher_score(self):
        matcher = FuzzyTextMatcher(["apple", "banana", "orange"])
        score = matcher._get_sequence_matcher_score("apple", "appl")
        self.assertEqual(score, 100.0)  # Exact match


if __name__ == "__main__":
    unittest.main()
