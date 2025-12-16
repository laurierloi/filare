from dataclasses import dataclass

from faker import Faker

from filare.models.utils import html_line_breaks

faker = Faker()


@dataclass
class MultilineHypertext:
    raw: str  # Hypertext possibly also including newlines to break lines in diagram output

    @staticmethod
    def to(value):
        if isinstance(value, MultilineHypertext):
            return value

        if isinstance(value, str):
            return MultilineHypertext(raw=value)

        if isinstance(value, list):
            return MultilineHypertext(raw="<br>".join(value))

        return MultilineHypertext("")

    @property
    def clean(self):
        return html_line_breaks(self.raw)

    def __repr__(self):
        return self.raw

    def is_empty(self):
        return not self.raw


class FakeMultilineHypertextFactory:
    """faker-backed factory for MultilineHypertext."""

    @classmethod
    def create(cls, lines: int = 1, words_per_line: int = 3) -> MultilineHypertext:
        rows = [faker.sentence(nb_words=words_per_line) for _ in range(max(lines, 1))]
        return MultilineHypertext.to("\n".join(rows))
