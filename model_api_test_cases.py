import subprocess
import unittest
import time
import requests
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score

from text_utils import clean_text


class ModelAPITestCase(unittest.TestCase):
    SERVER_URL = "http://localhost:8000"
    UP_URL = f"{SERVER_URL}/status"
    PREDICT_ONE_URL = f"{SERVER_URL}/predict"
    PREDICT_LIST_URL = f"{SERVER_URL}/predict-list"
    server_process = None

    @classmethod
    def setUpClass(cls):
        cls.server_process = subprocess.Popen(
            ["python", "serve.py", "--host", "127.0.0.1", "--port", "8000"]
        )
        timeout = 10
        start_time = time.time()
        while True:
            try:
                r = requests.get(cls.UP_URL)
                if r.status_code == 200:
                    break
            except requests.exceptions.ConnectionError:
                pass
            if time.time() - start_time > timeout:
                raise TimeoutError("Server did not start in time")
            time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        if cls.server_process:
            cls.server_process.terminate()
            cls.server_process.wait()

    def test_server_starts(self):
        response = requests.get(self.UP_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json(), {"status": "OK"})

    def test_model_predicts_one_non_fake_news_correctly(self):
        example_title = "Live from New York, it's a Trump-Clinton rematch - of sorts"
        example_text = (
            "NEW YORK (Reuters) - Veteran actor and frequent host Alec Baldwin returned to “Saturday Night Live” "
            "on Saturday, debuting his new gig playing a scowling, "
            "blustering Donald Trump, the Republican nominee for U.S. president. "
            "The late night NBC comedy show, kicking off its 42nd season, opened with an extended "
            "sketch featuring Baldwin as Trump facing off with a calculating, cunning and smug "
            "Hillary Clinton, with Kate McKinnon reprising her turn as the Democratic nominee. "
            "Much of the routine was lifted from the opponents’ Monday debate, including references to talk "
            "show host and Trump nemesis Rosie O’Donnell, and vocal Trump backer, Fox News’ Sean Hannity. "
            "Baldwin began his Trump routine promising “I’m going to be so good tonight,” before issuing a perfunctory "
            "response on jobs and economics. “End of story, I won the debate, I stayed calm just like I promised, "
            "and it, is, over. Goodnight,” he proclaimed before walking away. Told by the moderator there were still "
            "88 minutes left, “Trump” responded, “My microphone is broken,” adding “She broke it. With Obama.” "
            "Asked what she thought of Trump’s rambling discourse, a smirking McKinnon-as-Clinton replied "
            "“I think I’m going to be president.” The audience for the live show applauded wildly. After a few more minutes "
            "of Baldwin-as-Trump’s increasingly bizarre remarks, a swaggering Clinton asks “Can America vote right now?” "
            "Later, fighting tears, she explained, “This is going so well. It’s going exactly how I always dreamed.” "
            "The show’s writers made sure to take shots at the Democrat as well, including her referencing beauty queen "
            "Alicia Machado as “a political prop that I almost forgot to mention”. In her closing statement, Clinton said "
            "“Listen America, I get it, you hate me.” She then threatened that “If you don’t elect me, "
            "I will continue to run for president until the day I die.” Baldwin, who has hosted Saturday Night Live "
            "more than anyone in its storied history, will be back as Trump until the November election, likely "
            "providing a ratings spike for the show that has mined U.S. elections and politics for comic fodder since 1975. "
            "Trump himself appeared on the show as host in November 2015, when he was campaigning to win the Republican nomination.")

        response = requests.post(self.PREDICT_ONE_URL, json={"title": example_title, "text": example_text})

        self.assertEqual(200, response.status_code)
        self.assertEqual({"result": 0}, response.json())

    def test_model_prediction_is_above_80_percent(self):
        df_test_sample = pd.read_csv("evaluation.csv", sep=";",
                                     quotechar='"',
                                     escapechar="\\",
                                     engine="python")[:100]
        df_test_sample.title = df_test_sample.title.apply(clean_text)
        df_test_sample.text = df_test_sample.text.apply(clean_text)
        y_true = df_test_sample["label"].values

        predictions = []
        for _, row in df_test_sample.iterrows():
            data = {"title": row["title"], "text": row["text"]}
            response = requests.post(self.PREDICT_ONE_URL, json=data)
            pred = response.json()["result"]
            predictions.append(pred)

        acc = accuracy_score(y_true, predictions)
        print("Test set accuracy:", acc)
        self.assertGreaterEqual(acc, 0.8, "Accuracy below expected threshold!")

    def test_prediction_can_be_applied_to_whole_dataset(self):
        df_test_sample = pd.read_csv("evaluation.csv", sep=";",
                                     quotechar='"',
                                     escapechar="\\",
                                     engine="python")

        payload = [
            {"title": row.title, "text": row.text}
            for _, row in df_test_sample.iterrows()
        ]

        response = requests.post(self.PREDICT_LIST_URL, json=payload)
        pred = response.json()["result"]

        acc = balanced_accuracy_score(df_test_sample.label, pred)
        self.assertGreaterEqual(acc, 0.8, "Accuracy below expected threshold!")


if __name__ == '__main__':
    unittest.main()
