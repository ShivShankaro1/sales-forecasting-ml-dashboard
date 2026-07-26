from typing import Dict

import numpy as np
import pandas as pd

from config.settings import OUTPUT_DIR
from core.preprocessing import create_features


def forecast_sales(model_bundle: Dict, forecast_days: int) -> pd.DataFrame:
    model = model_bundle["model"]
    last_date = pd.to_datetime(model_bundle["last_date"])

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=forecast_days,
        freq="D",
    )

    future_df = pd.DataFrame({"Date": future_dates})
    future_features = create_features(pd.DataFrame({"Date": future_dates, "Sales": 0}))

    predictions = model.predict(future_features[model_bundle["feature_columns"]])
    predictions = np.maximum(predictions, 0)

    future_df["Predicted Sales"] = predictions.round(2)

    future_df.to_csv(OUTPUT_DIR / "forecast_output.csv", index=False)

    return future_df
