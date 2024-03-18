from typing import Generator, List

from transformers import AutoTokenizer, BatchEncoding

from tokenwise.models.base import (
    BaseTokenizerWrapper,
    Word,
    Token,
    Separator,
)


class HuggingFaceToken(Token):
    """
    A single token representation specific for HuggingFace models.
    """

    def is_partial(self):
        """
        Check if the token is a partial token.
        """
        return len(self.text) > 1 and (
            self.text.startswith("#") or self.text.endswith("#")
        )


class HuggingFaceTokenizer(BaseTokenizerWrapper):
    """
    A wrapper around the HuggingFace model and interacts with its tokenizer.
    Model might be specified by its name.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def iter_text_pieces(self, text: str) -> Generator[Word, None, None]:
        encoded_input: BatchEncoding = self.tokenizer(
            text, padding=True, truncation=True
        )

        # Get the tokens and the word ids they belong to.
        # A single word may consist of multiple tokens.
        special_token_texts = self.tokenizer.all_special_tokens
        token_ids = encoded_input.data["input_ids"]
        tokens = encoded_input.tokens()
        word_ids = encoded_input.word_ids()

        # Iterate over the words and yield a new word if the
        # id changes. Always yield a new word if the id is None.
        last_idx, last_word_id, last_word = 0, None, None
        for idx, word_id in enumerate(word_ids):
            # Here we know that the current word id is not None,
            # but if the last word id is None, we start a new word here.
            if word_id is not None and last_word_id is None:
                last_idx, last_word_id = idx, word_id
                continue

            # This is a continuation of the last word, so there are likely
            # multiple tokens that belong to the same word.
            if word_id is not None and word_id == last_word_id:
                continue

            # If the current word id is different from the last one,
            # we yield a new word with all the tokens since the last
            # yielded word. That means we exclude the current token.
            if word_id != last_word_id:
                word_tokens = [
                    HuggingFaceToken(
                        token_text,
                        token_ids[last_idx + i],
                        token_text in special_token_texts,
                    )
                    for i, token_text in enumerate(tokens[last_idx:idx])
                ]
                word_chars = encoded_input.word_to_chars(last_word_id)
                current_word = Word(
                    text[word_chars.start : word_chars.end],
                    word_tokens,
                    word_chars.start,
                    word_chars.end,
                )
                if (
                    last_word is not None
                    and last_word.end_index is not None
                    and current_word.start_index > last_word.end_index
                ):
                    yield Separator(
                        text[last_word.end_index : current_word.start_index]
                    )
                yield current_word
                last_idx, last_word_id, last_word = idx, word_id, current_word

            # If the current word is None, it is a special token
            # that does not belong to any real word. In that case,
            # we yield a new word with the current token.
            if word_id is None:
                word_tokens = [
                    HuggingFaceToken(
                        token_text,
                        token_ids[idx + i],
                        token_text in special_token_texts,
                    )
                    for i, token_text in enumerate(tokens[idx : idx + 1])
                ]
                current_word = Word(None, word_tokens)
                if (
                    last_word is not None
                    and current_word.start_index is not None
                    and last_word.end_index is not None
                    and current_word.start_index > last_word.end_index
                ):
                    yield Separator(
                        text[last_word.end_index : current_word.start_index]
                    )
                yield current_word
                last_idx, last_word_id, last_word = idx, word_id, current_word

    def get_all_tokens(self) -> List[Token]:
        """
        Get all the tokens from the tokenizer.
        """
        special_token_texts = [token.text for token in self.get_special_tokens()]
        return [
            HuggingFaceToken(token_text, token_id, token_text in special_token_texts)
            for token_text, token_id in zip(
                self.tokenizer.get_vocab().keys(), self.tokenizer.get_vocab().values()
            )
        ]

    def get_special_tokens(self) -> List[Token]:
        return [
            HuggingFaceToken(
                token_text, self.tokenizer.convert_tokens_to_ids(token_text), True
            )
            for token_text in self.tokenizer.all_special_tokens
        ]

    def get_unknown_token(self) -> Token:
        special_tokens = self.get_special_tokens()
        for token in special_tokens:
            if token.text == self.tokenizer.unk_token:
                return token
        raise ValueError("Unknown token not found")

    def finetune(self, texts: List[str], vocabulary_size: int):
        """
        Finetune the tokenizer on the new texts.
        """
        self.tokenizer.train_new_from_iterator(texts, vocabulary_size)


class SentenceTransformerTokenizer(HuggingFaceTokenizer):
    """
    A wrapper around the sentence transformer models available on
    HuggingFace. It is created just for a convenience, so that
    the user does not have to specify the model name prefix manually.
    """

    def __init__(self, model_name: str):
        super().__init__(f"sentence-transformers/{model_name}")
