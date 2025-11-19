import unittest

from serve import to_df, PredictRequest


class PredictRequestToDfTEstCase(unittest.TestCase):

    def test_when_list_is_empty_then_returned_df_is_empty(self):
       df = to_df([])
       self.assertEqual(len(df), 0)

    def test_conversion_of_one_request_item_to_df(self):
       df = to_df([PredictRequest(title="test", text="text for the test")])
       self.assertEqual(len(df), 1)
       self.assertEqual(df.title[0], "test")
       self.assertEqual(df.text[0], "text for the test")

    def test_conversion_of_two_to_df(self):
       df = to_df([PredictRequest(title="test 0", text="text for the test 0"),
                   PredictRequest(title="test 1", text="text for the test 1")])
       self.assertEqual(len(df), 2)
       for index in [0, 1]:
           self.assertEqual(df.title[index], f"test {index}")
           self.assertEqual(df.text[index], f"text for the test {index}")

    def test_conversion_of_one_request_item_to_df_is_cleaning_text(self):
        df = to_df([PredictRequest(title="test!!!!", text="Text ! for the test;;")])
        self.assertEqual(len(df), 1)
        self.assertEqual(df.title[0], "test")
        self.assertEqual(df.text[0], "text for the test")



if __name__ == '__main__':
    unittest.main()
