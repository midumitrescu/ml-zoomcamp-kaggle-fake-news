import os
import pickle

import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel, ValidationError
from requests import Request
from starlette.responses import JSONResponse

from text_utils import clean_text

KEY_TITLE = "title"
KEY_TEXT = "text"


class PredictRequest(BaseModel):
    title: str
    text: str


def load_pipeline(version: int):
    with open(f"pipeline_v{version}.pickle", "rb") as f:
        return pickle.load(f)


app = FastAPI(title="ML-Zoomcamp-Midterm-Challenge-Kaggle-Fake-News-Detector")
preferred_model_version: int = int(os.getenv("PARAM_VERSION", "1").lower())

pipeline = load_pipeline(preferred_model_version)

MEDIA_TYPE_JSON_PROBLEM = "application/problem+json"
BASE_PROBLEM_URL = "https://mlzoomcamp.api/problems"


@app.get("/status")
def ping():
    return {"status": "OK"}


@app.post("/predict")
def predict_one(request: PredictRequest, version=preferred_model_version):
    df = to_df(incoming_payload=[request])
    prediction = pipeline.predict(df)
    prediction_as_int = int(prediction[0]) if isinstance(prediction[0], np.generic) else prediction[0]
    return JSONResponse(
        content={"result": prediction_as_int},
        media_type="application/json"
    )


@app.post("/predict-list")
def predict_list(request: list[PredictRequest], version=preferred_model_version):
    df = to_df(incoming_payload=request)
    prediction = pipeline.predict(df)
    return JSONResponse(
        content={"result": prediction.tolist()},
        media_type="application/list+json"
    )


def to_df(incoming_payload: list[PredictRequest]) -> pd.DataFrame:
    data = [
        {
            KEY_TITLE: clean_text(item.title),
            KEY_TEXT: clean_text(item.text)
        } for item in incoming_payload]
    return pd.DataFrame(data)


def create_problem(type_: str, title: str, status: int, detail: str, instance: str):
    return {
        "type": type_,
        "title": title,
        "status": status,
        "detail": detail,
        "instance": instance
    }


@app.exception_handler(ValidationError)
async def handle_validation_error(request: Request, e: ValidationError):
    problem = create_problem(
        type_="/invalid-input",
        title="Invalid input",
        status=400,
        detail=str(e),
        instance=str(request.url)
    )
    logger.debug("Request {} was not valid {}. Returned problem was {}", request, e, problem)
    return JSONResponse(status_code=400, content=problem, media_type=MEDIA_TYPE_JSON_PROBLEM)


@app.exception_handler(FileNotFoundError)
async def handle_model_not_found_error(request: Request, e: FileNotFoundError):
    problem = create_problem(
        type_=f"{BASE_PROBLEM_URL}/model-not-found",
        title="Model not found",
        status=500,
        detail=str(e),
        instance=str(request.url)
    )
    logger.debug("Request {} returned file not found {}. Returned problem was {}", request, e, problem)
    return JSONResponse(status_code=500, content=problem, media_type=MEDIA_TYPE_JSON_PROBLEM)


@app.exception_handler(Exception)
async def handle_generic_exception(request: Request, e: Exception):
    problem = create_problem(
        type_=f"{BASE_PROBLEM_URL}/internal-error",
        title="Internal server error",
        status=500,
        detail="An unexpected error occurred.",
        instance=str(request.url)
    )
    logger.debug("Request {} returned unexpected exception {}. Returned problem was {}", request, e, problem)
    return JSONResponse(status_code=500, content=problem, media_type=MEDIA_TYPE_JSON_PROBLEM)


if __name__ == "__main__":
    logger.info(f"Detected preferred version {preferred_model_version}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
