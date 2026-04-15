"""
DevOps Tools - Docker, CI/CD, and Cloud API Examples
"""

import os
import subprocess
import json
from typing import Dict, List


# Docker Examples
def create_dockerfile():
    """Create a sample Dockerfile for a Python application"""
    dockerfile_content = """
# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content.strip())
    
    print("Created Dockerfile")


def create_docker_compose():
    """Create a sample docker-compose.yml file"""
    docker_compose_content = """
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - .:/app
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_content.strip())
    
    print("Created docker-compose.yml")


def docker_commands():
    """Demonstrate common Docker commands"""
    print("Common Docker Commands:")
    print("  docker build -t myapp .")
    print("  docker run -p 5000:5000 myapp")
    print("  docker ps")
    print("  docker stop <container_id>")
    print("  docker-compose up -d")
    print("  docker-compose down")


# CI/CD Examples
def create_github_actions_workflow():
    """Create a sample GitHub Actions workflow file"""
    workflow_content = """
name: Python CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t myapp:${{ github.sha }} .
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push myapp:${{ github.sha }}
"""
    
    os.makedirs(".github/workflows", exist_ok=True)
    with open(".github/workflows/ci-cd.yml", "w") as f:
        f.write(workflow_content.strip())
    
    print("Created GitHub Actions workflow: .github/workflows/ci-cd.yml")


def create_jenkinsfile():
    """Create a sample Jenkinsfile"""
    jenkinsfile_content = """
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest'
            }
        }
        
        stage('Package') {
            steps {
                sh 'docker build -t myapp:${BUILD_NUMBER} .'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker push myapp:${BUILD_NUMBER}'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
"""
    
    with open("Jenkinsfile", "w") as f:
        f.write(jenkinsfile_content.strip())
    
    print("Created Jenkinsfile")


# Cloud API Examples
def create_aws_boto3_example():
    """Create AWS Boto3 example for cloud operations"""
    boto3_example = """
import boto3
from typing import Dict, List

class AWSCloudManager:
    '''Simple AWS cloud operations manager'''
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.s3 = boto3.client('s3', region_name=region)
    
    def list_instances(self) -> List[Dict]:
        '''List all EC2 instances'''
        response = self.ec2.describe_instances()
        instances = []
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'State': instance['State']['Name']
                })
        
        return instances
    
    def create_s3_bucket(self, bucket_name: str) -> bool:
        '''Create S3 bucket'''
        try:
            self.s3.create_bucket(Bucket=bucket_name)
            return True
        except Exception as e:
            print(f"Error creating bucket: {e}")
            return False
    
    def list_s3_buckets(self) -> List[str]:
        '''List all S3 buckets'''
        response = self.s3.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]

# Example usage:
if __name__ == "__main__":
    # Note: This requires AWS credentials configured
    # manager = AWSCloudManager()
    # instances = manager.list_instances()
    # print(f"Found {len(instances)} instances")
    pass
"""
    
    with open("aws_cloud_manager.py", "w") as f:
        f.write(boto3_example.strip())
    
    print("Created AWS cloud manager example: aws_cloud_manager.py")


def create_azure_example():
    """Create Azure SDK example"""
    azure_example = """
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient

class AzureCloudManager:
    '''Simple Azure cloud operations manager'''
    
    def __init__(self, subscription_id: str):
        self.subscription_id = subscription_id
        self.credential = DefaultAzureCredential()
        self.resource_client = ResourceManagementClient(
            self.credential, 
            subscription_id
        )
        self.compute_client = ComputeManagementClient(
            self.credential,
            subscription_id
        )
    
    def list_virtual_machines(self, resource_group: str) -> List:
        '''List virtual machines in resource group'''
        vms = self.compute_client.virtual_machines.list(resource_group)
        return list(vms)
    
    def create_resource_group(self, resource_group_name: str, location: str):
        '''Create resource group'''
        return self.resource_client.resource_groups.create_or_update(
            resource_group_name,
            {'location': location}
        )

# Example usage:
if __name__ == "__main__":
    # Note: This requires Azure credentials configured
    # manager = AzureCloudManager("subscription-id")
    # vms = manager.list_virtual_machines("resource-group")
    # print(f"Found {len(vms)} virtual machines")
    pass
"""
    
    with open("azure_cloud_manager.py", "w") as f:
        f.write(azure_example.strip())
    
    print("Created Azure cloud manager example: azure_cloud_manager.py")


