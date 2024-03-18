import abc
import enum
from dataclasses import dataclass, field
from typing import Optional, List, Generator


class TokenType(str, enum.Enum):
    STANDARD = "standard"


@dataclass(frozen=True, slots=True, eq=True, repr=True, unsafe_hash=True)
class Token:
    """
    A single token representation.
    """

    text: str
    index: int
    is_special: bool = field(default=False, compare=False)

    def __str__(self) -> str:
        return self.text

    def is_partial(self):
        """
        Check if the token is a partial token.
        """
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class TextPiece(abc.ABC):
    """
    A text piece is either a word or a text separator used
    to split the text into words. For example, a space or a
    new line, but that depends on the tokenizer.
    """

    text: Optional[str]
    tokens: List[Token] = field(default_factory=list)

    def __str__(self) -> str:
        return self.text if self.text is not None else ""

    def is_word(self):
        """
        Check if the text piece is a word.
        """
        return False


@dataclass(frozen=True, slots=True, eq=True, repr=True, unsafe_hash=True)
class Separator(TextPiece):
    """
    A separator between the words.
    """

    pass


@dataclass(frozen=True, slots=True, eq=True, repr=True, unsafe_hash=True)
class Word(TextPiece):
    """
    A mapping between a single word and all the tokens that represent it.
    """

    start_index: Optional[int] = None
    end_index: Optional[int] = None

    def __str__(self) -> str:
        if self.text is None:
            return " ".join(token.text for token in self.tokens if not token.is_special)
        return self.text

    def is_special(self):
        """
        Check if the word contains any special tokens. If so, we can assume
        that the word is not a real word.
        :return:
        """
        return any(token.is_special for token in self.tokens)

    def is_word(self):
        """
        Check if the text piece is a word.
        """
        return True


class BaseTokenizerWrapper:
    """
    An interface for all the wrappers that are used to wrap the tokenizers. Since
    various tokenizers have different interfaces, this class is used to provide
    unified access to them.
    """

    def iter_text_pieces(self, text: str) -> Generator[TextPiece, None, None]:
        """
        Iterate over all the text pieces in the text and yield them.
        A single piece is either a word or a separator. We need both
        to be able to reconstruct the original text.
        :param text: The text to tokenize.
        """

        raise NotImplementedError

    def tokenize(self, text: str) -> List[TextPiece]:
        """
        Tokenize the text and return all the text pieces.
        :param text:
        :return:
        """
        return list(self.iter_text_pieces(text))

    def get_all_tokens(self) -> List[Token]:
        """
        Get all the tokens that the tokenizer uses.
        :return:
        """

        raise NotImplementedError

    def get_special_tokens(self) -> List[Token]:
        """
        Get all the special tokens that the tokenizer uses.
        :return:
        """

        raise NotImplementedError

    def get_unknown_token(self) -> Optional[Token]:
        """
        Get the unknown token that the tokenizer uses. If the tokenizer does not have
        an unknown token, return None.
        :return:
        """

        raise NotImplementedError
