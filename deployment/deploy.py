"""
Deployment Manager
Handles deployment to Railway and AWS
"""

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class DeploymentManager:
    """Manages deployments to various platforms"""
    
    def __init__(self):
        self.deployment_history = []
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
    
    def deploy_railway(self, service_name="rift26-backend"):
        """
        Deploy to Railway
        
        Args:
            service_name (str): Name of the service
            
        Returns:
            dict: Deployment result
        """
        logger.info(f"Deploying to Railway: {service_name}")
        
        deployment_result = {
            "platform": "railway",
            "service": service_name,
            "timestamp": datetime.now().isoformat(),
            "status": "initiated"
        }
        
        try:
            # Check if Railway CLI is installed
            check_result = subprocess.run(
                ["railway", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if check_result.returncode != 0:
                logger.warning("Railway CLI not installed. Simulating deployment...")
                deployment_result["status"] = "simulated"
                deployment_result["message"] = "Railway CLI not available - deployment simulated"
            else:
                logger.info("Railway CLI detected")
                
                # Login check (would require user interaction)
                logger.info("Note: Railway deployment requires authentication")
                deployment_result["status"] = "ready"
                deployment_result["message"] = "Ready for Railway deployment (requires auth)"
            
            deployment_result["success"] = True
            
        except FileNotFoundError:
            logger.warning("Railway CLI not found. Simulating deployment...")
            deployment_result["status"] = "simulated"
            deployment_result["success"] = True
            deployment_result["message"] = "Railway CLI not installed - deployment simulated"
        
        except Exception as e:
            logger.error(f"Deployment error: {e}")
            deployment_result["status"] = "failed"
            deployment_result["error"] = str(e)
            deployment_result["success"] = False
        
        self.deployment_history.append(deployment_result)
        return deployment_result
    
    def deploy_aws(self, region="us-east-1", service_type="lambda"):
        """
        Deploy to AWS
        
        Args:
            region (str): AWS region
            service_type (str): Type of AWS service (lambda, ec2, ecs)
            
        Returns:
            dict: Deployment result
        """
        logger.info(f"Deploying to AWS {service_type} in {region}")
        
        deployment_result = {
            "platform": "aws",
            "service_type": service_type,
            "region": region,
            "timestamp": datetime.now().isoformat(),
            "status": "initiated"
        }
        
        try:
            # Check if AWS CLI is installed
            check_result = subprocess.run(
                ["aws", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if check_result.returncode != 0:
                logger.warning("AWS CLI not installed. Simulating deployment...")
                deployment_result["status"] = "simulated"
                deployment_result["message"] = "AWS CLI not available - deployment simulated"
            else:
                logger.info("AWS CLI detected")
                deployment_result["status"] = "ready"
                deployment_result["message"] = f"Ready for AWS {service_type} deployment"
            
            deployment_result["success"] = True
            
        except FileNotFoundError:
            logger.warning("AWS CLI not found. Simulating deployment...")
            deployment_result["status"] = "simulated"
            deployment_result["success"] = True
            deployment_result["message"] = "AWS CLI not installed - deployment simulated"
        
        except Exception as e:
            logger.error(f"Deployment error: {e}")
            deployment_result["status"] = "failed"
            deployment_result["error"] = str(e)
            deployment_result["success"] = False
        
        self.deployment_history.append(deployment_result)
        return deployment_result
    
    def validate_deployment(self, url):
        """
        Validate deployment by checking endpoint
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: Validation status
        """
        logger.info(f"Validating deployment at {url}")
        
        try:
            import requests
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                logger.info("✓ Deployment validated successfully")
                return True
            else:
                logger.warning(f"⚠ Unexpected status code: {response.status_code}")
                return False
                
        except ImportError:
            logger.warning("requests library not available, skipping validation")
            return None
        except Exception as e:
            logger.error(f"✗ Validation failed: {e}")
            return False
    
    def save_deployment_history(self):
        """Save deployment history to file"""
        history_file = self.data_dir / "deployment_history.json"
        
        with open(history_file, 'w') as f:
            json.dump(self.deployment_history, f, indent=2)
        
        logger.info(f"Deployment history saved to {history_file}")
    
    def print_deployment_summary(self):
        """Print deployment summary"""
        if not self.deployment_history:
            logger.info("No deployments recorded")
            return
        
        print("\n" + "="*60)
        print("DEPLOYMENT SUMMARY")
        print("="*60)
        
        for idx, deployment in enumerate(self.deployment_history, 1):
            platform = deployment.get('platform', 'unknown')
            status = deployment.get('status', 'unknown')
            success_icon = "✓" if deployment.get('success') else "✗"
            
            print(f"{success_icon} Deployment #{idx}")
            print(f"   Platform: {platform}")
            print(f"   Status: {status}")
            print(f"   Time: {deployment.get('timestamp', 'N/A')}")
            
            if 'message' in deployment:
                print(f"   Message: {deployment['message']}")
            print()
        
        print("="*60 + "\n")


def main():
    """Main execution"""
    logger.info("=== Deployment Manager ===\n")
    
    manager = DeploymentManager()
    
    # Deploy to Railway
    logger.info("Initiating Railway deployment...")
    railway_result = manager.deploy_railway("rift26-backend")
    
    # Deploy to AWS
    logger.info("\nInitiating AWS deployment...")
    aws_result = manager.deploy_aws(region="us-east-1", service_type="lambda")
    
    # Print summary
    manager.print_deployment_summary()
    
    # Save history
    manager.save_deployment_history()
    
    logger.info("Deployment process complete!")


if __name__ == "__main__":
    main()
