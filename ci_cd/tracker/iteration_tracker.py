"""
Iteration Tracker for CI/CD Timeline
Tracks and visualizes CI/CD pipeline iterations
"""

import json
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class IterationTracker:
    """Tracks CI/CD pipeline iterations and generates timeline data"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.timeline_file = self.data_dir / "ci_pipeline_timeline.json"
        self.tracker_file = self.data_dir / "iteration_tracker.json"
        
        self.iterations = []
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing timeline data"""
        if self.timeline_file.exists():
            try:
                with open(self.timeline_file, 'r') as f:
                    data = json.load(f)
                    self.iterations = data.get('pipeline_history', [])
                    logger.info(f"Loaded {len(self.iterations)} existing iterations")
            except Exception as e:
                logger.error(f"Failed to load existing data: {e}")
    
    def add_iteration(self, iteration_data):
        """Add a new iteration to tracking"""
        self.iterations.append(iteration_data)
        logger.info(f"Added iteration #{len(self.iterations)}")
    
    def get_statistics(self):
        """Calculate statistics from iterations"""
        if not self.iterations:
            return None
        
        total = len(self.iterations)
        passed = sum(1 for i in self.iterations if i.get('status') == 'passed')
        failed = total - passed
        
        durations = [i.get('duration', 0) for i in self.iterations]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        stats = {
            "total_iterations": total,
            "passed": passed,
            "failed": failed,
            "success_rate": round((passed / total) * 100, 2) if total > 0 else 0,
            "average_duration": round(avg_duration, 2),
            "total_duration": round(sum(durations), 2)
        }
        
        return stats
    
    def generate_timeline_report(self):
        """Generate detailed timeline report"""
        stats = self.get_statistics()
        
        if not stats:
            logger.warning("No iterations to report")
            return None
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "project": "RIFT'26 - DevOps/Git Automation Lead",
            "statistics": stats,
            "iterations": []
        }
        
        # Process each iteration
        for idx, iteration in enumerate(self.iterations, 1):
            iteration_summary = {
                "iteration_number": idx,
                "status": iteration.get('status'),
                "duration": iteration.get('duration'),
                "start_time": iteration.get('start_time'),
                "end_time": iteration.get('end_time'),
                "stages": {}
            }
            
            # Process stages
            stages = iteration.get('stages', {})
            for stage_name, stage_data in stages.items():
                iteration_summary['stages'][stage_name] = {
                    "passed": stage_data.get('passed', False),
                    "timestamp": stage_data.get('timestamp')
                }
            
            report['iterations'].append(iteration_summary)
        
        return report
    
    def save_report(self):
        """Save timeline report to file"""
        report = self.generate_timeline_report()
        
        if not report:
            return False
        
        with open(self.tracker_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to {self.tracker_file}")
        return True
    
    def print_summary(self):
        """Print summary to console"""
        stats = self.get_statistics()
        
        if not stats:
            logger.warning("No data to summarize")
            return
        
        print("\n" + "="*60)
        print("CI/CD PIPELINE TIMELINE SUMMARY")
        print("="*60)
        print(f"Total Iterations:    {stats['total_iterations']}")
        print(f"Passed:              {stats['passed']} ({stats['success_rate']}%)")
        print(f"Failed:              {stats['failed']}")
        print(f"Average Duration:    {stats['average_duration']}s")
        print(f"Total Duration:      {stats['total_duration']}s")
        print("="*60 + "\n")
        
        # Print iteration details
        print("ITERATION DETAILS:")
        print("-" * 60)
        
        for idx, iteration in enumerate(self.iterations, 1):
            status_icon = "✓" if iteration.get('status') == 'passed' else "✗"
            duration = iteration.get('duration', 0)
            print(f"{status_icon} Iteration #{idx:2d} - {iteration.get('status', 'unknown'):8s} - {duration:6.2f}s")
        
        print("-" * 60 + "\n")


def main():
    """Main execution"""
    logger.info("=== Iteration Tracker ===\n")
    
    tracker = IterationTracker()
    
    # Print summary
    tracker.print_summary()
    
    # Save report
    tracker.save_report()
    
    logger.info("Tracking complete!")


if __name__ == "__main__":
    main()
