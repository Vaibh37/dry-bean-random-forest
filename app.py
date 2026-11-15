from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from frontend import attach_frontend
app = FastAPI()

model = joblib.load("random_forest_model.joblib")
print(model.feature_names_in_.tolist())


class BeanInput(BaseModel):
    Area: float
    Perimeter: float
    MajorAxisLength: float
    MinorAxisLength: float
    AspectRation: float
    Eccentricity: float
    ConvexArea: float
    EquivDiameter: float
    Extent: float
    Solidity: float
    roundness: float
    Compactness: float
    ShapeFactor1: float
    ShapeFactor2: float
    ShapeFactor3: float
    ShapeFactor4: float



@app.post("/predict")
def predict(bean:BeanInput):
    features = pd.DataFrame([bean.model_dump()])
    features = features[model.feature_names_in_]

    prediction = model.predict(features)[0]
    return {"Prediction" : str(prediction)}

attach_frontend(app, model, BeanInput)