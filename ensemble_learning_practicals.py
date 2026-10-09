"""
Ensemble Learning Practicals
============================
25 practical exercises covering Bagging, Random Forest, and Stacking.

Requirements:
    pip install scikit-learn pandas numpy matplotlib

Run:
    python ensemble_learning_practicals.py

The script uses built-in scikit-learn datasets, so no external dataset files
are needed. Some practicals display plots; close each plot window to continue.
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.base import clone
from sklearn.datasets import load_breast_cancer, load_diabetes, load_wine, make_classification, make_regression
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, mean_squared_error, roc_auc_score, precision_score,
    recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay,
    classification_report, PrecisionRecallDisplay, roc_curve
)
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import (
    BaggingClassifier, BaggingRegressor, RandomForestClassifier,
    RandomForestRegressor, StackingClassifier
)
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsRegressor


RANDOM_STATE = 42


def make_bagging_classifier(estimator=None, n_estimators=100, **kwargs):
    """Support both newer and older scikit-learn parameter names."""
    params = dict(n_estimators=n_estimators, random_state=RANDOM_STATE, **kwargs)
    if estimator is not None:
        try:
            return BaggingClassifier(estimator=estimator, **params)
        except TypeError:
            return BaggingClassifier(base_estimator=estimator, **params)
    return BaggingClassifier(**params)


def make_bagging_regressor(estimator=None, n_estimators=100, **kwargs):
    """Support both newer and older scikit-learn parameter names."""
    params = dict(n_estimators=n_estimators, random_state=RANDOM_STATE, **kwargs)
    if estimator is not None:
        try:
            return BaggingRegressor(estimator=estimator, **params)
        except TypeError:
            return BaggingRegressor(base_estimator=estimator, **params)
    return BaggingRegressor(**params)


def classification_data():
    data = load_breast_cancer()
    return train_test_split(
        data.data, data.target, test_size=0.25, random_state=RANDOM_STATE,
        stratify=data.target
    )


def regression_data():
    data = load_diabetes()
    return train_test_split(
        data.data, data.target, test_size=0.25, random_state=RANDOM_STATE
    )


def heading(number, title):
    print("\n" + "=" * 78)
    print(f"Practical {number}: {title}")
    print("=" * 78)


def practical_1():
    heading(1, "Bagging Classifier with Decision Trees: Accuracy")
    X_train, X_test, y_train, y_test = classification_data()
    model = make_bagging_classifier(
        DecisionTreeClassifier(random_state=RANDOM_STATE), n_estimators=100
    )
    model.fit(X_train, y_train)
    print(f"Bagging Classifier accuracy: {accuracy_score(y_test, model.predict(X_test)):.4f}")


def practical_2():
    heading(2, "Bagging Regressor with Decision Trees: MSE")
    X_train, X_test, y_train, y_test = regression_data()
    model = make_bagging_regressor(
        DecisionTreeRegressor(random_state=RANDOM_STATE), n_estimators=100
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print(f"Mean Squared Error (MSE): {mean_squared_error(y_test, pred):.4f}")


def practical_3():
    heading(3, "Random Forest Classifier on Breast Cancer: Feature Importance")
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.25, random_state=RANDOM_STATE,
        stratify=data.target
    )
    model = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    print(f"Accuracy: {accuracy_score(y_test, model.predict(X_test)):.4f}")
    importance = pd.Series(model.feature_importances_, index=data.feature_names)
    print("\nFeature importance scores (highest first):")
    print(importance.sort_values(ascending=False).to_string())


def practical_4():
    heading(4, "Random Forest Regressor vs Single Decision Tree")
    X_train, X_test, y_train, y_test = regression_data()
    models = {
        "Single Decision Tree": DecisionTreeRegressor(random_state=RANDOM_STATE),
        "Random Forest": RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE),
    }
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        print(f"{name:24s} MSE={mean_squared_error(y_test, pred):.4f}")


def practical_5():
    heading(5, "Random Forest Classifier: Out-of-Bag (OOB) Score")
    X_train, X_test, y_train, y_test = classification_data()
    model = RandomForestClassifier(
        n_estimators=300, oob_score=True, bootstrap=True,
        random_state=RANDOM_STATE, n_jobs=-1
    )
    model.fit(X_train, y_train)
    print(f"OOB score: {model.oob_score_:.4f}")
    print(f"Test accuracy: {accuracy_score(y_test, model.predict(X_test)):.4f}")


def practical_6():
    heading(6, "Bagging Classifier with SVM Base Estimator")
    X_train, X_test, y_train, y_test = classification_data()
    svm = make_pipeline(StandardScaler(), SVC(kernel="linear"))
    model = make_bagging_classifier(svm, n_estimators=20, max_samples=0.8)
    model.fit(X_train, y_train)
    print(f"Bagging + SVM accuracy: {accuracy_score(y_test, model.predict(X_test)):.4f}")


def practical_7():
    heading(7, "Random Forest Accuracy with Different Numbers of Trees")
    X_train, X_test, y_train, y_test = classification_data()
    results = []
    for n in [1, 10, 50, 100, 200, 400]:
        model = RandomForestClassifier(n_estimators=n, random_state=RANDOM_STATE, n_jobs=-1)
        model.fit(X_train, y_train)
        score = accuracy_score(y_test, model.predict(X_test))
        results.append((n, score))
        print(f"Trees={n:3d} | Accuracy={score:.4f}")
    pd.DataFrame(results, columns=["Number of Trees", "Accuracy"]).plot(
        x="Number of Trees", y="Accuracy", marker="o", legend=False
    )
    plt.title("Random Forest: Number of Trees vs Accuracy")
    plt.ylabel("Test Accuracy")
    plt.tight_layout()
    plt.show()


def practical_8():
    heading(8, "Bagging Classifier with Logistic Regression: ROC-AUC")
    X_train, X_test, y_train, y_test = classification_data()
    base = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000))
    model = make_bagging_classifier(base, n_estimators=30, max_samples=0.8)
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    print(f"ROC-AUC score: {roc_auc_score(y_test, prob):.4f}")


def practical_9():
    heading(9, "Random Forest Regressor: Feature Importance")
    data = load_diabetes()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.25, random_state=RANDOM_STATE
    )
    model = RandomForestRegressor(n_estimators=250, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    print(f"Test MSE: {mean_squared_error(y_test, model.predict(X_test)):.4f}")
    importance = pd.Series(model.feature_importances_, index=data.feature_names)
    print("\nFeature importance scores:")
    print(importance.sort_values(ascending=False).to_string())
    importance.sort_values().plot(kind="barh")
    plt.title("Random Forest Regressor Feature Importance")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.show()


def practical_10():
    heading(10, "Compare Bagging Classifier and Random Forest")
    X_train, X_test, y_train, y_test = classification_data()
    models = {
        "Bagging": make_bagging_classifier(
            DecisionTreeClassifier(random_state=RANDOM_STATE), n_estimators=150
        ),
        "Random Forest": RandomForestClassifier(n_estimators=150, random_state=RANDOM_STATE),
    }
    for name, model in models.items():
        model.fit(X_train, y_train)
        print(f"{name:16s} accuracy={accuracy_score(y_test, model.predict(X_test)):.4f}")


def practical_11():
    heading(11, "Random Forest Hyperparameter Tuning with GridSearchCV")
    X_train, X_test, y_train, y_test = classification_data()
    model = RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1)
    params = {
        "n_estimators": [100, 200],
        "max_depth": [None, 5, 10],
        "min_samples_split": [2, 5],
        "max_features": ["sqrt", 0.8],
    }
    search = GridSearchCV(model, params, cv=5, scoring="accuracy", n_jobs=-1)
    search.fit(X_train, y_train)
    print(f"Best parameters: {search.best_params_}")
    print(f"Best cross-validation accuracy: {search.best_score_:.4f}")
    print(f"Test accuracy: {accuracy_score(y_test, search.best_estimator_.predict(X_test)):.4f}")


def practical_12():
    heading(12, "Bagging Regressor with Different Numbers of Estimators")
    X_train, X_test, y_train, y_test = regression_data()
    results = []
    for n in [5, 10, 50, 100, 200]:
        model = make_bagging_regressor(
            DecisionTreeRegressor(random_state=RANDOM_STATE), n_estimators=n
        )
        model.fit(X_train, y_train)
        mse = mean_squared_error(y_test, model.predict(X_test))
        results.append((n, mse))
        print(f"Estimators={n:3d} | MSE={mse:.4f}")
    pd.DataFrame(results, columns=["Estimators", "MSE"]).plot(
        x="Estimators", y="MSE", marker="o", legend=False
    )
    plt.title("Bagging Regressor: Number of Estimators vs MSE")
    plt.tight_layout()
    plt.show()


def practical_13():
    heading(13, "Random Forest: Analyze Misclassified Samples")
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.25, random_state=RANDOM_STATE,
        stratify=data.target
    )
    model = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    mis_idx = np.flatnonzero(pred != y_test)
    print(f"Test accuracy: {accuracy_score(y_test, pred):.4f}")
    print(f"Misclassified samples: {len(mis_idx)} out of {len(y_test)}")
    if len(mis_idx):
        output = pd.DataFrame(X_test[mis_idx], columns=data.feature_names)
        output.insert(0, "Test row index", mis_idx)
        output["Actual label"] = y_test[mis_idx]
        output["Predicted label"] = pred[mis_idx]
        print("\nFirst 10 misclassified samples:")
        print(output.head(10).to_string(index=False))


def practical_14():
    heading(14, "Bagging Classifier vs Single Decision Tree")
    X_train, X_test, y_train, y_test = classification_data()
    models = {
        "Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE),
        "Bagging": make_bagging_classifier(
            DecisionTreeClassifier(random_state=RANDOM_STATE), n_estimators=150
        ),
    }
    for name, model in models.items():
        model.fit(X_train, y_train)
        print(f"{name:16s} accuracy={accuracy_score(y_test, model.predict(X_test)):.4f}")


def practical_15():
    heading(15, "Random Forest: Confusion Matrix")
    X_train, X_test, y_train, y_test = classification_data()
    model = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print(confusion_matrix(y_test, pred))
    ConfusionMatrixDisplay.from_predictions(
        y_test, pred, display_labels=load_breast_cancer().target_names,
        cmap="Blues"
    )
    plt.title("Random Forest Confusion Matrix")
    plt.tight_layout()
    plt.show()


def practical_16():
    heading(16, "Stacking Classifier: Decision Tree, SVM, Logistic Regression")
    X_train, X_test, y_train, y_test = classification_data()
    estimators = [
        ("tree", DecisionTreeClassifier(max_depth=5, random_state=RANDOM_STATE)),
        ("svm", make_pipeline(StandardScaler(), SVC(probability=True, random_state=RANDOM_STATE))),
        ("logreg", make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000))),
    ]
    model = StackingClassifier(
        estimators=estimators,
        final_estimator=LogisticRegression(max_iter=3000),
        cv=5
    )
    model.fit(X_train, y_train)
    print(f"Stacking Classifier accuracy: {accuracy_score(y_test, model.predict(X_test)):.4f}")
    for name, estimator in estimators:
        estimator.fit(X_train, y_train)
        print(f"{name:10s} accuracy={accuracy_score(y_test, estimator.predict(X_test)):.4f}")


def practical_17():
    heading(17, "Random Forest: Top 5 Important Features")
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.25, random_state=RANDOM_STATE,
        stratify=data.target
    )
    model = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    importance = pd.Series(model.feature_importances_, index=data.feature_names)
    print(importance.sort_values(ascending=False).head(5).to_string())


def practical_18():
    heading(18, "Bagging Classifier: Precision, Recall, and F1-score")
    X_train, X_test, y_train, y_test = classification_data()
    model = make_bagging_classifier(
        DecisionTreeClassifier(random_state=RANDOM_STATE), n_estimators=150
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print(f"Precision: {precision_score(y_test, pred, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_test, pred, zero_division=0):.4f}")
    print(f"F1-score:  {f1_score(y_test, pred, zero_division=0):.4f}")
    print("\nFull classification report:")
    print(classification_report(y_test, pred, target_names=load_breast_cancer().target_names))


def practical_19():
    heading(19, "Random Forest: Effect of max_depth on Accuracy")
    X_train, X_test, y_train, y_test = classification_data()
    results = []
    for depth in [1, 2, 3, 5, 8, 10, 15, None]:
        model = RandomForestClassifier(
            n_estimators=150, max_depth=depth, random_state=RANDOM_STATE, n_jobs=-1
        )
        model.fit(X_train, y_train)
        score = accuracy_score(y_test, model.predict(X_test))
        results.append((str(depth), score))
        print(f"max_depth={str(depth):4s} | Accuracy={score:.4f}")
    pd.DataFrame(results, columns=["max_depth", "Accuracy"]).plot(
        x="max_depth", y="Accuracy", marker="o", legend=False
    )
    plt.title("Random Forest: max_depth vs Accuracy")
    plt.ylabel("Test Accuracy")
    plt.tight_layout()
    plt.show()


def practical_20():
    heading(20, "Bagging Regressor: Decision Tree vs KNeighbors Regressor")
    X_train, X_test, y_train, y_test = regression_data()
    models = {
        "Decision Tree": make_bagging_regressor(
            DecisionTreeRegressor(random_state=RANDOM_STATE), n_estimators=100
        ),
        "KNeighbors": make_bagging_regressor(
            make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=7)),
            n_estimators=100
        ),
    }
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        print(f"{name:16s} MSE={mean_squared_error(y_test, pred):.4f}")


def practical_21():
    heading(21, "Random Forest: ROC-AUC Score")
    X_train, X_test, y_train, y_test = classification_data()
    model = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    probabilities = model.predict_proba(X_test)[:, 1]
    print(f"ROC-AUC score: {roc_auc_score(y_test, probabilities):.4f}")
    fpr, tpr, _ = roc_curve(y_test, probabilities)
    plt.plot(fpr, tpr, label=f"Random Forest AUC = {roc_auc_score(y_test, probabilities):.3f}")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Random Forest ROC Curve")
    plt.legend()
    plt.tight_layout()
    plt.show()


def practical_22():
    heading(22, "Bagging Classifier: Cross-validation")
    data = load_breast_cancer()
    model = make_bagging_classifier(
        DecisionTreeClassifier(random_state=RANDOM_STATE), n_estimators=100
    )
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    scores = cross_val_score(model, data.data, data.target, cv=cv, scoring="accuracy", n_jobs=-1)
    print("Fold accuracies:", np.round(scores, 4))
    print(f"Mean accuracy: {scores.mean():.4f}")
    print(f"Standard deviation: {scores.std():.4f}")


def practical_23():
    heading(23, "Random Forest: Precision-Recall Curve")
    X_train, X_test, y_train, y_test = classification_data()
    model = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    PrecisionRecallDisplay.from_estimator(model, X_test, y_test)
    plt.title("Random Forest Precision-Recall Curve")
    plt.tight_layout()
    plt.show()


def practical_24():
    heading(24, "Stacking Classifier: Random Forest + Logistic Regression")
    X_train, X_test, y_train, y_test = classification_data()
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=150, random_state=RANDOM_STATE),
        "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000)),
        "Stacking": StackingClassifier(
            estimators=[
                ("rf", RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)),
                ("lr", make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000))),
            ],
            final_estimator=LogisticRegression(max_iter=3000),
            cv=5
        ),
    }
    for name, model in models.items():
        model.fit(X_train, y_train)
        print(f"{name:22s} accuracy={accuracy_score(y_test, model.predict(X_test)):.4f}")


def practical_25():
    heading(25, "Bagging Regressor: Compare Bootstrap Sample Fractions")
    X_train, X_test, y_train, y_test = regression_data()
    results = []
    for fraction in [0.4, 0.6, 0.8, 1.0]:
        model = make_bagging_regressor(
            DecisionTreeRegressor(random_state=RANDOM_STATE),
            n_estimators=100, max_samples=fraction, bootstrap=True
        )
        model.fit(X_train, y_train)
        mse = mean_squared_error(y_test, model.predict(X_test))
        results.append((fraction, mse))
        print(f"max_samples={fraction:.1f} | MSE={mse:.4f}")
    pd.DataFrame(results, columns=["Bootstrap sample fraction", "MSE"]).plot(
        x="Bootstrap sample fraction", y="MSE", marker="o", legend=False
    )
    plt.title("Bootstrap Sample Fraction vs MSE")
    plt.tight_layout()
    plt.show()


PRACTICALS = {
    1: practical_1, 2: practical_2, 3: practical_3, 4: practical_4, 5: practical_5,
    6: practical_6, 7: practical_7, 8: practical_8, 9: practical_9, 10: practical_10,
    11: practical_11, 12: practical_12, 13: practical_13, 14: practical_14,
    15: practical_15, 16: practical_16, 17: practical_17, 18: practical_18,
    19: practical_19, 20: practical_20, 21: practical_21, 22: practical_22,
    23: practical_23, 24: practical_24, 25: practical_25,
}


def main():
    print("ENSEMBLE LEARNING PRACTICALS")
    print("1-25: Run one practical; 0: Run all; q: Quit")
    print("Note: practicals with plots open a window. Close it to continue.")
    while True:
        choice = input("\nEnter practical number (1-25), 0 for all, or q to quit: ").strip().lower()
        if choice == "q":
            print("Exiting.")
            break
        if choice == "0":
            for number, function in PRACTICALS.items():
                try:
                    function()
                except Exception as exc:
                    print(f"\nPractical {number} failed: {type(exc).__name__}: {exc}")
            continue
        try:
            number = int(choice)
        except ValueError:
            print("Please enter a number from 0 to 25, or q.")
            continue
        if number not in PRACTICALS:
            print("Please enter a number from 0 to 25, or q.")
            continue
        try:
            PRACTICALS[number]()
        except Exception as exc:
            print(f"Practical {number} failed: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
