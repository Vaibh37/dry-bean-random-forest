from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd
from frontend import attach_frontend

app = FastAPI()

model = joblib.load("random_forest_model.joblib")


class BeanInput(BaseModel):
    Area: float = Field(gt=0, allow_inf_nan=False)
    Perimeter: float = Field(gt=0, allow_inf_nan=False)
    MajorAxisLength: float = Field(gt=0, allow_inf_nan=False)
    MinorAxisLength: float = Field(gt=0, allow_inf_nan=False)
    AspectRation: float = Field(gt=0, allow_inf_nan=False)
    Eccentricity: float = Field(ge=0, le=1, allow_inf_nan=False)
    ConvexArea: float = Field(gt=0, allow_inf_nan=False)
    EquivDiameter: float = Field(gt=0, allow_inf_nan=False)
    Extent: float = Field(ge=0, le=1, allow_inf_nan=False)
    Solidity: float = Field(ge=0, le=1, allow_inf_nan=False)
    roundness: float = Field(ge=0, le=1, allow_inf_nan=False)
    Compactness: float = Field(ge=0, le=1, allow_inf_nan=False)
    ShapeFactor1: float = Field(gt=0, allow_inf_nan=False)
    ShapeFactor2: float = Field(gt=0, allow_inf_nan=False)
    ShapeFactor3: float = Field(gt=0, allow_inf_nan=False)
    ShapeFactor4: float = Field(gt=0, allow_inf_nan=False)


@app.post("/predict")
def predict(bean: BeanInput):
    features = pd.DataFrame([bean.model_dump()])
    features = features[model.feature_names_in_]
    prediction = model.predict(features)[0]
    return {"Prediction": str(prediction)}


attach_frontend(app, model, BeanInput)