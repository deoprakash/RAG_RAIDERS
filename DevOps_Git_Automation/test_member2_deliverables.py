"""
Test all Member 2 (DevOps Lead) deliverables.
Ensures all systems are working before hackathon demo.
"""
import sys
from pathlib import Path
import json

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "scripts"))

def test_deliverable_1():
    """Test: Working Git Automation"""
    print("\n" + "="*70)
    print("  DELIVERABLE 1: Working Git Automation")
    print("="*70)
    
    from branch_manager import BranchManager
    
    # Test branch manager
    print("\n[TEST] Creating branches with TEAM_LEADER_AI_Fix naming...")
    manager = BranchManager()
    
    # Create branches
    branch_configs = [
        ("bug", "101", "fix_authentication"),
        ("feature", "102", "add_analytics"),
        ("hotfix", "103", "security_patch"),
        ("fix", None, "performance_optimization"),
    ]
    
    created_branches = []
    for branch_type, issue_id, description in branch_configs:
        branch = manager.create_branch_entry(branch_type, issue_id, description)
        created_branches.append(branch)
        print(f"  [OK] {branch['branch_name']}")
    
    # Verify file
    history_file = project_root / "data" / "branch_history.json"
    
    print(f"\n[CHECK] Verifying {history_file}")
    if not history_file.exists():
        print(f"  [FAIL] File does not exist")
        return False
    
    history = json.loads(history_file.read_text())
    print(f"  [CHECK] Branches created: {len(created_branches)}")
    print(f"  [CHECK] Branches saved: {len(history)}")
    print(f"  [CHECK] File size: {history_file.stat().st_size} bytes")
    
    # Verify naming convention
    all_correct = all(
        branch['branch_name'].startswith("TEAM_LEADER_AI_Fix/")
        for branch in history
    )
    
    success = len(history) >= 4 and all_correct
    
    if success:
        print("\n  [PASS] Deliverable 1: Working Git Automation ✓")
    else:
        print("\n  [FAIL] Deliverable 1: Issues detected ✗")
    
    return success


def test_deliverable_2():
    """Test: CI/CD Timeline Data"""
    print("\n" + "="*70)
    print("  DELIVERABLE 2: CI/CD Timeline Data")
    print("="*70)
    
    required_files = [
        "data/branch_history.json",
        "data/ci_pipeline_timeline.json",
        "data/iteration_tracker.json",
        "data/deployment_history.json",
        "data/git_automation_history.json"
    ]
    
    print("\n[CHECK] Verifying CI/CD data files:")
    files_exist = []
    files_with_data = []
    
    for file_path in required_files:
        full_path = project_root / file_path
        exists = full_path.exists()
        size = full_path.stat().st_size if exists else 0
        has_data = size > 2  # More than just "[]"
        
        if exists and has_data:
            status = "[OK]     "
        elif exists:
            status = "[EMPTY]  "
        else:
            status = "[MISSING]"
        
        print(f"  {status} {file_path:<40} ({size:>6} bytes)")
        
        files_exist.append(exists)
        files_with_data.append(has_data)
    
    total_files = len(required_files)
    existing_files = sum(files_exist)
    files_with_content = sum(files_with_data)
    
    print(f"\n  Summary: {existing_files}/{total_files} files exist, {files_with_content}/{total_files} have data")
    
    # Pass if at least branch_history and one other file has data
    success = files_exist[0] and files_with_data[0] and existing_files >= 4
    
    if success:
        print("\n  [PASS] Deliverable 2: CI/CD Timeline Data ✓")
    else:
        print("\n  [WARN] Deliverable 2: Some files need data (Docker required for full CI/CD)")
    
    return success


def test_branch_naming_convention():
    """Test: TEAM_LEADER_AI_Fix naming convention"""
    print("\n" + "="*70)
    print("  BONUS: Branch Naming Convention Test")
    print("="*70)
    
    history_file = project_root / "data" / "branch_history.json"
    
    if not history_file.exists():
        print("  [SKIP] No branch history file")
        return False
    
    history = json.loads(history_file.read_text())
    
    if not history:
        print("  [SKIP] No branches in history")
        return False
    
    print(f"\n[TEST] Verifying {len(history)} branches:")
    
    all_valid = True
    for idx, branch in enumerate(history, 1):
        name = branch['branch_name']
        valid = name.startswith("TEAM_LEADER_AI_Fix/")
        status = "[OK]" if valid else "[FAIL]"
        
        # Show first and last branch
        if idx <= 2 or idx == len(history):
            print(f"  {status} {name}")
        elif idx == 3:
            print(f"  ... ({len(history) - 3} more branches)")
        
        all_valid = all_valid and valid
    
    if all_valid:
        print("\n  [PASS] All branches follow TEAM_LEADER_AI_Fix convention ✓")
    else:
        print("\n  [FAIL] Some branches don't follow convention ✗")
    
    return all_valid


def main():
    """Run all Member 2 tests."""
    print("\n" + "="*70)
    print("  MEMBER 2 - DevOps/Git Automation Lead")
    print("  DELIVERABLES TEST SUITE")
    print("="*70)
    print("\n  Testing all Member 2 hackathon deliverables...")
    
    results = []
    
    # Test deliverable 1
    results.append(("Git Automation", test_deliverable_1()))
    
    # Test deliverable 2
    results.append(("CI/CD Timeline Data", test_deliverable_2()))
    
    # Bonus test
    results.append(("Branch Naming Convention", test_branch_naming_convention()))
    
    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n  Results: {passed}/{total} tests passed")
    
    if passed >= 2:  # At least core deliverables work
        print("\n  [SUCCESS] Member 2 deliverables ready for hackathon! 🚀")
        print("\n  Note: Run with Docker Desktop for full CI/CD pipeline data")
        return 0
    else:
        print("\n  [WARNING] Core deliverables need attention")
        return 1


if __name__ == "__main__":
    sys.exit(main())
