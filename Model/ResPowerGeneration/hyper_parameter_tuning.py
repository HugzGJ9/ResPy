import optuna
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from lightgbm import LGBMRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

from API.OPENMETEO.Config_class import cfg
from Asset_Modeling.Energy_Modeling.data.data import fetchGenerationHistoryData
from Model.ResPowerGeneration.targets import TARGETS
from Model.ResPowerGeneration.dataProcessing import dataRESGenerationCleaning

def build_preprocessor(feats):
    return ColumnTransformer([
        ("num", StandardScaler(), feats)
    ])

def objective(trial, df, techno):
    feats = TARGETS[techno]
    mask = df[feats + [techno]].notnull().all(axis=1)
    X, y = df.loc[mask, feats], df.loc[mask, techno]

    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
        "learning_rate": trial.suggest_float("learning_rate", 0.005, 0.2, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 16, 256),
        "max_depth": trial.suggest_int("max_depth", 3, 20),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "random_state": cfg.random_seed
    }

    model = LGBMRegressor(**params)

    pipe = Pipeline([
        ("prep", build_preprocessor(feats)),
        ("model", model)
    ])

    tscv = TimeSeriesSplit(n_splits=5)
    scores = cross_val_score(pipe, X, y, cv=tscv, scoring="neg_mean_squared_error")

    return -scores.mean()

def run_optimization(df: pd.DataFrame, techno: str, n_trials: int = 50):
    study = optuna.create_study(direction="minimize")
    study.optimize(lambda trial: objective(trial, df, techno), n_trials=n_trials)

    print(f"\nBest parameters for {techno}:")
    for k, v in study.best_params.items():
        print(f"{k}: {v}")
    print(f"Best MSE: {study.best_value:.4f}")

    return study.best_params

if __name__ == "__main__":
    df = fetchGenerationHistoryData("FR")

    # Outlier cleaning
    outlier_indices = set()
    for var, target in [("Solar_Radiation", "SR"), ("Wind_Speed_100m", "WIND")]:
        outliers = dataRESGenerationCleaning(df, var, target, quantile_clip=0.9)
        outlier_indices.update(outliers.index.tolist())
    df_cleaned = df.drop(index=outlier_indices)

    # Run tuning
    best_params_sr = run_optimization(df_cleaned, techno="SR", n_trials=50)
    best_params_wind = run_optimization(df_cleaned, techno="WIND", n_trials=50)