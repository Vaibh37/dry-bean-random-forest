import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

df = pd.read_excel("Dry_Bean_Dataset.xlsx")
df = df.drop_duplicates()

X = df.drop(columns=["Class"])
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    criterion="entropy",
    max_features="sqrt",
    bootstrap=True,
    random_state=42
)

model.fit(X_train, y_train)

scores = cross_val_score(
    model,
    X_train,
    y_train,
    cv=5,
    scoring="accuracy"
)

print("Baseline CV scores:", scores)
print("Baseline mean CV accuracy:", scores.mean())
print("Baseline training accuracy:", model.score(X_train, y_train))

param_grid = {
    "max_depth": [None, 12],
    "min_samples_leaf": [1, 3]
}

grid = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=5,
    scoring="accuracy"
)

grid.fit(X_train, y_train)

print("Best parameters:", grid.best_params_)
print("Best CV accuracy:", grid.best_score_)

best_model = grid.best_estimator_

y_pred = best_model.predict(X_test)

print("Final training accuracy:", best_model.score(X_train, y_train))
print("Final test accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=best_model.classes_
)

display.plot(cmap="Blues")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

importance = pd.Series(
    best_model.feature_importances_,
    index=X.columns
)

sorted_importance = importance.sort_values(ascending=True)

plt.figure(figsize=(10, 8))
plt.barh(sorted_importance.index, sorted_importance.values)
plt.xlabel("Feature Importance Score")
plt.ylabel("Bean Features")
plt.title("Random Forest Feature Importance")
plt.tight_layout()
plt.show()

joblib.dump(best_model, "random_forest_model.joblib")
