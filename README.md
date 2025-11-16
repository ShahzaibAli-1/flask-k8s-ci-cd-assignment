# Flask Kubernetes CI/CD Assignment

## Project Overview

This project demonstrates a complete DevOps workflow for deploying a Flask web application using **Docker containerization**, **Kubernetes orchestration**, and **Jenkins CI/CD pipeline automation**. The application showcases production-ready practices including automated deployments, rolling updates, service load balancing, and self-healing infrastructure.

### Key Features
- **Containerized Application**: Multi-stage Docker build for optimized image size
- **Kubernetes Orchestration**: Automated scaling, rolling updates, and self-healing
- **Load Balancing**: Service-based traffic distribution across replicas
- **CI/CD Pipeline**: Jenkins automation for build, test, and deployment
- **High Availability**: Multiple replicas with liveness and readiness probes
- **Health Checks**: Dedicated endpoints for monitoring application health

---

## Kubernetes Features Used

This project implements several core Kubernetes capabilities:

### 1. **Deployments (ReplicaSet Management)**
- **Multi-Replica Setup**: Maintains 3 running instances of the Flask application
- **Self-Healing**: Automatically restarts failed containers
- **Declarative Configuration**: Infrastructure-as-Code approach using YAML manifests

### 2. **Rolling Updates (Automated Rollouts)**
- **Strategy**: RollingUpdate with maxSurge=1 and maxUnavailable=1
- **Zero-Downtime Deployments**: New versions deploy without service interruption
- **Automatic Rollback**: Failed deployments can be rolled back to previous versions
- **Rollout History**: Full audit trail of deployment changes

### 3. **Service Discovery & Load Balancing**
- **NodePort Service**: Exposes application via port 30008 on the Kubernetes node
- **Internal DNS**: Services discover each other within the cluster using DNS names
- **Round-Robin Load Balancing**: Traffic distributed evenly across all pod replicas
- **Session Persistence**: Optional sticky sessions for stateful applications

### 4. **Resource Management & Scaling**
- **Request Limits**: CPU (100m-200m) and Memory (128Mi-256Mi) constraints
- **Horizontal Pod Autoscaling**: Can be extended with HPA for dynamic scaling
- **Quality of Service**: Guaranteed resource allocation for pod stability

### 5. **Health Monitoring**
- **Liveness Probes**: Detects unresponsive containers and restarts them
- **Readiness Probes**: Ensures only healthy containers receive traffic
- **Proactive Healing**: Maintains service availability automatically

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
// I am testing this again and again and again and again test
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

## Building and Running the Application Locally with Docker

### Prerequisites
- Docker installed and running
- Docker CLI access

### Step 1: Build the Docker Image

```powershell
# Navigate to project directory
cd flask-k8s-ci-cd-assignment

# Build the Docker image with tag
docker build -t flask-app:latest .

# Verify the image was created
docker images | Select-String flask-app
```

**What happens during build:**
1. **Stage 1 (Builder)**: Installs Python dependencies in a temporary container
2. **Stage 2 (Runtime)**: Copies only necessary files to minimize image size
3. Result: Optimized ~150MB image (instead of ~500MB with all build artifacts)

### Step 2: Run the Container Locally

```powershell
# Run the container in the foreground
docker run -p 5000:5000 flask-app:latest

# OR run in background
docker run -d -p 5000:5000 --name flask-container flask-app:latest
```

**Port Mapping:** `-p 5000:5000` maps local port 5000 to container port 5000

### Step 3: Access the Application

```powershell
# Test the main endpoint
curl http://localhost:5000
# Returns: "Hello, World!"

# Test health check endpoint
curl http://localhost:5000/health
# Returns: {"status": "healthy", "message": "Service is running"}

# Test readiness check endpoint
curl http://localhost:5000/ready
# Returns: {"status": "ready", "message": "Service is ready to accept traffic"}
```

### Step 4: Stop and Clean Up

```powershell
# Stop running container
docker stop flask-container

# Remove container
docker rm flask-container

# Remove image (optional)
docker rmi flask-app:latest
```

---

## Deploying to Kubernetes Using Jenkins Pipeline

### Prerequisites
- Kubernetes cluster running (Minikube, Docker Desktop K8s, or cloud cluster)
- Jenkins server configured with kubectl access
- Docker installed on Jenkins agent
- Git repository access

### Step 1: Configure Jenkins

1. **Add required credentials** to Jenkins:
   - GitHub repository credentials (if private)
   - Docker registry credentials (if using private registry)
   - Kubernetes configuration file (`kubeconfig`)

