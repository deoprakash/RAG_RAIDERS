"""
Docker Sandbox Configuration
Manages Docker-based test environments
"""

import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
log_dir = Path(__file__).parent.parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"docker_sandbox_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class DockerSandbox:
    """Manages Docker sandbox environments for testing"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        
    def check_docker(self):
        """Check if Docker is available"""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info(f"✓ Docker available: {result.stdout.strip()}")
                return True
            else:
                logger.error("✗ Docker not available")
                return False
                
        except Exception as e:
            logger.error(f"✗ Failed to check Docker: {e}")
            return False
    
    def build_image(self, service="ci-pipeline"):
        """Build Docker image"""
        logger.info(f"Building Docker image for {service}...")
        
        try:
            result = subprocess.run(
                ["docker-compose", "build", service],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                logger.info(f"✓ Image built successfully")
                return True
            else:
                logger.error(f"✗ Build failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Failed to build image: {e}")
            return False
    
    def run_container(self, service, command=None):
        """Run Docker container"""
        logger.info(f"Running container: {service}")
        
        cmd = ["docker-compose", "run", "--rm", service]
        if command:
            cmd.append(command)
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            return {
                "success": result.returncode == 0,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except Exception as e:
            logger.error(f"✗ Failed to run container: {e}")
            return None
    
    def run_pytest_sandbox(self):
        """Run pytest in Docker sandbox"""
        logger.info("Running pytest in sandbox...")
        
        result = self.run_container("pytest-runner")
        
        if result and result["success"]:
            logger.info("✓ Tests passed in sandbox")
            return True
        else:
            logger.error("✗ Tests failed in sandbox")
            return False
    
    def cleanup(self):
        """Clean up Docker resources"""
        logger.info("Cleaning up Docker resources...")
        
        try:
            subprocess.run(
                ["docker-compose", "down"],
                cwd=self.project_root,
                capture_output=True,
                timeout=60
            )
            logger.info("✓ Cleanup complete")
        except Exception as e:
            logger.error(f"✗ Cleanup failed: {e}")


def main():
    """Main execution"""
    logger.info("=== Docker Sandbox Manager ===\n")
    
    sandbox = DockerSandbox()
    
    # Check Docker
    if not sandbox.check_docker():
        logger.error("Docker is not available. Please install Docker.")
        return
    
    # Build image
    if sandbox.build_image():
        logger.info("Docker environment ready!")
    
    logger.info("\nSandbox management complete!")


if __name__ == "__main__":
    main()
