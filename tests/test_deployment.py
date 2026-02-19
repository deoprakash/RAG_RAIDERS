"""
Test suite for Deployment
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "deployment"))


class TestDeployment:
    """Tests for Deployment Manager"""
    
    def test_deployment_manager_import(self):
        """Test Deployment Manager can be imported"""
        from deploy import DeploymentManager
        assert DeploymentManager is not None
    
    def test_deployment_manager_initialization(self):
        """Test Deployment Manager initialization"""
        from deploy import DeploymentManager
        manager = DeploymentManager()
        
        assert manager.deployment_history == []
        assert manager.data_dir.exists()
    
    def test_railway_deployment_simulation(self):
        """Test Railway deployment (simulation)"""
        from deploy import DeploymentManager
        manager = DeploymentManager()
        
        result = manager.deploy_railway("test-service")
        
        assert result is not None
        assert "platform" in result
        assert result["platform"] == "railway"
        assert "status" in result
    
    def test_aws_deployment_simulation(self):
        """Test AWS deployment (simulation)"""
        from deploy import DeploymentManager
        manager = DeploymentManager()
        
        result = manager.deploy_aws(region="us-east-1", service_type="lambda")
        
        assert result is not None
        assert "platform" in result
        assert result["platform"] == "aws"
        assert "status" in result
        assert result["region"] == "us-east-1"


def test_deployment_history_tracking():
    """Test deployment history is tracked properly"""
    from deploy import DeploymentManager
    manager = DeploymentManager()
    
    # Simulate multiple deployments
    manager.deploy_railway("service-1")
    manager.deploy_aws("us-west-2", "ecs")
    
    assert len(manager.deployment_history) >= 2
    
    # Verify first deployment
    first = manager.deployment_history[0]
    assert first["platform"] == "railway"
    
    # Verify second deployment
    second = manager.deployment_history[1]
    assert second["platform"] == "aws"


def test_deployment_configurations_exist():
    """Test deployment configuration files exist"""
    project_root = Path(__file__).parent.parent
    
    # Railway configs
    railway_dir = project_root / "deployment" / "railway"
    assert railway_dir.exists()
    assert (railway_dir / "README.md").exists()
    assert (railway_dir / "railway.json").exists()
    
    # AWS configs
    aws_dir = project_root / "deployment" / "aws"
    assert aws_dir.exists()
    assert (aws_dir / "README.md").exists()
    assert (aws_dir / "ecs-task-definition.json").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
