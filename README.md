# comp_4705_hw_06

Assignment 6 for COMP 4705

# GitHub Actions Use

From CLI:
* git commit -a -m 'input message'
* git push
This will push the changes to the dev branch.

From github.com
* click merge & pull request to merge it from dev to main.
* wait for actions to complete their checks.
* if the checks are successful the changes will be merged to main.

# AWS Instructions
Download and install putty  
Create the EC2 instance:
    1. Launch and Configure EC2 Instance:
        ○ Launch a new t2.micro EC2 instance with Ubuntu.
        Create a new key *during* the EC2 instance creation and save it
        ○ Configure its Security Group to allow incoming traffic on:
            § Port 22 (SSH) from your IP address for access.
            § Port 8000 (FastAPI) from anywhere (Custom TCP)
            § Port 8501 (Streamlit) from anywhere (Custom TCP)
        ○ Connect to your EC2 instance using SSH.
    2. Set up the Server Environment:
        ○ On the EC2 instance, install Docker and Git.
    3. Deploy the Application:
        ○ Clone your GitHub repository onto the EC2 instance.
        ○ Create a shared Docker volume for the logs.
        ○ Build the Docker images for both the api and monitoring services.
Run both containers in detached mode (-d), ensuring they are connected to the shared volume.

For EC2 SSH access
Download putty
Create a new key *during* the EC2 instance creation
Download it to a directory
Right click them pem file and open with puttygen.exe
Click save private key in the same directory as the pem
Open putty.exe
Copy the public ipv4 address into the Host Name field in putty
In putty, Under Connection>SSH>Auth>Credentials in the "Private key file for authentication" click browse and open the ppk
In putty, under Window>Appearance, increase the font size.
In putty, Under Session, save this session
In putty, click open
In the putty cli, the username is "ubuntu". 
Run each of the following commands:
# Update packages and install Docker
sudo apt-get update -y
sudo apt-get install docker.io -y

# Start and enable Docker so it runs on boot
sudo systemctl start docker
sudo systemctl enable docker

# Add the 'ubuntu' user to the docker group
sudo usermod -aG docker ubuntu

# Log out and log back in to apply the group changes


Still in the putty cli, run:
git --version (to confirm git is installed)
git clone https://github.com/twinchutes/comp_4705_hw_06.git
sudo apt install make
sudo apt install make-doc
cd comp_4705_hw_06
sudo make build
sudo make run

If the instance times out or if you close putty, you must create a new ppk file.

Dashboard will be located at ipv4address:8501, ie http://18.213.2.212:8501/ (it takes a long time to open in micro t2)
In postman, make calls to ipv4address, for example, make a post request to:

http://18.213.2.212:8000/predict
with the body
{
    "body": "what an incredible movie"
}

The dashboard will only load once at least one call has been amde, so be sure to make a call to /predict prior to loading the dashboard.

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