def create_kubernetes_example():
    """Create Kubernetes example"""
    kubernetes_example = """
from kubernetes import client, config

class KubernetesManager:
    '''Simple Kubernetes operations manager'''
    
    def __init__(self):
        # Load kube config
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
    
    def list_pods(self, namespace: str = 'default') -> List:
        '''List pods in namespace'''
        pods = self.v1.list_namespaced_pod(namespace)
        return pods.items
    
    def list_deployments(self, namespace: str = 'default') -> List:
        '''List deployments in namespace'''
        deployments = self.apps_v1.list_namespaced_deployment(namespace)
        return deployments.items
    
    def create_deployment(self, namespace: str, deployment_manifest: Dict):
        '''Create deployment from manifest'''
        return self.apps_v1.create_namespaced_deployment(
            namespace=namespace,
            body=deployment_manifest
        )

# Example usage:
if __name__ == "__main__":
    # Note: This requires kube config configured
    # manager = KubernetesManager()
    # pods = manager.list_pods()
    # print(f"Found {len(pods)} pods")
    pass
"""
    
    with open("kubernetes_manager.py", "w") as f:
        f.write(kubernetes_example.strip())
    
    print("Created Kubernetes manager example: kubernetes_manager.py")


# Infrastructure as Code
def create_terraform_example():
    """Create Terraform example"""
    terraform_example = """
# Provider configuration
provider "aws" {
  region = "us-east-1"
}

# VPC resource
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "main-vpc"
  }
}

# EC2 instance
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.main.id
  
  tags = {
    Name = "WebServer"
  }
}

# Subnet
resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  
  tags = {
    Name = "main-subnet"
  }
}
"""
    
    with open("main.tf", "w") as f:
        f.write(terraform_example.strip())
    
    print("Created Terraform configuration: main.tf")


def main():
    """Main function to demonstrate DevOps tools"""
    print("DevOps Tools Examples")
    print("=" * 50)
    
    print("\nDocker Examples:")
    create_dockerfile()
    create_docker_compose()
    docker_commands()
    
    print("\nCI/CD Examples:")
    create_github_actions_workflow()
    create_jenkinsfile()
    
    print("\nCloud API Examples:")
    create_aws_boto3_example()
    create_azure_example()
    create_kubernetes_example()
    
    print("\nInfrastructure as Code:")
    create_terraform_example()
    
    print("\n" + "=" * 50)
    print("DevOps Key Concepts:")
    print("✓ Docker: Containerization and deployment")
    print("✓ CI/CD: Automated testing and deployment pipelines")
    print("✓ Cloud APIs: Programmatic cloud resource management")
    print("✓ IaC: Infrastructure as Code with Terraform")
    print("✓ Kubernetes: Container orchestration")
    print("✓ Monitoring: Observability and logging")
    
    print("\nTools Covered:")
    print("• Docker & Docker Compose")
    print("• GitHub Actions")
    print("• Jenkins")
    print("• AWS Boto3")
    print("• Azure SDK")
    print("• Kubernetes Python Client")
    print("• Terraform")
    
    print("\nTo use cloud SDKs:")
    print("pip install boto3 azure-identity azure-mgmt kubernetes")
    print("\nFor Docker:")
    print("Install Docker Desktop and use Docker CLI")
    print("\nFor CI/CD:")
    print("Configure GitHub Actions or Jenkins server")


if __name__ == "__main__":
    main()