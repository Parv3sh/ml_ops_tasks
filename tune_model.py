import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import optuna

# Define objective function
def objective(trial):
    # Load dataset
    data_url = "http://lib.stat.cmu.edu/datasets/boston"
    raw_df = pd.read_csv(data_url, sep='\s+', skiprows=22, header=None)
    data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
    target = raw_df.values[1::2, 2]

    X = pd.DataFrame(data)
    y = pd.Series(target)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Hyperparameters
    n_estimators = trial.suggest_int('n_estimators', 100, 200)
    max_depth = trial.suggest_int('max_depth', 10, 20)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 5)
    min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 2)

    # Model
    model = RandomForestRegressor(
        n_estimators=n_estimators, 
        max_depth=max_depth, 
        min_samples_split=min_samples_split, 
        min_samples_leaf=min_samples_leaf,
        random_state=42
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)

    return mse

if __name__ == '__main__':
    db_url = 'postgresql://user:password@postgres/optuna'
    study = optuna.create_study(study_name='optuna_study', direction='minimize', storage=db_url, load_if_exists=True)
    study.optimize(objective, n_trials=100, n_jobs=-1)
    print(f"Best trial: {study.best_trial.value}")
    print(f"Best params: {study.best_trial.params}")
    study.trials_dataframe().to_csv('./results/optuna_trials.csv')  # Save study as CSV
    optuna.visualization.plot_optimization_history(study).write_html('./results/optuna_optimization_history.html')
