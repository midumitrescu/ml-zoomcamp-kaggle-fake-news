# ml-zoomcamp-kaggle-fake-news
ML Zoomcamp Showcase Project for the midterm challenge

## Purpose of the project
Showcase the skills we got/learned during the ML Zoomcamp role.

## Problem
The problem at hand is automatically detecting if an article is
**fake news** or not. 

Why? Because we just get absolutely loaded with information. 
For a human, checking the content of an article is just too time-consuming and 
classical algorithms may/should not work!

Thus, an ML model should be the proper tool to solving the problem!

## How to build the project?

```
git@github.com:midumitrescu/ml-zoomcamp-kaggle-fake-news.git
cd ml-zoomcamp-kaggle-fake-news
conda create -n ml-zoomcamp-kaggle-fake-news python=3.10 -y
conda activate ml-zoomcamp-kaggle-fake-news
pip install .
pytest
```

You find some tests & also an integration test showing how the API works.

There are two endpoints:

1. /predict - for predicting one item
2. predict-list - for predicting a list of articles at once

## How to use the model/pipeline?
``` bash
curl --location 'https://ml-zoomcamp-kaggle-fake-news.fly.dev/predict' \
--header 'Content-Type: application/json' \
--data '{
    "title": "something that trump did!",
    "text": "Have you heard Epstein got released?"
}'
```

Just set in a JSON title and text and you should get a response.
0 means not fake news
1 means fake news

## Which dataset I used?

I used [this](https://www.kaggle.com/code/aadyasingh55/news-classification-model) kaggle dataset which promised to
give articles which are fake news but... it proved to be rubbish.
Sorry!

## Code

I did exploratory testing in [this python notebook](ExploreDataset.ipynb).
After that, I extracted the notebook to build the pipeline in [Pipeline.ipynb](Pipeline.ipynb). 
Remove the comments to download the kaggle dataset in the first cells!
The fast api script is in [serve.py](serve.py) and there are some tests.
The rest is pretty standard.

## Deployment
[click here](https://ml-zoomcamp-kaggle-fake-news.fly.dev/status)
If returns "UP", then it's running!

## OpenAPI
there is some auto generated open-api docs [here](https://ml-zoomcamp-kaggle-fake-news.fly.dev/docs)!

## Disclaimer
I thought the problem will be extra interesting and I could do some hyperparameter tunning.
Scikit-Lean does allow one to play with some parameter when extracting text.
However, I did not have enough time and... the model worked on the evaluation set extremely well, even when considering 
balanced accuracy score (of course, a classical pitfall is not to remember that news/fakenews classes are very imbalanced).

Unfortunately, the model does not work on new examples: 

```
curl --location 'https://ml-zoomcamp-kaggle-fake-news.fly.dev/predict-list' \
--header 'Content-Type: application/json' \
--data '[{
    "title": "something that trump did!",
    "text": "Have you heard Epstein got released?"
}, 
{"title": "Michael Jackson is still alive!",
"text": "Summary: The video published in 2014 claimed that Michael Jackson is still alive and escaped to LA. His mysterious death is still raising discussion between those who believe he is alive and those who do not, in a series of comments under the video. The respectable music magazine New Musical Express claims that it is user BeLiEve who posts regular videos claiming Jackson’s death was a hoax, and officially, Michael Jackson is dead and buried,but the discussion still exists and these youtube videos attract many viewers each year."},
{"title": "Is he alive?! Michael Jackson appears in a '\''selfie'\'' with the girl?!", "text": "It was a day of mourning for music fans on June 25, 2009 when Michael Jackson passed away. However, there are people who cannot accept that the King of pop music is dead, raising various conspiracy theories that say the singer is healthy and well. And a '\''selfie'\'' posted by his daughter, Paris Jackson, has only added fuel to the fire, Telegraph reports. image This was the original photo posted by his daughter. In the photo published by the 18-year-old, a shadow appears in the background, which has prompted fans of Jackson to say that it is her late father. At the same time, a video was published that elaborates on these theories with the title \"Dude! Michael Jackson was seen alive in 2016 in Paris Jackson'\''s Instagram photo. The video, which lasts less than two minutes, contains comments about the photo speculating about the presence of the singer. At the end, there is a zoom-in of the figure behind, showing the face of the hitmaker of the song \"Billie Jean\" in focus, Telegrafi informs.  Many fans have also commented on the photo of Paris on Instagram, casting doubts that it is about her father. Is this supposed to be Jackson or is it just a photomontage?! Is this supposed to be Jackson or is it just a photomontage?! However, not everyone is easily convinced by these statements, saying that it was edited and that from that shadow it is impossible to find out what or who is in the photograph. Jack Michael Jackson died on June 25, 2009. (Getty) The new theories come after another video was released earlier this year that claimed Jackson was in the crowd. According to those claims, the singer is hiding in Canada or Africa."}]'
```
returns that the last article is not fake news, while it [obviously is!](https://telegrafi.com/en/he-is-alive-michael-jackson-appears-in-selfie-girl-photovideo/)



