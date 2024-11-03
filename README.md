# ML Ops Tasks

## Overview
This project demonstrates the setup of a CI/CD pipeline for machine learning model deployment using Kubernetes. I cover training a model, setting up a CI/CD pipeline, and deploying the model to production.

## Project Structure
- .github/workflows - for defining GitHub Actions CI/CD pipeline
- results: stores best model that is used for training, visualisation of reducing mse / increasing accuracy, and history of all trials and results
- tests
- app.py is used for deploying the best model
- deployment.yaml defines the api service with 3 replicas that can be hit to get the predictions
- Dockerfiles for training and deploying respectively
- training job yaml for training and parallel hyperparameter tunning
- postgres deployment was needed so that multiple pods could share the same memory and can understand it as a single study instead of separately training same model over and over. tried sqlite first, but the paralle write was creating issue hence used a faster db
- requirements files for train and deploy respectively
- tune model for the actual logic of training and tunning

## Reproducing the Pipelines

### 0. Basics
- Basic understanding of linux, shell, git, brew and other tools is expected
- For this project I used the locally hosted setup of kubernetes which completely supports kubectl. And for the deployments in EKS, or GKE etc, only minimum items are to be changed in the yaml configuration such as removing the image never pull option
- I have strived to use best practices to train, deploy this model. Yet a lot could be optimised and improved
- Boston dataset has inherent ethical issue but for the sake of this project, we've proceeded to utilise it with suggested means

### 1. Environment Setup
- **Minikube**: Ensure you have Minikube installed and running for local Kubernetes testing.
- **Docker**: Docker is required for building and managing container images.

### 2. Create a Repository
- For the purpose of this project, a new repository was created

### 3. Run the Model Training
Mount the Project Directory: mounting to see the output results with ease of access

```bash
minikube mount /path/to/project:/mnt/data
```

Deploy PostgreSQL: Apply the PostgreSQL deployment YAML.
```bash
kubectl apply -f postgres-deployment.yaml
```
Train the Model: Build the Docker image and apply the training job.
```bash
docker build -f Dockerfile.train -t model-training:latest .
kubectl apply -f optuna_tuning_job.yaml
```
### 4. Deploy the Best Model
Build Deployment Image: Ensure the model file is in the expected directory, then build the Docker image.

```bash
docker build -f Dockerfile.deploy -t best-model-api:latest .
```
Deploy to Kubernetes: Apply the deployment and service YAML files.

```bash
kubectl apply -f deployment.yaml
```
Access the Service: Use port forwarding to access the API locally.

```bash
kubectl port-forward deployment/best-model-api 8080:5000
```
Test the API: Send a test request to the API. e.g.,

```bash
curl -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d '{"data": [[0.00632, 18.0, 2.31, 0.0, 0.538, 6.575, 65.2, 4.0900, 1.0, 296.0, 15.3, 396.90, 6]]}'
```
### CI/CD Pipeline
Setting Up the Pipeline
- GitHub Actions: The CI/CD pipeline is configured using GitHub Actions. It runs tests, builds Docker images, and pushes them to GitHub Packages.

- Environment Variables: Ensure you have a personal access token (PAT) with write:packages scope added as a secret (GHCR_PAT) in your GitHub repository settings.

Workflow
1. Run Tests: Automatically triggered on pushing code to the repository. Runs the model tests to validate changes.

2. Build and Push Docker Image: Builds the Docker image and pushes it to GitHub Packages if tests pass.

Recreate the Pipeline
1. Clone the Repository: Clone your repository to your local machine.

    ```bash
    git clone <repository-url>
    ```
2. Set Up GitHub Actions: Add the workflow file in .github/workflows/ directory of your repository.

3. Add Secrets: Add the PAT (GHCR_PAT) in your repository settings under Secrets.

4. Commit and Push: Push your changes to trigger the CI/CD pipeline.


## Deployment at:
https://ghcr.io/parv3sh/parv3sh/ml_ops_tasks/best-model-api


## Results
To check the result either open the html in any browser, or open the csv file.

## Demo snippets in the results folder

-- Thank You

-- Parvesh
