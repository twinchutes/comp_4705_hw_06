# comp_4705_hw_05
Assignment 5 for COMP 4705


Installation directions
* Gitclone the repo
* Install requirements

Makefile use:
* Start WSL2 from CMD
* To mount Google Drive folder if it's not already mounted:
* $ sudo mount -t drvfs H: /mnt/h
* Navigate to folder in WSL2
*  build the container with Docker
* $ make build
* run the app on localhost
* $ make run
* Navigate to http://localhost:8501/
* click analyze to analyze the results
* $ make clean - delete the image and network when you're finished

Postman use:
In Postman:
Healthcheck: GET request to http://127.0.0.1/health_check
Predict: POST request to http://127.0.0.1/predict.
Example predict request: http://127.0.0.1/predict
{
    "body": "this movie is amazing!"
}
Example output: 
{
    "prediction": "positive"
}

Predict with probability: POST request to http://127.0.0.1/predict_proba
Example predict_proba request: http://127.0.0.1/predict_proba
{
    "body": "this movie is amazing!"
}
Example output:
{
    "prediction": "positive",
    "probability_negative": "0.2259",
    "probability_positive": "0.7741"
}

Get examples: GET request to http://127.0.0.1/example
No parameters needed. Returns a random review along with its target sentiment, and a json example of the model's predict_proba output.
Example:
{
    "review": "Two movies back to back which dealt with Indian POWs; Veer Zaara and Deewaar. Although Veer Zara was a love story of a guy who gives everything up for someone, Deewaar focuses on the main subject itself. It is not hidden that many Indian POWs are rotting in Pakistani Jails for years - for whom neither Indian Govt. has time or sympathy nor the other side. I'm sure some of Pakistani POWs are in India as well, but let's focus on the movie. Full of actors. Some were stage actors like Raghubir Yadav, Rajendra Gupta, etc. Amitabh Bachchan who plays the role of a Major, acted well. Akshaye Khanna did his part well. There was nothing for Amrita Rao to do than a few giggles and couple songs. I think Sanjay Dutt's role was most solid even though it wasn't too long. He acted really well here and his dialog delivery was also impressive. If you compare it to LOC, which was nothing but a day long movie with story going in all directions (if it HAD a story) - Deewaar is a well directed movie that keeps a good pace and does justice to all actors. 7.5/10",
    "target": "positive",
    "response": {
        "prediction": "positive",
        "probability_negative": "0.3871",
        "probability_positive": "0.6129"
    }
}

get prediction logs via http://127.0.0.1/predictions


To test performance, run evaluate.py on your host machine.