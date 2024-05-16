import unittest
from fuzzy_text_matcher import FuzzyTextMatcher

class TestFuzzyTextMatcher(unittest.TestCase):

    def setUp(self):
        self.list_of_strings = [
            "শাহপরান গেট শাখা",
            "শাহপরান গেট",
            "শাহপরান",
            "শাহপরান গেট ব্রাঞ্চ"
        ]
        self.list_of_strings = sorted(self.list_of_strings, key=lambda x: (len(x), x))
        self.ftm = FuzzyTextMatcher(
            list_of_strings=self.list_of_strings,
            soft_similarity_cutoff=0.5,
            hard_similarity_cutoff=0.5,
            search_bound=(-115, +115)
        )

    def test_call(self):
        query = 'আমার একাউন্ট টি শাহ মখদুম এভিনিউ ব্রাঞ্চ এ খুলেছি'
        matches = self.ftm(query)
        expected_matches = [
            self.ftm.return_format(index=-1, text='শাহপরান গেট ব্রাঞ্চ', similarity=0.445, equality=0.388),
            self.ftm.return_format(index=-1, text='শাহপরান গেট শাখা', similarity=0.344, equality=0.327),
            self.ftm.return_format(index=-1, text='শাহপরান গেট', similarity=0.339, equality=0.224),
            self.ftm.return_format(index=-1, text='শাহপরান', similarity=0.309, equality=0.143)
        ]
        self.assertEqual(matches, expected_matches)

    def test_get_span_from_matched_text(self):
        query = 'আমার একাউন্ট টি শাহ মখদুম এভিনিউ ব্রাঞ্চ এ খুলেছি'
        matches = self.ftm(query)
        span = self.ftm.get_span_from_matched_text(matches[0], query)
        expected_span = ('শাহ মখদুম এভিনিউ ব্রাঞ্চ', (16, 40))
        self.assertEqual(span, expected_span)

    def test_get_span_of_a_from_b(self):
        query = 'আমার একাউন্ট টি শাহ মখদুম এভিনিউ ব্রাঞ্চ এ খুলেছি'
        matches = self.ftm(query)
        span = self.ftm.get_span_of_a_from_b(a=matches[0].text, b=query)
        expected_span = ('শাহ মখদুম এভিনিউ ব্রাঞ্চ', (16, 40))
        self.assertEqual(span, expected_span)

if __name__ == '__main__':
    unittest.main()
