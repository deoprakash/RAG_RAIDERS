# Railway Deployment Configuration

## Configuration File: railway.json

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

## Environment Variables

Required environment variables for Railway:
- `PYTHONUNBUFFERED=1`
- `CI_ENVIRONMENT=railway`
- `PORT=8080`

## Deployment Commands

### Using Railway CLI

```bash
# Login to Railway
railway login

# Link to project
railway link

# Deploy
railway up
```

### Configuration Steps

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Initialize Project**
   ```bash
   railway init
   ```

3. **Set Environment Variables**
   ```bash
   railway variables set PYTHONUNBUFFERED=1
   railway variables set CI_ENVIRONMENT=railway
   ```

4. **Deploy**
   ```bash
   railway up
   ```

## Monitoring

Check deployment logs:
```bash
railway logs
```

## Rollback

Rollback to previous deployment:
```bash
railway rollback
```
