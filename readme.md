# FuzzyTextMatcher

The FuzzyTextMatcher class is designed for fuzzy text matching, allowing you to find approximate matches for a given text from a list of strings. This is useful in scenarios where exact matches are not possible due to variations in the text, such as typos, different spellings, or slight differences in phrasing.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/FuzzyTextMatcherV2.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Class Initialization

```python
FuzzyTextMatcher(
    list_of_strings: List[str],
    soft_similarity_cutoff: float = 0.5,
    hard_similarity_cutoff: float = 0.5,
    return_index: bool = False,
    search_bound: tuple = (-15, +15)
)
```
## Parameters
- list_of_strings (List[str]): A list of strings to match against.
- soft_similarity_cutoff (float): Minimum similarity score for an initial similarity matching. Range [0, 1]. Default to 0.5.
- hard_similarity_cutoff (float): Minimum similarity score for the final similarity match. Range [0, 1]. Default to 0.5.
- return_index (bool): If True, returns the index of the matched string in the original list_of_strings. Default to False.
- search_bound (tuple): Search boundary for matching, which updates the search space based on the boundary. Default to (-15, +15) characters.


## Example
```python
from fuzzy_text_matcher import FuzzyTextMatcher

list_of_strings = [
    "শাহপরান গেট শাখা",
    "শাহপরান গেট",
    "শাহপরান",
    "শাহপরান গেট ব্রাঞ্চ"
]

list_of_strings = sorted(list_of_strings, key=lambda x: (len(x), x))
ftm = FuzzyTextMatcher(
    list_of_strings=list_of_strings,
    soft_similarity_cutoff=0.5,
    hard_similarity_cutoff=0.5,
    search_bound=(-115, +115)
)
```
## Methods
### callable(self, text: str, search_bound: tuple = None, topk: int = None)
Performs fuzzy text matching.

### Parameters
- text (str): The text to match against.
- search_bound (tuple): Search boundary for matching. Default is the class-level search_bound.
- topk (int): Number of top matches to return. Default is None (returns all matches).
### Returns
- list: A list of matched texts and their scores.

### Example

```python
matches = ftm('আমার একাউন্ট টি শাহ মখদুম এভিনিউ ব্রাঞ্চ এ খুলেছি')
print(matches)
# Output: [
#    MatchedText(index=-1, text='শাহপরান গেট ব্রাঞ্চ', similarity=0.445, equality=0.388),
#    MatchedText(index=-1, text='শাহপরান গেট শাখা', similarity=0.344, equality=0.327),
#    MatchedText(index=-1, text='শাহপরান গেট', similarity=0.339, equality=0.224),
#    MatchedText(index=-1, text='শাহপরান', similarity=0.309, equality=0.143)
# ]

```

### get_span_from_matched_text(matched_text, query_text)
Gets the span of the matched text within the query text.

### Parameters
- matched_text (MatchedText): The matched text object.
- query_text (str): The query text.
### Returns
- tuple: Matched text and the span of the matched text in the query text.

### Example
```python
span = ftm.get_span_from_matched_text(matches[0], 'আমার একাউন্ট টি শাহ মখদুম এভিনিউ ব্রাঞ্চ এ খুলেছি')
print(span)
# Output: ('শাহ মখদুম এভিনিউ ব্রাঞ্চ', (16, 40))

```
### get_span_of_a_from_b(a, b)
Gets the span of text a within text b.

- Parameters
    - a (str): Text to find the span of.
    - b (str): Text to search within.
Returns
    - tuple: The span of text a in text b.
```python
span = ftm.get_span_of_a_from_b(a=matches[0].text, b='আমার একাউন্ট টি শাহ মখদুম এভিনিউ ব্রাঞ্চ এ খুলেছি')
print(span)
# Output: ('শাহ মখদুম এভিনিউ ব্রাঞ্চ', (16, 40))
```

## Internal Methods
- _format_texts(self, list_of_strings)
Formats the list of strings for efficient searching.

- _unordered_search(self, texts: str, text: str, topk: int = None)
Performs an unordered search for matching.

- _order_preserving_search(self, texts: str, text: str, topk: int = None)
Performs an order-preserving search for matching.

- _get_sequence_matcher_score(self, texts, text)
Calculates sequence matcher score.

- _get_length_equality_score(self, text_a, text_b)
Calculates length equality score.

- _get_search_bound(self, fuzzy_text_length: int, search_bound: tuple)
Calculates search boundary.

- _get_span(self, text, query_text)
Calculates the span of a substring within a text.

## Complete Example
Here’s a full example demonstrating how to use the FuzzyTextMatcher:

```python
from fuzzy_text_matcher import FuzzyTextMatcher

# Define a list of strings and sort it
list_of_strings = [
    "শাহপরান গেট শাখা",
    "শাহপরান গেট",
    "শাহপরান",
    "শাহপরান গেট ব্রাঞ্চ"
]

list_of_strings = sorted(list_of_strings, key=lambda x: (len(x), x))

# Initialize the FuzzyTextMatcher
ftm = FuzzyTextMatcher(
    list_of_strings=list_of_strings,
    soft_similarity_cutoff=0.5,
    hard_similarity_cutoff=0.5,
    search_bound=(-115, +115)
)

# Perform fuzzy text matching
matches = ftm('আমার একাউন্ট টি শাহ মখদুম এভিনিউ ব্রাঞ্চ এ খুলেছি')

# Output the matches
print(matches)
# Output: [
#    MatchedText(index=-1, text='শাহপরান গেট ব্রাঞ্চ', similarity=0.445, equality=0.388),
#    MatchedText(index=-1, text='শাহপরান গেট শাখা', similarity=0.344, equality=0.327),
#    MatchedText(index=-1, text='শাহপরান গেট', similarity=0.339, equality=0.224),
#    MatchedText(index=-1, text='শাহপরান', similarity=0.309, equality=0.143)
# ]

# Get the span of the matched text within the query text
span = ftm.get_span_from_matched_text(matches[0], 'আমার একাউন্ট টি শাহ মখদুম এভিনিউ ব্রাঞ্চ এ খুলেছি')
print(span)
# Output: ('শাহ মখদুম এভিনিউ ব্রাঞ্চ', (16, 40))

# Get the span of text 'a' within text 'b'
span = ftm.get_span_of_a_from_b(a=matches[0].text, b='আমার একাউন্ট টি শাহ মখদুম এভিনিউ ব্রাঞ্চ এ খুলেছি')
print(span)
# Output: ('শাহ মখদুম এভিনিউ ব্রাঞ্চ', (16, 40))
```
## Acknowledgments
- This project utilizes the fuzzywuzzy library for fuzzy string matching.
- Sequence matching functionality is provided by the difflib library.
## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.
