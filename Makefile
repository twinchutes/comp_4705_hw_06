FASTAPI_IMAGE := fastapi-app
STREAMLIT_IMAGE := streamlit-app
FASTAPI_DOCKERFILE := api/Dockerfile
STREAMLIT_DOCKERFILE := monitoring/Dockerfile

build:
	@echo "Building Docker api image: $(FASTAPI_IMAGE)"
	docker build -f $(FASTAPI_DOCKERFILE) -t $(FASTAPI_IMAGE) api
	@echo "Building Docker streamlit image: $(STREAMLIT_IMAGE)"
	docker build -f $(STREAMLIT_DOCKERFILE) -t $(STREAMLIT_IMAGE) monitoring
	@echo "Creating network"
	docker network create app-network

run:
	@echo "Running Docker api container..."
	docker run -d --rm --name fastapi-container --network app-network -p 8000:8000 $(FASTAPI_IMAGE)
	@echo "Running Docker streamlit container..."
	docker run -d --rm --name streamlit-container --network app-network -p 8501:8501 $(STREAMLIT_IMAGE)

clean:
	@echo "Stopping and removing FastAPI container..."
	docker stop fastapi-container || true
	docker rm fastapi-container || true
	@echo "Stopping and removing Streamlit container..."
	docker stop streamlit-container || true
	docker rm streamlit-container || true
	@echo "Removing Docker images..."
	docker rmi $(FASTAPI_IMAGE) || true
	docker rmi $(STREAMLIT_IMAGE) || true
	@echo "Removing network app-network"
	docker network rm app-network

# Can include -v for volume. Went over this in lecture 2. Whichever director youyo'ure working on gets mounted to the docker container. So if you make a change to the log file it gets modified docker
# app folder 