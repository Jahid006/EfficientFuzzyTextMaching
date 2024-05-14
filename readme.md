# FuzzyTextMatcher

FuzzyTextMatcher is a Python class for fuzzy text matching, capable of efficiently finding similar strings within a list of strings. It utilizes various algorithms such as fuzzy matching and sequence matching to provide accurate results.

## Features

- **Fuzzy Matching**: Utilizes the `fuzzywuzzy` library to perform fuzzy matching based on similarity scores.
- **Sequence Matching**: Uses the `difflib` library to calculate sequence matcher scores.
- **Order Preservation**: Supports both order-preserving and unordered matching modes.
- **Customizable**: Provides options to customize similarity cutoff, search boundaries, and text preprocessing.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Jahid006/EfficientFuzzyTextMaching.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Example Usage

```python
from fuzzy_text_matcher import FuzzyTextMatcher

# Define a list of strings and sort it
list_of_strings = ['abc', 'abc', 'abc', 'abc', 'abc', 'abc', 'a', 'abbbbbbc','abbbbbb', 'abbbbb', 'abbbb', 'abb'][:]
list_of_strings = sorted(list_of_strings, key = lambda x: (len(x), x))

# Initialize FuzzyTextMatcher
ftm = FuzzyTextMatcher(
    list_of_strings=list_of_strings,
    similarity_cutoff=60,
    preserve_order=False, # if true, returns an order preserving list of matching text
    search_bound=(-15, +15)
)

# Perform fuzzy matching
matches = ftm('abbbbbbc')

# Display matched texts and their scores
for match in matches:
    print(match)
```
## Outputs

```bash
MatchedText(index=-1, text='abbbbbbc', similarity=1.0, equality=1.0)
MatchedText(index=-1, text='abbbbbb', similarity=0.956, equality=0.875)
MatchedText(index=-1, text='abbbbb', similarity=0.905, equality=0.75)
MatchedText(index=-1, text='abbbb', similarity=0.846, equality=0.625)
MatchedText(index=-1, text='abb', similarity=0.697, equality=0.375)
MatchedText(index=-1, text='abc', similarity=0.587, equality=0.375)
MatchedText(index=-1, text='a', similarity=0.481, equality=0.125)
```
## Parameters
- list_of_strings: List of strings to match against.
- similarity_cutoff: Minimum similarity score for a match (default: 80).
- preserve_order: Flag to indicate if order of matches should be preserved (default: False).
- search_bound: Search boundary for matching (default: (-15, +15)).
- process_text: Function to preprocess text before matching.
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- This project utilizes the fuzzywuzzy library for fuzzy string matching.
- Sequence matching functionality is provided by the difflib library.
## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.
