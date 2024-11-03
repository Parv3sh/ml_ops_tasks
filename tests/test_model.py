import joblib
import pandas as pd

def test_model_loading():
    model = joblib.load('results/best_model.pkl')
    assert model is not None

def test_model_prediction():
    model = joblib.load('results/best_model.pkl')
    data = [[0.00632, 18.0, 2.31, 0.0, 0.538, 6.575, 65.2, 4.0900, 1.0, 296.0, 15.3, 396.90, 4.98]]
    df = pd.DataFrame(data)
    predictions = model.predict(df)
    assert len(predictions) == 1
