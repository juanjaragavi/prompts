"""
Production-grade analytics and monitoring system.
Tracks application submissions, success rates, and performance metrics.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
from collections import defaultdict
import statistics

class AnalyticsEngine:
    """
    Comprehensive analytics system tracking:
    - Application submissions by platform
    - Success/failure rates
    - Performance metrics
    - Candidate engagement tracking
    - Time-series analysis
    """
    
    def __init__(self, logger, config, status_dir: str):
        self.logger = logger
        self.config = config
        self.status_dir = status_dir
        self.analytics_file = os.path.join(status_dir, 'analytics.json')
        self.analytics_data = self._load_analytics()
    
    def _load_analytics(self) -> Dict[str, Any]:
        """Load existing analytics or create new"""
        try:
            if os.path.exists(self.analytics_file):
                with open(self.analytics_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load analytics: {str(e)}")
        
        return {
            'created_at': datetime.now().isoformat(),
            'applications': [],
            'metrics': {}
        }
    
    def record_application(
        self,
        index: int,
        company: str,
        job_title: str,
        platform: str,
        status: str,
        details: str = "",
        duration_seconds: float = 0
    ):
        """Record an application attempt"""
        try:
            record = {
                'index': index,
                'company': company,
                'job_title': job_title,
                'platform': platform,
                'status': status,
                'details': details,
                'duration_seconds': duration_seconds,
                'timestamp': datetime.now().isoformat(),
            }
            
            self.analytics_data['applications'].append(record)
            self._save_analytics()
            
            self.logger.debug(f"Recorded application: {company} - {job_title}")
        except Exception as e:
            self.logger.error(f"Error recording application: {str(e)}")
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """Generate comprehensive summary statistics"""
        try:
            apps = self.analytics_data['applications']
            
            if not apps:
                return {'status': 'no_data'}
            
            # Status breakdown
            status_counts = defaultdict(int)
            platform_counts = defaultdict(int)
            company_counts = defaultdict(int)
            
            for app in apps:
                status_counts[app['status']] += 1
                platform_counts[app['platform']] += 1
                company_counts[app['company']] += 1
            
            # Duration analysis
            durations = [app['duration_seconds'] for app in apps if app['duration_seconds'] > 0]
            
            # Success rate
            total = len(apps)
            submitted = status_counts.get('Submitted', 0) + status_counts.get('Form Filled', 0)
            success_rate = (submitted / total * 100) if total > 0 else 0
            
            return {
                'total_applications': total,
                'submitted_or_filled': submitted,
                'success_rate': success_rate,
                'status_breakdown': dict(status_counts),
                'platform_breakdown': dict(platform_counts),
                'company_breakdown': dict(company_counts),
                'duration': {
                    'avg_seconds': statistics.mean(durations) if durations else 0,
                    'min_seconds': min(durations) if durations else 0,
                    'max_seconds': max(durations) if durations else 0,
                    'median_seconds': statistics.median(durations) if durations else 0,
                },
                'timestamp': datetime.now().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Error generating summary statistics: {str(e)}")
            return {'error': str(e)}
    
    def get_platform_analysis(self) -> Dict[str, Any]:
        """Analyze performance by platform"""
        try:
            apps = self.analytics_data['applications']
            platform_data = defaultdict(list)
            
            for app in apps:
                platform_data[app['platform']].append(app)
            
            analysis = {}
            for platform, applications in platform_data.items():
                submitted = sum(
                    1 for app in applications 
                    if app['status'] in ['Submitted', 'Form Filled']
                )
                
                analysis[platform] = {
                    'total': len(applications),
                    'submitted': submitted,
                    'success_rate': submitted / len(applications) * 100,
                    'statuses': defaultdict(int),
                }
                
                for app in applications:
                    analysis[platform]['statuses'][app['status']] += 1
            
            return dict(analysis)
        except Exception as e:
            self.logger.error(f"Error generating platform analysis: {str(e)}")
            return {}
    
    def get_company_analysis(self) -> Dict[str, Any]:
        """Analyze performance by company"""
        try:
            apps = self.analytics_data['applications']
            company_data = defaultdict(list)
            
            for app in apps:
                company_data[app['company']].append(app)
            
            analysis = {}
            for company, applications in company_data.items():
                submitted = sum(
                    1 for app in applications 
                    if app['status'] in ['Submitted', 'Form Filled']
                )
                
                analysis[company] = {
                    'total': len(applications),
                    'submitted': submitted,
                    'success_rate': submitted / len(applications) * 100 if applications else 0,
                    'roles': [app['job_title'] for app in applications],
                }
            
            return dict(analysis)
        except Exception as e:
            self.logger.error(f"Error generating company analysis: {str(e)}")
            return {}
    
    def get_timeline_analysis(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get applications submitted over time"""
        try:
            apps = self.analytics_data['applications']
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Group by date
            date_counts = defaultdict(lambda: defaultdict(int))
            
            for app in apps:
                app_date = datetime.fromisoformat(app['timestamp'])
                if app_date >= cutoff_date:
                    date_str = app_date.date().isoformat()
                    date_counts[date_str][app['status']] += 1
            
            # Convert to sorted list
            timeline = []
            for date_str in sorted(date_counts.keys()):
                timeline.append({
                    'date': date_str,
                    'statuses': dict(date_counts[date_str]),
                    'total': sum(date_counts[date_str].values()),
                })
            
            return timeline
        except Exception as e:
            self.logger.error(f"Error generating timeline: {str(e)}")
            return []
    
    def export_report(self, filename: str = None) -> str:
        """Export comprehensive analytics report"""
        try:
            if filename is None:
                filename = os.path.join(
                    self.config.get_output_dirs()['logs_dir'],
                    f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )
            
            report = {
                'generated_at': datetime.now().isoformat(),
                'summary': self.get_summary_statistics(),
                'by_platform': self.get_platform_analysis(),
                'by_company': self.get_company_analysis(),
                'timeline': self.get_timeline_analysis(),
                'raw_data': self.analytics_data,
            }
            
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            
            self.logger.info(f"Analytics report exported: {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Error exporting report: {str(e)}")
            return ""
    
    def _save_analytics(self):
        """Save analytics data to file"""
        try:
            with open(self.analytics_file, 'w') as f:
                json.dump(self.analytics_data, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Could not save analytics: {str(e)}")
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get data for dashboard display"""
        summary = self.get_summary_statistics()
        if 'error' in summary or summary.get('status') == 'no_data':
            return summary
        
        return {
            'summary': summary,
            'platform_stats': self.get_platform_analysis(),
            'top_companies': sorted(
                self.get_company_analysis().items(),
                key=lambda x: x[1]['total'],
                reverse=True
            )[:5],
            'recent_applications': self.analytics_data['applications'][-10:],
        }
