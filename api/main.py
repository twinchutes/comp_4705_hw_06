import joblib
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import os
import time
import json
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class text_input_c(BaseModel):
    body: str

app = FastAPI(
    title='Movie Review Sentiment Prediction API'
)

def load_model():
    '''Loads the pre-trained model and target names.'''
    try:
        model = joblib.load('model.pkl')
        print('Model loaded successfully.')
    except FileNotFoundError:
        print('Error: Model file "model.pkl" not found.')
        print('Please run the "train.py" script first to generate the model file.')
    return model

model = load_model()

@app.on_event('startup')
def startup_event():
    '''A startup event handler. Checks if the model was loaded correctly, if not prints a persistent warning.'''
    if model is None:
        print('WARNING: Model is not loaded. Prediction endpoints will not work.')
    os.mkdir('logs')

@app.get('/health_check')
def health_check():
    '''
    Health Check Endpoint
    This endpoing is used to verify that the API server is running and responsive.
    '''
    return {"status": "ok", "message": "API is running"}

@app.post("/predict")
def predict(text_input: text_input_c):
    """
    Prediction Endpoint
    Takes a movie review string returns a binary prediction (0 or 1).
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Cannot make predictions."
        )

    prediction = model.predict([text_input.body])
    timestamp = time.time()
    request_text = text_input.body
    true_sentiment = None

    log_record = {
        "timestamp": timestamp,
        "request_text": request_text,
        "predicted_sentiment": prediction[0],
        'true_sentiment': true_sentiment
    }

    with open("logs/predictions.json", "a") as f:
        x = json.dumps(log_record)
        f.write(x + "\n")

    return {"prediction": prediction[0]}

@app.post("/predict_proba")
def predict_with_probability(text_input: text_input_c):
    """
    Prediction with Probability Endpoint
    Takes a movie review string and returns the prediction along with the
    probabilities for each class (0 and 1).
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Cannot make predictions."
        )

    probabilities = model.predict_proba([text_input.body])
    prediction = model.predict([text_input.body])

    # The probabilities for class 0 and class 1
    prob_class_0 = probabilities[0][0]
    prob_class_1 = probabilities[0][1]
    
    return {
        "prediction": prediction[0],
        "probability_negative": f"{prob_class_0:.4f}",
        "probability_positive": f"{prob_class_1:.4f}"
    }

@app.get("/example")
def get_training_example():
    '''
    Get a training example from the original dataset.
    Returns the training example review, along with a prediction and probabilities.
    '''
    df = pd.read_csv('IMDB Dataset.csv')
    sample = df.sample(1)
    sample_input = sample['review'].iloc[0]
    text_obj = text_input_c(body=sample_input)
    target = sample['sentiment'].iloc[0]
    prediction = predict_with_probability(text_obj)
    return {
        "review": sample_input,
        "target": target,
        "response": prediction
    }

@app.get("/predictions")
def get_predictions():
    return FileResponse("logs/predictions.json", media_type="application/json")