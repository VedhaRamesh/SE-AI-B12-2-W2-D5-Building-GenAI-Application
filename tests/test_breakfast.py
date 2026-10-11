import unittest

from breakfast import parse_breakfast_ideas


class ParseBreakfastIdeasTests(unittest.TestCase):
    def test_parses_exactly_five_numbered_ideas(self) -> None:
        response = "\n".join(
            f"{index}. **Breakfast {index}** — A balanced meal number {index}."
            for index in range(1, 6)
        )

        ideas = parse_breakfast_ideas(response)

        self.assertEqual(len(ideas), 5)
        self.assertEqual(ideas[0]["title"], "Breakfast 1")
        self.assertEqual(ideas[4]["description"], "A balanced meal number 5.")

    def test_rejects_fewer_than_five_ideas(self) -> None:
        response = "1. **Breakfast** — A balanced meal."

        with self.assertRaises(ValueError):
            parse_breakfast_ideas(response)

    def test_rejects_unexpected_numbering(self) -> None:
        response = "\n".join(
            f"{index + 1}. **Breakfast** — A balanced meal."
            for index in range(4)
        )
        response += "\n6. **Breakfast** — A balanced meal."

        with self.assertRaises(ValueError):
            parse_breakfast_ideas(response)


if __name__ == "__main__":
    unittest.main()
