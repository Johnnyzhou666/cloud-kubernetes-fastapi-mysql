# ECE 9016 Cloud Computing Project: High Availability Web Deployment on GCP

## Project Overview

This project demonstrates the deployment of a containerized web application with a database backend using Kubernetes on Google Cloud Platform (GCP). The main objective of this project is to design, deploy, and verify a cloud-based web application that supports both a development environment and a production environment with high availability.

The application is built with Python Flask and MySQL. It performs basic read operations from the database and displays the retrieved data through a web interface. Kubernetes is used to manage container deployment, service discovery, load balancing, and pod scheduling.

---

## Technologies Used

- Google Cloud Platform (GCP)
- Google Kubernetes Engine (GKE)
- Kubernetes
- Docker
- Python
- Flask
- MySQL
- YAML
- gcloud CLI
- kubectl

---

## System Architecture

### Development Environment

The development environment is designed for testing and debugging on a simplified single-node setup.

- One worker node is used.
- The web application pod and database pod run in the same environment.
- The web application communicates with the MySQL database through an internal Kubernetes service.
- This environment is mainly used to verify basic application functionality before production deployment.

### Production Environment

The production environment is designed to support high availability and improved fault tolerance.

- Worker Node 1 hosts one web application pod.
- Worker Node 2 hosts another web application pod.
- Worker Node 3 is dedicated to the MySQL database pod.
- A Kubernetes LoadBalancer service distributes incoming traffic across the web application pods.
- Kubernetes pod anti-affinity is used to prevent the two web application pods from being scheduled on the same node.
- This design allows the application to remain accessible even if one web pod fails.

---

## Repository Structure

```text
.
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── database/
│   └── init.sql
│
├── k8s-dev/
│   └── dev-deployment.yaml
│
├── k8s-prod/
│   ├── prod-deployment.yaml
│   └── prod-services.yaml
│
└── README.md
```

---

## File Descriptions

### `app/app.py`

Contains the Python Flask web application. The application connects to the MySQL database, retrieves data, and displays the results through a simple web page.

### `app/requirements.txt`

Lists the Python dependencies required to run the Flask application.

### `app/Dockerfile`

Defines the container image for the Flask web application.

### `database/init.sql`

Contains the SQL script used to initialize the MySQL database, including table creation and sample data insertion.

### `k8s-dev/dev-deployment.yaml`

Contains the Kubernetes configuration for the development environment.

### `k8s-prod/prod-deployment.yaml`

Contains the Kubernetes deployment configuration for the production environment, including web application replicas, database deployment, node scheduling, and pod anti-affinity settings.

### `k8s-prod/prod-services.yaml`

Contains the Kubernetes service configuration, including the LoadBalancer service for external access and the internal service for database communication.

---

## Deployment Guide

### Prerequisites

Before deploying this project, make sure the following tools are installed and configured:

- Google Cloud Platform account
- Google Cloud SDK
- kubectl
- Docker
- Access to a GKE cluster

---

## Step 1: Create a GKE Cluster

Create a Kubernetes cluster with at least three nodes to support the production high-availability setup.

```bash
gcloud container clusters create cloud-project-cluster \
  --num-nodes=3 \
  --zone=us-central1-a
```

After the cluster is created, connect kubectl to the cluster:

```bash
gcloud container clusters get-credentials cloud-project-cluster \
  --zone=us-central1-a
```

Verify that the nodes are available:

```bash
kubectl get nodes
```

---

## Step 2: Label Kubernetes Nodes

Label the three worker nodes so that Kubernetes can schedule the web application pods and database pod to the correct nodes.

```bash
kubectl get nodes
```

Replace the node names below with your actual node names:

```bash
kubectl label nodes <node-1-name> env=web-node-1
kubectl label nodes <node-2-name> env=web-node-2
kubectl label nodes <node-3-name> env=db-node
```

Verify the labels:

