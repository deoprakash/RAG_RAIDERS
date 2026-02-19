"""
Test suite for CI/CD Pipeline
"""

import pytest
from pathlib import Path
import sys
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "ci_cd" / "pipeline"))
sys.path.insert(0, str(Path(__file__).parent.parent / "ci_cd" / "tracker"))


class TestCIPipeline:
    """Tests for CI Pipeline"""
    
    def test_ci_runner_import(self):
        """Test CI Runner can be imported"""
        from ci_runner import CIRunner
        assert CIRunner is not None
    
    def test_ci_runner_initialization(self):
        """Test CI Runner initialization"""
        from ci_runner import CIRunner
        runner = CIRunner()
        
        assert runner.current_iteration == 0
        assert runner.pipeline_history == []
        assert runner.start_time is None


class TestIterationTracker:
    """Tests for Iteration Tracker"""
    
    def test_tracker_import(self):
        """Test Iteration Tracker can be imported"""
        from iteration_tracker import IterationTracker
        assert IterationTracker is not None
    
    def test_tracker_initialization(self):
        """Test tracker initialization"""
        from iteration_tracker import IterationTracker
        tracker = IterationTracker()
        
        assert tracker.data_dir.exists()
        assert isinstance(tracker.iterations, list)
    
    def test_add_iteration(self):
        """Test adding iteration"""
        from iteration_tracker import IterationTracker
        tracker = IterationTracker()
        
        test_iteration = {
            "iteration": 1,
            "status": "passed",
            "duration": 45.2
        }
        
        tracker.add_iteration(test_iteration)
        assert len(tracker.iterations) >= 1


class TestDockerSandbox:
    """Tests for Docker Sandbox"""
    
    def test_docker_sandbox_import(self):
        """Test Docker Sandbox can be imported"""
        sys.path.insert(0, str(Path(__file__).parent.parent / "ci_cd" / "docker"))
        from sandbox_manager import DockerSandbox
        assert DockerSandbox is not None


def test_ci_pipeline_flow():
    """Test complete CI pipeline flow"""
    from ci_runner import CIRunner
    
    runner = CIRunner()
    
    # Test that runner is ready
    assert runner.current_iteration == 0
    
    # Simulate pipeline data
    pipeline_data = {
        "iteration": 1,
        "status": "passed",
        "duration": 30.5,
        "stages": {
            "build": {"passed": True},
            "test": {"passed": True}
        }
    }
    
    runner.pipeline_history.append(pipeline_data)
    assert len(runner.pipeline_history) == 1
    assert runner.pipeline_history[0]["status"] == "passed"


def test_timeline_data_structure():
    """Test timeline data structure"""
    from iteration_tracker import IterationTracker
    
    tracker = IterationTracker()
    
    # Add test iterations
    test_iterations = [
        {"iteration": 1, "status": "passed", "duration": 25.3},
        {"iteration": 2, "status": "passed", "duration": 28.1},
        {"iteration": 3, "status": "failed", "duration": 15.7}
    ]
    
    for iteration in test_iterations:
        tracker.add_iteration(iteration)
    
    stats = tracker.get_statistics()
    
    assert stats is not None
    assert stats["total_iterations"] >= 3
    assert "success_rate" in stats
    assert "average_duration" in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