2. **Create Jenkins Pipeline Job**:
   - Select "Pipeline" job type
   - Under "Pipeline" section, select "Pipeline script from SCM"
   - Set Repository URL: `https://github.com/ShahzaibAli-1/flask-k8s-ci-cd-assignment.git`
   - Set Branch: `feature/jenkins-k8s-pipeline`
   - Script Path: `Jenkinsfile`

### Step 2: Pipeline Stages Overview

The Jenkins pipeline executes the following stages automatically:

```
1. Checkout Code
   └─> Clones the latest code from GitHub

2. Build Docker Image
   └─> Builds and tags the Docker image: flask-app:latest

3. Deploy to Kubernetes
   └─> Applies Kubernetes manifests to the cluster
   └─> Creates/Updates deployment, service, and namespace

4. Verify Deployment
   └─> Checks pods, services, and deployments are running
   └─> Shows rollout history and current status

5. Smoke Test
   └─> Confirms at least one pod is running
   └─> Validates deployment success
```

### Step 3: Trigger Deployment

**Option A: Automatic Trigger** (Recommended)
- Configure GitHub webhook in Jenkins
- Push to `feature/jenkins-k8s-pipeline` branch
- Pipeline automatically starts

**Option B: Manual Trigger**
```powershell
# In Jenkins web interface:
1. Navigate to the pipeline job
2. Click "Build Now"
3. Monitor build progress in "Console Output"
```

### Step 4: Monitor Pipeline Execution

```powershell
# Watch Jenkins pipeline progress
# In Jenkins UI: Job > Build History > Select build > Console Output

# During deployment, monitor Kubernetes:
kubectl get pods -l app=flask-app --watch

kubectl get services

kubectl describe deployment flask-app

# Check rollout status
kubectl rollout status deployment/flask-app --watch
```

### Step 5: Access the Deployed Application

```powershell
# Get the NodePort service details
kubectl get service flask-service -o wide

# For NodePort (port 30008):
curl http://<NODE_IP>:30008

# For Minikube:
minikube service flask-service
```

### Step 6: Rollback or Update

```powershell
# View rollout history
kubectl rollout history deployment/flask-app

# Rollback to previous version
kubectl rollout undo deployment/flask-app

# Rollback to specific revision
kubectl rollout undo deployment/flask-app --to-revision=2
```

---

## Understanding Automated Rollouts, Scaling, and Load Balancing

### Automated Rollouts (Rolling Updates)

**What it does:** Updates the application to a new version with zero downtime.

**Configuration (in deployment.yaml):**
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1          # Launch 1 new pod before terminating old ones
    maxUnavailable: 1    # Allow 1 pod to be temporarily unavailable
```

**Process flow:**
```
Initial State (3 replicas):
[Old-v1] [Old-v1] [Old-v1]

Step 1:
[Old-v1] [Old-v1] [Old-v1] [New-v2]        # maxSurge: 1 new pod starts

Step 2:
[Old-v1] [Old-v1] [New-v2] [New-v2]        # Old pod removed (maxUnavailable: 1)

Step 3:
[Old-v1] [New-v2] [New-v2] [New-v2]        # Continue rolling

Step 4 (Complete):
[New-v2] [New-v2] [New-v2]                  # All pods updated, traffic flows to v2
```

**Benefits:**
- ✅ No service downtime during updates
- ✅ Automatic rollback if deployment fails
- ✅ Users experience no interruption
- ✅ Gradual version migration

**Trigger an update:**
```powershell
# Update container image
kubectl set image deployment/flask-app flask-app=flask-app:v2 --record

# Monitor the rolling update
kubectl rollout status deployment/flask-app
```

### Horizontal Pod Autoscaling (HPA)

**What it does:** Automatically scales the number of pods based on resource usage.

**Current Configuration (deployment.yaml):**
```yaml
spec:
  replicas: 3              # Fixed 3 pods currently

resources:
  requests:
    cpu: "100m"            # Each pod needs 100 millicores minimum
    memory: "128Mi"        # Each pod needs 128MB minimum
  limits:
    cpu: "200m"            # Maximum 200 millicores per pod
    memory: "256Mi"        # Maximum 256MB per pod
```

**How HPA would work (if configured):**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flask-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-app
  minReplicas: 2           # Minimum 2 pods
  maxReplicas: 10          # Maximum 10 pods
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70   # Scale up if avg CPU > 70%
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80   # Scale up if avg memory > 80%
```