```bash
kubectl get nodes --show-labels
```

---

## Step 3: Build the Docker Image

Set your GCP project ID:

```bash
export PROJECT_ID="your-gcp-project-id"
```

Build the Docker image for the Flask web application:

```bash
docker build -t gcr.io/$PROJECT_ID/flask-mysql-app:v1 ./app
```

---

## Step 4: Push the Docker Image to GCP

Push the image to Google Container Registry:

```bash
docker push gcr.io/$PROJECT_ID/flask-mysql-app:v1
```

Before applying the Kubernetes YAML files, make sure the image field in the deployment file uses your correct project ID.

Example:

```yaml
image: gcr.io/your-gcp-project-id/flask-mysql-app:v1
```

---

## Step 5: Create the Database ConfigMap

Create a Kubernetes ConfigMap from the SQL initialization script:

```bash
kubectl create configmap mysql-init-script --from-file=./database/init.sql
```

This ConfigMap allows the MySQL container to initialize the database when the pod is created.

---

## Step 6: Deploy the Development Environment

To deploy the development environment, run:

```bash
kubectl apply -f ./k8s-dev/dev-deployment.yaml
```

Check the status of the pods:

```bash
kubectl get pods -o wide
```

---

## Step 7: Deploy the Production Environment

Deploy the production Kubernetes resources:

```bash
kubectl apply -f ./k8s-prod/prod-deployment.yaml
kubectl apply -f ./k8s-prod/prod-services.yaml
```

Check whether all pods are running:

```bash
kubectl get pods -o wide
```

The web application pods should be scheduled on different worker nodes, while the database pod should be scheduled on the dedicated database node.

---

## Step 8: Access the Web Application

Check the Kubernetes services:

```bash
kubectl get services
```

Find the external IP address of the LoadBalancer service.

Open the application in a web browser:

```text
http://<EXTERNAL-IP>
```

The application should display data retrieved from the MySQL database.

---

## High Availability Verification

To verify high availability, first confirm that multiple web application pods are running:

```bash
kubectl get pods -o wide
```

Then delete one web application pod:

```bash
kubectl delete pod <web-pod-name>
```

After deleting one pod, refresh the web application in the browser using the LoadBalancer external IP.

The application should remain accessible because the LoadBalancer redirects traffic to the remaining running web pod. Kubernetes will also automatically create a replacement pod to restore the desired number of replicas.

Check the pod recovery process:

```bash
kubectl get pods -o wide
```

---

## Useful Kubernetes Commands

Check all pods:

```bash
kubectl get pods
```

Check pods with node placement:

```bash
kubectl get pods -o wide
```

Check services:

```bash
kubectl get services
```

Check deployments:

```bash
kubectl get deployments
```

Describe a pod:

```bash
kubectl describe pod <pod-name>
```

Check pod logs:

```bash
kubectl logs <pod-name>
```

Delete a pod:

```bash
kubectl delete pod <pod-name>
```

---

## Key Learning Outcomes

Through this project, I gained practical experience in:

- Deploying containerized applications on Google Kubernetes Engine
- Building and pushing Docker images to Google Cloud
- Writing Kubernetes deployment and service YAML files
- Configuring a Flask application to communicate with a MySQL database
- Using Kubernetes services for internal and external communication
- Applying node labels and pod scheduling rules
- Designing a high-availability architecture using multiple web replicas
- Verifying fault tolerance through pod deletion and automatic recovery

---

## Conclusion

This project demonstrates how cloud infrastructure, containerization, and Kubernetes orchestration can be combined to deploy a scalable and highly available web application. The development environment provides a simplified setup for testing, while the production environment uses multiple worker nodes, load balancing, and pod anti-affinity to improve reliability and availability.

By separating the web application and database across different nodes and using a LoadBalancer service, the system can continue serving users even when one web application pod fails. This project provides a practical example of deploying and managing cloud-native applications on GCP.
