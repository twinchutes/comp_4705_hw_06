import json
import requests
from sklearn.metrics import accuracy_score

# Constants

def load_test_data(path):
    with open(path, "r") as f:
        return json.load(f)

def get_prediction(text, url):
    response = requests.post(url, json={"body": text})
    if response.status_code == 200:
        return response.json().get("prediction")
    else:
        print(f"Error {response.text}")
        return None

def evaluate(test_path, url):
    test_data = load_test_data(test_path)
    y_true = []
    y_pred = []

    for i, item in enumerate(test_data, start=1):
        text = item["text"]
        true_label = item["true_label"]
        predicted_label = get_prediction(text, url)

        if predicted_label is not None:
            y_true.append(true_label.lower())
            y_pred.append(predicted_label.lower())

    accuracy = accuracy_score(y_true, y_pred)
    print(f"Final Accuracy: {accuracy}")

if __name__ == "__main__":
    url = "http://127.0.0.1/predict"
    evaluate('test.json', url)