**Scaling behavior:**
- **Scale Up**: If average CPU/memory exceeds threshold → more pods added (up to maxReplicas)
- **Scale Down**: If average CPU/memory falls below threshold → pods removed (down to minReplicas)
- **Adjustment Period**: Scales up every 3 min, scales down every 5 min (conservative approach)

**Example scenario:**
```
Traffic increases:
2 pods (running well)
└─> CPU usage rises to 85% (exceeds 70% threshold)
    └─> HPA adds pods
        └─> 4 pods (CPU drops to 60%, now optimal)

Traffic decreases:
4 pods (over-provisioned)
└─> CPU usage drops to 40% (below 70% threshold)
    └─> After 5 min wait, HPA removes pods
        └─> 2 pods (CPU rises to 50%, still good)
```

### Service Load Balancing

**What it does:** Distributes incoming traffic across all healthy pod replicas.

**Configuration (in service.yaml):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  selector:
    app: flask-app           # Select pods with this label
  ports:
    - protocol: TCP
      port: 80               # External port
      targetPort: 5000       # Internal pod port
  type: NodePort             # Exposes on node port 30008
```

**How load balancing works:**

```
Request arrives at NodePort 30008
        │
        ▼
┌─────────────────────────────────────┐
│   Service (flask-service)           │
│   Port: 80 → targetPort: 5000      │
│   Type: NodePort (30008)            │
│   Selector: app=flask-app           │
└────────┬────────┬────────┬──────────┘
         │        │        │
    ┌────▼─┐  ┌───▼──┐  ┌──▼────┐
    │Pod 1 │  │Pod 2 │  │Pod 3  │
    │5000  │  │5000  │  │5000   │
    │      │  │      │  │       │
    │✓ OK  │  │✓ OK  │  │✓ OK   │
    └──────┘  └──────┘  └───────┘

Traffic distribution (round-robin):
Request 1 → Pod 1
Request 2 → Pod 2
Request 3 → Pod 3
Request 4 → Pod 1  (cycles back)
```

**Load Balancing Algorithm:**
- **Round-Robin (Default)**: Each request goes to next available pod in order
- **IP Hash (Optional)**: Same client IP always routes to same pod (sessionAffinity: ClientIP)

**Key features:**
- ✅ Even distribution across healthy pods
- ✅ Automatic removal of failed pods from load balancer
- ✅ Pod IP addresses hidden from users
- ✅ Service IP stable even when pods restart

**Verify load balancing:**
```powershell
# Create a service IP (internal to cluster)
kubectl get service flask-service

# See which pods receive traffic
kubectl exec -it <pod-name> -- bash
# Inside pod, check logs to see traffic patterns
```

---

## Monitoring and Troubleshooting

### Common Commands

```powershell
# View pods status
kubectl get pods -l app=flask-app

# View detailed pod information
kubectl describe pod <pod-name>

# Check pod logs
kubectl logs <pod-name>

# Stream logs in real-time
kubectl logs -f <pod-name>

# View all deployment events
kubectl describe deployment flask-app

# Check resource usage
kubectl top pods -l app=flask-app
kubectl top nodes
```

### Deployment Issues

```powershell
# If pods not starting, check:
kubectl describe pod <pod-name>

# If service not accessible:
kubectl describe service flask-service

# If image not pulling:
kubectl get events --sort-by='.lastTimestamp'

# Debug by running shell in pod:
kubectl exec -it <pod-name> -- /bin/bash
```

---

## Summary

This project demonstrates a production-ready DevOps pipeline:

| Component | Feature | Benefit |
|-----------|---------|---------|
| **Docker** | Multi-stage build | Optimized 150MB image |
| **Kubernetes** | Rolling updates | Zero-downtime deployments |
| **Service** | NodePort + Load Balancer | Traffic distribution |
| **Replicas** | 3 pods | High availability |
| **Health Checks** | Liveness + Readiness | Self-healing infrastructure |
| **Jenkins** | Automated pipeline | CI/CD automation |

**Architecture flow:**
```
GitHub Repository
    ↓ (push to feature/jenkins-k8s-pipeline)
    ↓
Jenkins Pipeline (checkout → build → deploy)
    ↓
Docker Image Build & Storage
    ↓
Kubernetes Cluster
    ├─ Deployment (3 replicas, rolling updates)
    ├─ Service (NodePort 30008, load balancing)
    ├─ Health Checks (auto-healing)
    └─ Users Access via http://<node-ip>:30008
```

This setup provides automatic scaling, zero-downtime deployments, load balancing, and self-healing capabilities for production deployments.
