
# Dry Bean Classification

**Project Overview**

This project implements a supervised multiclass classification workflow for identifying seven dry bean varieties from sixteen numerical descriptors of their geometry and shape. The objective is to develop, validate, and evaluate a Random Forest classifier using a reproducible experimental process.

The implementation includes model training, hyperparameter selection, performance evaluation, feature importance analysis, and model serialization. A FastAPI application provides a REST prediction endpoint and a web interface. Docker is used to package and run the inference application.

The classifier operates on numerical measurements extracted from bean images. It does not process raw images or perform image recognition.

**Dataset and Preparation**

The Dry Bean dataset is sourced from the UCI Machine Learning Repository and contains 13,611 observations across seven classes. Each observation contains sixteen numerical features and one categorical class label.

Data inspection identified no missing values and 68 duplicate records. Removing those duplicates reduced the dataset to 13,543 observations. The cleaned data was divided using a stratified 80 percent training and 20 percent testing split, resulting in 10,834 training observations and 2,709 testing observations. The split uses a fixed random seed of 42.

Stratification was applied to preserve the class distribution across the training and testing partitions.

**Modeling and Selection**

A `RandomForestClassifier` with 100 estimators and entropy as the splitting criterion serves as the primary estimator. Bootstrap sampling is enabled, and the number of features considered at each split is determined using the square root of the total feature count.

Random Forest combines multiple Decision Trees trained on different bootstrap samples. Random feature selection introduces additional variation between individual trees. The final classification is determined by aggregating their predictions.

Hyperparameter selection was performed on the training partition using `GridSearchCV` with five fold cross validation. The search evaluated four combinations of maximum tree depth and minimum samples per leaf, using classification accuracy as the selection metric.

The selected configuration uses unrestricted maximum tree depth and requires at least one training sample per leaf. GridSearchCV refitted the selected estimator on the complete training partition.

**Evaluation Results**

Baseline mean cross validation accuracy: **92.54%**

Selected model mean cross validation accuracy: **92.54%**

Selected model training accuracy: **100.00%**

Final test accuracy: **92.06%**

The selected configuration did not improve cross validation accuracy over the baseline configuration. The difference between training accuracy and test accuracy indicates that the model fits the training observations more closely than unseen observations.

The mean cross validation accuracy and final test accuracy are relatively close in this experiment. These results describe performance on the supplied dataset and split, rather than a guarantee of performance on independently collected data.

**Error Analysis**

The implementation generates a classification report and confusion matrix to evaluate the model across individual bean classes.

The classification report includes precision, recall, and F1 scores for each class. The confusion matrix identifies correct classifications and misclassifications between the seven varieties.

These measurements provide information that overall accuracy alone does not capture. Per class evaluation is particularly important because the dataset has an uneven class distribution.

**Model Interpretation**

The implementation calculates impurity based feature importance using the fitted Random Forest estimator.

Feature importance scores represent the normalized total reduction in the splitting criterion attributed to each feature across the forest. The scores are sorted and visualized using Matplotlib.

These values describe how the fitted estimator uses the input features. They should not be interpreted as causal effects or as evidence that features with low importance contain no predictive information.

**Model Serialization and Inference**

The selected estimator is serialized using `joblib` and stored as `random_forest_model.joblib`.

A FastAPI application loads the serialized model and exposes a `POST /predict` endpoint. Requests contain sixteen numerical features, and responses contain the predicted class label in JSON format.

Pydantic validates the request structure and numerical input types. The inference pipeline constructs a pandas DataFrame and uses the estimator's `feature_names_in_` attribute to preserve the feature order established during training.

The application also provides an HTML and CSS interface for submitting measurements through a browser. The interface uses server side form processing without JavaScript.

Model training and inference are separate operations. The API loads the saved estimator and does not retrain it when processing requests.

**Containerization**

The inference application is packaged using Docker.

The Docker image contains the Python runtime, required dependencies, FastAPI application, serialized model, and frontend files. The training dataset and training script are not required for inference and are excluded from the image.

The image was built and tested locally using Docker Desktop with the WSL 2 backend. Both the REST endpoint and the HTML prediction interface were verified inside the running container.

The application has not been deployed to a public hosting service.

**Implementation and Execution**

The project is implemented in Python using pandas for dataset operations, scikit-learn for model training and evaluation, Matplotlib for visualization, joblib for model serialization, FastAPI for inference, and Docker for containerization.

For local inference, install the dependencies listed in `requirements.txt` and execute `python -m uvicorn app:app --reload` from the repository root.

The web interface is available at `http://127.0.0.1:8000/`, and the interactive API documentation is available at `http://127.0.0.1:8000/docs`.

For model training and evaluation, install the additional `matplotlib` and `openpyxl` dependencies, retain `Dry_Bean_Dataset.xlsx` in the repository root, and execute `python main.py`.

To build the container image, execute `docker build -t dry-bean-api .`. To run the application in Docker, execute `docker run --rm -p 8001:8000 dry-bean-api`.

**Limitations**

The experiment evaluates a single model family using one stratified dataset split and five fold cross validation for model selection. Training accuracy exceeds test accuracy, indicating a generalization gap.

No external dataset validation, raw image inference pipeline, or production deployment is included. The classifier requires all sixteen numerical measurements for each prediction.

Feature importance is derived from impurity reduction and does not establish causal relationships between input measurements and class labels.

Additional validation on independently collected observations would be required before considering operational use.

**Data Attribution and Licensing**

Dataset: Dry Bean, UCI Machine Learning Repository.

Source: [https://archive.ics.uci.edu/dataset/602/dry%2Bbean](https://archive.ics.uci.edu/dataset/602/dry%2Bbean)

DOI: [https://doi.org/10.24432/C50S4B](https://doi.org/10.24432/C50S4B)

The original dataset is distributed under Creative Commons Attribution 4.0 International. The repository source code is distributed under the MIT License. The MIT License does not replace the dataset's original license. Dataset attribution is retained in the repository.
