# Update packages and install Docker
sudo apt-get update -y
sudo apt-get install docker.io -y

# Start and enable Docker so it runs on boot
sudo systemctl start docker
sudo systemctl enable docker

# Add the 'ubuntu' user to the docker group
sudo usermod -aG docker ubuntu

# Log out and log back in to apply the group changes
exit