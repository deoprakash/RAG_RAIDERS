# AWS Deployment Configuration

## AWS Lambda Deployment

### Prerequisites
- AWS CLI installed and configured
- AWS credentials set up

### Deployment Steps

1. **Install AWS CLI**
   ```bash
   pip install awscli
   aws configure
   ```

2. **Create Lambda Function**
   ```bash
   aws lambda create-function \
     --function-name rift26-backend \
     --runtime python3.9 \
     --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
     --handler lambda_function.lambda_handler \
     --zip-file fileb://deployment.zip
   ```

3. **Update Function Code**
   ```bash
   aws lambda update-function-code \
     --function-name rift26-backend \
     --zip-file fileb://deployment.zip
   ```

## AWS Elastic Beanstalk

### Configuration File: .ebextensions/python.config

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: application:application
  aws:elasticbeanstalk:application:environment:
    PYTHONUNBUFFERED: "1"
    CI_ENVIRONMENT: "aws"
```

### Deployment Commands

```bash
# Initialize EB
eb init -p python-3.9 rift26-backend

# Create environment
eb create rift26-prod

# Deploy
eb deploy
```

## AWS ECS (Docker)

### Task Definition: ecs-task-definition.json

```json
{
  "family": "rift26-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "rift26-container",
      "image": "YOUR_ECR_REPO/rift26:latest",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "PYTHONUNBUFFERED",
          "value": "1"
        },
        {
          "name": "CI_ENVIRONMENT",
          "value": "aws"
        }
      ]
    }
  ]
}
```

### Deploy to ECS

```bash
# Build and push Docker image
docker build -t rift26:latest .
docker tag rift26:latest YOUR_ECR_REPO/rift26:latest
docker push YOUR_ECR_REPO/rift26:latest

# Register task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Update service
aws ecs update-service \
  --cluster rift26-cluster \
  --service rift26-service \
  --task-definition rift26-backend
```

## Monitoring

### CloudWatch Logs
```bash
aws logs tail /aws/lambda/rift26-backend --follow
```

### Health Check
```bash
aws lambda invoke \
  --function-name rift26-backend \
  --payload '{"action":"health_check"}' \
  output.json
```
