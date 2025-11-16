pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'flask-app'
        K8S_NAMESPACE = 'default'
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                echo '✅ Code checked out successfully from GitHub'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo '🐳 Building Docker image...'
                    sh 'docker build -t ${DOCKER_IMAGE}:latest .'
                    sh 'echo "Docker image built successfully:" && docker images | grep ${DOCKER_IMAGE}'
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo '🚀 Deploying to Kubernetes...'
                    sh '''
                        echo "Applying Kubernetes manifests..."
                        kubectl apply -f kubernetes/
                        
                        echo "Waiting for deployment to be ready..."
                        kubectl rollout status deployment/flask-app --timeout=300s
                        
                        echo "Kubernetes deployment completed!"
                    '''
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    echo '🔍 Verifying deployment...'
                    sh '''
                        echo "=== Checking Pods ==="
                        kubectl get pods -l app=flask-app -o wide
                        
                        echo "=== Checking Services ==="
                        kubectl get service flask-service -o wide
                        
                        echo "=== Checking Deployments ==="
                        kubectl get deployment flask-app -o wide
                        
                        echo "=== Rollout History ==="
                        kubectl rollout history deployment/flask-app
                        
                        echo "=== Rollout Status ==="
                        kubectl rollout status deployment/flask-app
                    '''
                }
            }
        }
        
        stage('Smoke Test') {
            steps {
                script {
                    echo '🧪 Running smoke tests...'
                    sh '''
                        echo "Checking if all pods are running..."
                        RUNNING_PODS=$(kubectl get pods -l app=flask-app --field-selector=status.phase=Running --no-headers | wc -l)
                        echo "Number of running pods: $RUNNING_PODS"
                        
                        if [ $RUNNING_PODS -ge 1 ]; then
                            echo "✅ Smoke test passed - pods are running"
                        else
                            echo "❌ Smoke test failed - no running pods found"
                            exit 1
                        fi
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo '🏁 Pipeline execution completed'
            script {
                // Final status check
                sh '''
                    echo "=== Final Status ==="
                    kubectl get pods,services,deployments -l app=flask-app
                '''
            }
        }
        success {
            echo '🎉 Pipeline succeeded! Application deployed successfully to Kubernetes.'
            // You can add notifications here (email, Slack, etc.)
        }
        failure {
            echo '💥 Pipeline failed! Check the logs for details.'
            // You can add failure notifications here
        }
    }
}