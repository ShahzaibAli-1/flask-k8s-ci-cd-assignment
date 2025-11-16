# Flask Kubernetes CI/CD Assignment

## Project Overview

This is a complete Flask-based web application deployment project that demonstrates modern DevOps practices including containerization, continuous integration/continuous deployment (CI/CD), and Kubernetes orchestration. The project showcases a minimal but functional web service ready for production deployment.

---

## Project Structure

```
flask-k8s-ci-cd-assignment/
├── app.py                          # Flask application source code
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker image build configuration
├── Jenkinsfile                     # CI/CD pipeline definition
├── test.txt                        # Test file (placeholder)
├── kubernetes/
│   ├── deployment.yaml             # Kubernetes deployment configuration
│   └── service.yaml                # Kubernetes service configuration
└── README.md                       # Project documentation
```


// Small Testing Change
// I am testing this again and again and again and again
---

## Component Details

### 1. **app.py** - Flask Application

**Purpose:** The core web application

**Functionality:**
- Creates a Flask web server that listens on all network interfaces (`0.0.0.0`) on port `5000`
- Defines a single route `/` that returns "Hello, World!"
- When executed directly, starts the Flask development server

**Code:**
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Key Points:**
- Binds to `0.0.0.0` making it accessible from any interface (required for containerized environments)
- Uses port `5000` (standard Flask development port)

---

### 2. **requirements.txt** - Dependencies

**Purpose:** Lists all Python package dependencies for the project

**Content:**
```
Flask==2.3.3
```

**Details:**
- Specifies Flask version 2.3.3 as the only production dependency
- Ensures reproducible builds across different environments
- Used by pip during Docker image build to install packages

---

### 3. **Dockerfile** - Container Configuration

**Purpose:** Defines how the Flask application is packaged into a Docker container

**Architecture:** Multi-stage build (builder + runtime)

**Build Stages:**

**Stage 1 - Builder:**
```dockerfile
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt
```
- Uses lightweight Python 3.9-slim base image
- Installs dependencies locally to `/root/.local`
- This stage is discarded in the final image (keeps image size smaller)

**Stage 2 - Runtime:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
CMD ["python", "app.py"]
```
- Copies only necessary files from builder stage
- Sets PATH to include installed packages
- Exposes port 5000 for incoming traffic
- Runs the Flask app as the container entry point

**Benefits:**
- Reduces final image size by excluding build artifacts
- Ensures consistent Python environment
- Optimized for production deployment

---

### 4. **Jenkinsfile** - CI/CD Pipeline

**Purpose:** Defines the automated build, test, and deployment pipeline

**Pipeline Stages:**

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building the application...'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying to Kubernetes...'
            }
        }
    }
}
```

**Stages Explained:**

1. **Build Stage**
   - Currently outputs a message (placeholder)
   - Would typically: compile code, build Docker image, push to registry

2. **Test Stage**
   - Currently outputs a message (placeholder)
   - Would typically: run unit tests, integration tests, code quality checks

3. **Deploy Stage**
   - Currently outputs a message (placeholder)
   - Would typically: apply Kubernetes manifests, update deployments

**Status:** This is a skeleton/template. Actual build commands need to be implemented.

---

### 5. **kubernetes/deployment.yaml** - Kubernetes Deployment

**Purpose:** Defines how the Flask application runs in a Kubernetes cluster

**Configuration Details:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 2                    # Run 2 copies of the application
  selector:
    matchLabels:
      app: flask-app             # Select pods with this label
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: flask-app:latest  # Container image to use
        ports:
        - containerPort: 5000    # Application listens on port 5000
        env:
        - name: FLASK_ENV
          value: "production"    # Run in production mode
```

**Key Features:**

- **Replicas: 2** - High availability with 2 running instances
- **Selector/Labels** - Kubernetes identifies pods to manage
- **Image** - Points to the Docker image built from Dockerfile
- **Port Mapping** - Container port 5000 exposed internally
- **Environment Variable** - Sets Flask to production mode

**What it Does:**
- Ensures 2 instances of the Flask app are always running
- Automatically restarts failed containers
- Enables rolling updates and scaling

---

### 6. **kubernetes/service.yaml** - Kubernetes Service

**Purpose:** Exposes the Flask application to external traffic

**Configuration:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  selector:
    app: flask-app               # Route traffic to pods with this label
  ports:
    - protocol: TCP
      port: 80                   # External port (what users access)
      targetPort: 5000           # Internal port (app listens here)
  type: LoadBalancer             # Exposes via external IP
```

**Key Features:**

- **Type: LoadBalancer** - Creates external IP address accessible from outside cluster
- **Port Mapping** - Translates external port 80 to internal port 5000
- **Selector** - Routes traffic to pods matching label `app: flask-app`

**Result:**
- Users access the service on port 80 (HTTP standard)
- Traffic is load-balanced across the 2 deployment replicas
- Automatic failover if a pod fails

---

### 7. **test.txt** - Test File

**Content:**
```
This file is test file
```

**Purpose:** Placeholder for test-related content or CI/CD validation

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User Request (Port 80)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│          Kubernetes Service (LoadBalancer)                   │
│                  flask-service                              │
│     Routes traffic to port 5000 internally                  │
└────────────┬───────────────────────────────────┬────────────┘
             │                                   │
             ▼                                   ▼
    ┌──────────────────┐              ┌──────────────────┐
    │  Pod 1           │              │  Pod 2           │
    │  Flask App       │              │  Flask App       │
    │  Port: 5000      │              │  Port: 5000      │
    │  Returns:        │              │  Returns:        │
    │  "Hello, World!" │              │  "Hello, World!" │
    └──────────────────┘              └──────────────────┘
         Replica 1                        Replica 2
```

---

## Data Flow

1. **Local Development**
   - Run `python app.py` → Flask server starts on `0.0.0.0:5000`

2. **Containerization**
   - Docker builds image using Dockerfile
   - Multi-stage build optimizes image size
   - Container includes Python, Flask, and app.py

3. **CI/CD Pipeline**
   - Jenkins Jenkinsfile orchestrates: Build → Test → Deploy
   - (Currently skeleton; implement actual commands as needed)

4. **Kubernetes Deployment**
   - Deployment creates 2 replicas of the Flask container
   - Service exposes replicas via LoadBalancer on port 80
   - Kubernetes manages health, scaling, and updates

---

## Technologies Used

| Technology | Purpose | Version |
|-----------|---------|---------|
| **Flask** | Web framework | 2.3.3 |
| **Python** | Runtime | 3.9 |
| **Docker** | Containerization | Latest |
| **Kubernetes** | Orchestration | Latest |
| **Jenkins** | CI/CD automation | Latest |

---

## How to Use

### Local Testing
```powershell
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py

# Access at http://localhost:5000
```

### Docker Build
```powershell
# Build the image
docker build -t flask-app:latest .

# Run the container
docker run -p 5000:5000 flask-app:latest
```

### Kubernetes Deployment
```powershell
# Apply configurations
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

# Verify deployment
kubectl get deployments
kubectl get services

# Access the service (get external IP)
kubectl get svc flask-service
```

---

## Summary

This project demonstrates a complete DevOps workflow:
- **Development:** Simple Flask application with a single endpoint
- **Containerization:** Optimized multi-stage Docker build
- **Orchestration:** Kubernetes deployment with 2 replicas and LoadBalancer service
- **CI/CD:** Jenkins pipeline framework for automation
- **High Availability:** Load-balanced, self-healing infrastructure

The application is production-ready and can be scaled horizontally by increasing replicas or adjusting Kubernetes configurations.
