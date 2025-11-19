import unittest

from text_utils import clean_text


class TextCleanUpTestCase(unittest.TestCase):

    def test_when_text_is_empty_then_same_is_returned(self):
        self.assertEqual("", clean_text(""))

    def test_when_text_is_none_then_empty_is_returned(self):
        self.assertEqual("", clean_text(None))

    def test_when_text_contains_upper_case_text_then_it_is_converted_to_lowercase(self):
        self.assertEqual("hello", clean_text("HeLLo"))

    def test_when_text_contains_paranthesis_then_it_does_not_exist_anymore(self):
        self.assertEqual("hey i am testing you", clean_text("Hey (i am testing you)"))
        self.assertEqual("hey i am testing you", clean_text("Hey (i am testing you"))
        self.assertEqual("hey i am testing you", clean_text("Hey i am testing you)"))
        self.assertEqual("hey i am testing you", clean_text("Hey i am testing you)"))
        self.assertEqual("hey", clean_text("Hey()"))

    def test_when_text_contains_special_characters_then_they_do_not_exist_anymore(self):
        self.assertEqual("hey i am testing you", clean_text("hey \i \\am \\testing \ you"))

    def test_when_text_contains_punctuation_marks_then_they_get_removed(self):
        self.assertEqual("are you an interviewer and checking my code welcome",
                         clean_text("Are you an interviewer and checking my code? Welcome!"))
        self.assertEqual("guess what i was looking forward to this",
                         clean_text("Guess what!?: I was looking forward to this"))
        self.assertEqual("the truth is sometimes programmers to crazy stuff in the code",
                         clean_text("The truth is;sometimes programmers to crazy stuff in the code!"))


if __name__ == '__main__':
    unittest.main()
