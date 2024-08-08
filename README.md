# Flask API Project

This project implements a basic Flask API in Python with the following functionalities:

1. An endpoint /hello that accepts a POST request with JSON containing a name field and returns a JSON response with a greeting message.
2. An endpoint /list that accepts a POST request and returns a JSON response containing all names and timestamps stored in a MySQL database.

## Additional features include:

- A Dockerfile to create a container for the application served on port 8080.

- A docker-compose setup with separate containers for the API and the database.

- A multi-stage Docker build for the Python container to minimize vulnerabilities.

- An Nginx setup in front of the Flask API, configured to accept only POST requests with appropriate security measures.

- Kubernetes deployment and service declarations for the application.

## Docker Setup

### Dockerfile
The Dockerfile is used to create a Docker image for the Flask application.

### Dockerfile.Nginx
The Dockerfile.Nginx is used to create a Docker image for the Nginx server.

### nginx.conf
The nginx.conf file contains the configuration for Nginx to proxy requests to the Flask application and enforce security measures.

### docker-compose.yml
The docker-compose.yml file is used to set up and run multi-container Docker applications. It defines three services: web, db, and nginx

## Running the Application

1. Build and start the Docker containers:
~~~
docker-compose up --build
~~~
2. Access the Flask API at 'http://localhost:8080'.

## Usage
### Endpoints

- POST /hello
  - Request:
~~~
   {
  "name": "Your Name"
   }
~~~

   - -  Response:
~~~
 {
  "message": "Hello, Your Name!"
 }
~~~

- POST /list
  - Response:

~~~
  [
  {
    "name": "Name1",
    "timestamp": "2024-07-28T12:34:56"
  },
  {
    "name": "Name2",
    "timestamp": "2024-07-28T12:35:56"
  }
]
~~~

## Vulnerability Scanning

To ensure that the Python container does not contain any CRITICAL or HIGH vulnerabilities, use Docker Scout:
~~~
docker scout cves junior-test-web --format packages --output scan_report.txt
~~~
The report will be saved in a file called 'scan_report.txt'.

## Kubernetes Setup
Instead of using docker-compose, the project includes Kubernetes deployment and service declarations to manage the application. These files are located in the kubernetes folder. The setup includes:

- Deployments for the Flask application and MySQL database.
- Service declarations to expose the Flask application and database.
- Usage of the junior-test namespace.

### Setup Instructions

1. Navigate to the folder containing the Kubernetes configuration files and create the Namespace:
~~~
kubectl create namespace junior-test
~~~

2. Deploy the MySQL Database:
~~~
kubectl apply -f db-deployment.yaml
kubectl apply -f db-service.yaml
~~~

3. Deploy the Flask Application:
~~~
kubectl apply -f web-deployment.yaml
kubectl apply -f web-service.yaml
~~~

4. Deploy Nginx:
~~~
kubectl apply -f nginx-deployment.yaml
kubectl apply -f nginx-service.yaml
~~~
5. Verify the Deployment:
~~~
kubectl get pods -n junior-test
~~~
   
6. Access the Flask Application:
To access the Flask application locally, use port forwarding:

~~~
kubectl port-forward -n junior-test service/web 8080:8080
~~~

The Flask application should now be accessible at http://localhost:8080, using the same endpoints as in the previous Docker setup.

## Considerations

- **Kubernetes Setup**: Ensure Docker Desktop with Kubernetes is set up before proceeding with the project deployment on Kubernetes.

- **Port Conflicts**: Be aware that Docker Compose and Kubernetes deployments should not run simultaneously, as there may be issues related to port usage. Make sure to stop one before starting the other to avoid conflicts.

