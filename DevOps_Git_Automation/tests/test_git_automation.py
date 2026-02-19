"""
Test suite for Git Automation
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from branch_manager import BranchManager


class TestBranchManager:
    """Tests for BranchManager"""
    
    def test_generate_branch_name_basic(self):
        """Test basic branch name generation"""
        manager = BranchManager()
        branch_name = manager.generate_branch_name("fix")
        
        assert "TEAM_LEADER_AI_Fix/fix" in branch_name
        assert len(branch_name) > 0
    
    def test_generate_branch_name_with_issue(self):
        """Test branch name with issue ID"""
        manager = BranchManager()
        branch_name = manager.generate_branch_name("bug", issue_id="123")
        
        assert "TEAM_LEADER_AI_Fix/bug" in branch_name
        assert "issue_123" in branch_name
    
    def test_generate_branch_name_with_description(self):
        """Test branch name with description"""
        manager = BranchManager()
        branch_name = manager.generate_branch_name(
            "feature",
            description="Add new dashboard"
        )
        
        assert "TEAM_LEADER_AI_Fix/feature" in branch_name
        assert "add_new_dashboard" in branch_name
    
    def test_generate_branch_name_full(self):
        """Test branch name with all parameters"""
        manager = BranchManager()
        branch_name = manager.generate_branch_name(
            "hotfix",
            issue_id="456",
            description="Critical security patch"
        )
        
        assert "TEAM_LEADER_AI_Fix/hotfix" in branch_name
        assert "issue_456" in branch_name
        assert "critical" in branch_name
    
    def test_branch_prefix_constant(self):
        """Test branch prefix constant"""
        assert BranchManager.BRANCH_PREFIX == "TEAM_LEADER_AI_Fix"


class TestGitAutomation:
    """Tests for Git Automation"""
    
    def test_import_git_automation(self):
        """Test that git_automation module can be imported"""
        from git_automation import GitAutomation
        assert GitAutomation is not None
    
    def test_import_repo_clone(self):
        """Test that repo_clone module can be imported"""
        from repo_clone import RepoCloner
        assert RepoCloner is not None


def test_project_structure():
    """Test that project structure is correct"""
    project_root = Path(__file__).parent.parent
    
    # Check key directories exist
    assert (project_root / "scripts").exists()
    assert (project_root / "ci_cd").exists()
    assert (project_root / "deployment").exists()
    assert (project_root / "tests").exists()
    
    # Check key files exist
    assert (project_root / "README.md").exists()
    assert (project_root / "requirements.txt").exists()
    assert (project_root / "Dockerfile").exists()


def test_branch_naming_convention():
    """Test branch naming follows TEAM_LEADER_AI_Fix convention"""
    manager = BranchManager()
    
    test_cases = [
        ("bug", None, None),
        ("feature", "789", None),
        ("fix", None, "improve performance"),
        ("hotfix", "111", "emergency fix")
    ]
    
    for issue_type, issue_id, description in test_cases:
        branch_name = manager.generate_branch_name(issue_type, issue_id, description)
        assert branch_name.startswith("TEAM_LEADER_AI_Fix/")
        print(f"✓ Generated: {branch_name}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
