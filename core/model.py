from typing import Dict

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from config.settings import FEATURE_COLUMNS, MODEL_PATH, OUTPUT_DIR
from core.preprocessing import create_features


def train_models(daily_df: pd.DataFrame) -> Dict:
    if len(daily_df) < 30:
        raise ValueError("At least 30 days of sales data is required for training.")

    feature_df = create_features(daily_df)

    X = feature_df[FEATURE_COLUMNS]
    y = feature_df["Sales"]

    split_index = int(len(feature_df) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=150,
            random_state=42,
            max_depth=10,
        ),
        "Gradient Boosting Regressor": GradientBoostingRegressor(
            random_state=42,
            n_estimators=150,
            learning_rate=0.06,
            max_depth=3,
        ),
    }

    comparison_rows = []
    prediction_results = {}
    best_model_name = ""
    best_model = None
    best_rmse = float("inf")

    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        rmse = mean_squared_error(y_test, predictions) ** 0.5
        r2 = r2_score(y_test, predictions)

        comparison_rows.append(
            {
                "Model": name,
                "MAE": round(mae, 2),
                "RMSE": round(rmse, 2),
                "R2 Score": round(r2, 4),
            }
        )

        result_df = pd.DataFrame(
            {
                "Date": feature_df.iloc[split_index:]["Date"].values,
                "Actual Sales": y_test.values,
                "Predicted Sales": predictions,
                "Error": y_test.values - predictions,
            }
        )

        prediction_results[name] = result_df

        if rmse < best_rmse:
            best_rmse = rmse
            best_model_name = name
            best_model = model

    comparison_df = pd.DataFrame(comparison_rows).sort_values("RMSE")

    best_prediction_df = prediction_results[best_model_name]

    model_bundle = {
        "model_name": best_model_name,
        "model": best_model,
        "feature_columns": FEATURE_COLUMNS,
        "last_date": daily_df["Date"].max(),
        "trained_rows": len(X_train),
        "tested_rows": len(X_test),
        "trained_on": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    joblib.dump(model_bundle, MODEL_PATH)

    comparison_df.to_csv(OUTPUT_DIR / "model_comparison.csv", index=False)
    best_prediction_df.to_csv(OUTPUT_DIR / "actual_vs_predicted.csv", index=False)

    return {
        "model_bundle": model_bundle,
        "comparison": comparison_df,
        "best_prediction": best_prediction_df,
        "metrics": comparison_df.iloc[0].to_dict(),
    }


def load_saved_model() -> Dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Saved model not found. Please train the model first.")

    return joblib.load(MODEL_PATH)
