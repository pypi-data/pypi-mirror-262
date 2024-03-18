from functools import cached_property
from typing import Iterable, List

from tokenwise.models.base import TextPiece, BaseTokenizerWrapper, Token


class TokenizerQuality:
    """
    A class that provides methods to measure the quality of a tokenizer. It gets a list of texts, conver
    """

    # TODO: should the CLS and SEP tokens be removed from the tokenized texts?

    def __init__(self, tokenizer: BaseTokenizerWrapper, texts: Iterable[str]):
        self.tokenizer = tokenizer
        self.texts = texts
        self.tokenized_texts = None

    @cached_property
    def tokenized(self) -> List[List[TextPiece]]:
        """
        Tokenize the texts and return the tokenized texts.
        """
        return [self.tokenizer.tokenize(text) for text in self.texts]

    @cached_property
    def words(self) -> List[TextPiece]:
        """
        Get all the words from the tokenized texts.
        """
        return [
            text_piece
            for tokenized_text in self.tokenized
            for text_piece in tokenized_text
            if text_piece.is_word()
        ]

    @cached_property
    def tokens(self) -> List[Token]:
        """
        Get all the tokens from the tokenized texts.
        """
        return [token for text_piece in self.words for token in text_piece.tokens]

    def avg_tokens_per_word(self) -> float:
        sum_tokens, count_words = 0, 0
        for text_piece in self.words:
            if not text_piece.is_word():
                continue
            sum_tokens += len(text_piece.tokens)
            count_words += 1
        return sum_tokens / count_words

    def unknown_token_percentage(self) -> float:
        unknown_token = self.tokenizer.get_unknown_token()
        return len([token for token in self.tokens if token == unknown_token]) / len(
            self.tokens
        )

    def partial_token_percentage(self) -> float:
        return len([token for token in self.tokens if token.is_partial()]) / len(
            self.tokens
        )
