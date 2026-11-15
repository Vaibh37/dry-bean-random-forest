
from pathlib import Path

import pandas as pd
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

SAMPLE = {
    "Area": 28395.0,
    "Perimeter": 610.291,
    "MajorAxisLength": 208.1781167085,
    "MinorAxisLength": 173.8887470416,
    "AspectRation": 1.1971914241,
    "Eccentricity": 0.5498121871,
    "ConvexArea": 28715.0,
    "EquivDiameter": 190.1410972745,
    "Extent": 0.7639225182,
    "Solidity": 0.9888559986,
    "roundness": 0.9580271263,
    "Compactness": 0.9133577548,
    "ShapeFactor1": 0.0073315061,
    "ShapeFactor2": 0.0031472892,
    "ShapeFactor3": 0.8342223882,
    "ShapeFactor4": 0.998723889,
}

GROUPS = [
    {
        "number": "01",
        "title": "Dimensions",
        "description": "Measurements of the bean's size and axes",
        "fields": [
            {"name": "Area", "label": "Area"},
            {"name": "Perimeter", "label": "Perimeter"},
            {"name": "MajorAxisLength", "label": "Major axis length"},
            {"name": "MinorAxisLength", "label": "Minor axis length"},
            {"name": "ConvexArea", "label": "Convex area"},
            {"name": "EquivDiameter", "label": "Equivalent diameter"},
        ],
    },
    {
        "number": "02",
        "title": "Shape metrics",
        "description": "Ratios and descriptors of the bean's outline",
        "fields": [
            {"name": "AspectRation", "label": "Aspect ratio"},
            {"name": "Eccentricity", "label": "Eccentricity"},
            {"name": "Extent", "label": "Extent"},
            {"name": "Solidity", "label": "Solidity"},
            {"name": "roundness", "label": "Roundness"},
            {"name": "Compactness", "label": "Compactness"},
        ],
    },
    {
        "number": "03",
        "title": "Shape factors",
        "description": "Four additional numerical shape descriptors",
        "fields": [
            {"name": "ShapeFactor1", "label": "Shape factor 1"},
            {"name": "ShapeFactor2", "label": "Shape factor 2"},
            {"name": "ShapeFactor3", "label": "Shape factor 3"},
            {"name": "ShapeFactor4", "label": "Shape factor 4"},
        ],
    },
]

def attach_frontend(app, model, bean_schema):
    app.mount(
        "/static",
        StaticFiles(directory=str(BASE_DIR / "static")),
        name="static"
    )

    def page(request, values, prediction=None, error=None, status_code=200):
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "groups": GROUPS,
                "values": values,
                "prediction": prediction,
                "error": error,
            },
            status_code=status_code,
        )

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def home(request: Request):
        return page(request, SAMPLE)

    @app.post("/classify", response_class=HTMLResponse, include_in_schema=False)
    async def classify(request: Request):
        values = dict(await request.form())

        try:
            bean = bean_schema.model_validate(values)
        except ValidationError:
            return page(
                request,
                values,
                error="Enter a valid number for all 16 measurements.",
                status_code=422,
            )

        features = pd.DataFrame([bean.model_dump()])
        features = features[list(model.feature_names_in_)]

        prediction = str(model.predict(features)[0])

        return page(
            request,
            bean.model_dump(),
            prediction=prediction
        )
