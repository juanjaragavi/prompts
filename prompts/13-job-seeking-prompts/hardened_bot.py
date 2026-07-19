"""
Production-grade hardened bot with Phase 3 enhancements.
Features: Puppeteer, scheduling, analytics, retry logic, state recovery, multi-candidate.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import time

# Import handlers
from puppeteer_handler import PuppeteerFormHandler, FormState
from scheduler_manager import ScheduledJobManager
from analytics_engine import AnalyticsEngine
from config import Config

class HardenedProductionBot:
    """
    Production-grade bot with:
    - Advanced Puppeteer form handling
    - Retry logic with exponential backoff
    - State management and recovery
    - Comprehensive analytics
    - Scheduled execution
    - Multi-candidate support
    - Health monitoring
    """
    
    def __init__(self, config: Optional[Config] = None, logger: Optional[logging.Logger] = None):
        self.config = config or Config()
        self.logger = logger or self._setup_logger()
        self.candidate_profiles: Dict[str, Dict[str, Any]] = {}
        self.scheduler = ScheduledJobManager(self.logger, self.config)
        self.analytics = AnalyticsEngine(
            self.logger,
            self.config,
            self.config.get_output_dirs()['status_dir']
        )
        self.active_sessions: Dict[str, Any] = {}
        self.max_retries = 3
        self.max_concurrent = 3
        job_search_cfg = self.config.get_job_search_config() or {}
        self.batch_timeout_seconds = int(job_search_cfg.get('batch_timeout_seconds', 1800))
    
    def _setup_logger(self) -> logging.Logger:
        """Setup structured logging"""
        log_dir = self.config.get_output_dirs()['logs_dir']
        os.makedirs(log_dir, exist_ok=True)
        
        logger = logging.getLogger("HardenedBot")
        logger.setLevel(logging.DEBUG)

        if logger.handlers:
            return logger
        
        handler = logging.FileHandler(
            os.path.join(log_dir, f"hardened_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        )
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(handler)
        
        return logger
    
    def register_candidate(self, name: str, profile: Dict[str, Any]) -> bool:
        """Register a candidate profile for multi-candidate support"""
        try:
            self.candidate_profiles[name] = profile
            self.logger.info(f"Registered candidate: {name}")
            return True
        except Exception as e:
            self.logger.error(f"Error registering candidate: {str(e)}")
            return False
    
    async def process_application(
        self,
        url: str,
        company: str,
        job_title: str,
        platform: str,
        candidate_name: str = "default",
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        Process single application with hardened retry logic.
        Returns: {status, details, duration, form_state}
        """
        start_time = time.time()
        candidate_data = self.candidate_profiles.get(candidate_name) or self.config.get_candidate()
        final_result: Dict[str, Any] = {
            'status': 'Error',
            'details': 'Unexpected failure',
            'duration': 0.0,
            'form_state': FormState.FAILED.value,
            'retries': retry_count,
        }

        for attempt in range(retry_count, self.max_retries + 1):
            handler = PuppeteerFormHandler(self.logger, self.config)
            try:
                self.logger.info(
                    f"Processing {company} - {job_title} (attempt {attempt + 1}/{self.max_retries + 1})"
                )

                if not await handler.load_page(url):
                    final_result = {
                        'status': 'Failed to Load',
                        'details': 'Could not load page',
                        'duration': time.time() - start_time,
                        'form_state': FormState.FAILED.value,
                        'retries': attempt,
                    }
                    if attempt < self.max_retries:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    break

                form_analysis = await handler.detect_form_fields_advanced()
                if not form_analysis:
                    final_result = {
                        'status': 'Form Detection Failed',
                        'details': 'Could not detect form fields',
                        'duration': time.time() - start_time,
                        'form_state': handler.state.value,
                        'retries': attempt,
                    }
                    if attempt < self.max_retries:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    break

                if not await handler.fill_form_intelligent(candidate_data):
                    final_result = {
                        'status': 'Form Filling Failed',
                        'details': 'Could not map or fill required fields',
                        'duration': time.time() - start_time,
                        'form_state': handler.state.value,
                        'retries': attempt,
                    }
                    if attempt < self.max_retries:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    break

                success, message = await handler.submit_form()
                final_result = {
                    'status': 'Submitted' if success else 'Submission Failed',
                    'details': message,
                    'duration': time.time() - start_time,
                    'form_state': handler.state.value,
                    'retries': attempt,
                }

                if success:
                    break

                if attempt < self.max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                break
            except Exception as exc:
                self.logger.error(f"Exception processing {company}: {exc}")
                final_result = {
                    'status': 'Error',
                    'details': str(exc),
                    'duration': time.time() - start_time,
                    'form_state': FormState.FAILED.value,
                    'retries': attempt,
                }
                if attempt < self.max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                break
            finally:
                await handler.cleanup()

        self.analytics.record_application(
            index=0,
            company=company,
            job_title=job_title,
            platform=platform,
            status=final_result['status'],
            details=final_result.get('details', ''),
            duration_seconds=final_result.get('duration', 0.0)
        )
        return final_result
    
    async def process_batch(
        self,
        applications: List[Dict[str, Any]],
        candidate_name: str = "default"
    ) -> List[Dict[str, Any]]:
        """
        Process batch of applications with concurrency control.
        Limits concurrent processing to avoid resource exhaustion.
        """
        self.logger.info(f"Processing batch of {len(applications)} applications")
        
        results: List[Dict[str, Any]] = []
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def process_with_semaphore(app):
            async with semaphore:
                required = ['url', 'company', 'job_title', 'platform']
                missing = [key for key in required if key not in app or not app.get(key)]
                if missing:
                    return {
                        'status': 'Invalid Application Data',
                        'details': f"Missing required fields: {', '.join(missing)}",
                        'duration': 0.0,
                        'form_state': FormState.FAILED.value,
                        'retries': 0,
                    }

                return await self.process_application(
                    url=app['url'],
                    company=app['company'],
                    job_title=app['job_title'],
                    platform=app['platform'],
                    candidate_name=candidate_name,
                )
        
        tasks = [asyncio.create_task(process_with_semaphore(app)) for app in applications]
        try:
            gathered = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=self.batch_timeout_seconds,
            )
        except asyncio.TimeoutError:
            self.logger.error(
                f"Batch processing timed out after {self.batch_timeout_seconds} seconds"
            )
            for task in tasks:
                if not task.done():
                    task.cancel()
            return [
                {
                    'status': 'Timeout',
                    'details': 'Batch timed out before completion',
                    'duration': 0.0,
                    'form_state': FormState.FAILED.value,
                    'retries': 0,
                }
                for _ in applications
            ]

        for item in gathered:
            if isinstance(item, Exception):
                results.append(
                    {
                        'status': 'Error',
                        'details': str(item),
                        'duration': 0.0,
                        'form_state': FormState.FAILED.value,
                        'retries': 0,
                    }
                )
            else:
                results.append(item)
        
        self.logger.info(f"Batch processing complete: {len(results)} applications")
        return results
    
    async def schedule_batch_runs(
        self,
        applications_file: str,
        schedule: str = "daily",
        hour: int = 9,
        minute: int = 0,
        candidate_name: str = "default"
    ) -> bool:
        """
        Schedule batch runs of applications.
        schedule: 'daily', 'hourly', 'every_4_hours', or cron expression
        """
        try:
            async def batch_callback():
                with open(applications_file, 'r') as f:
                    apps = json.load(f)
                return await self.process_batch(apps, candidate_name)
            
            if schedule == "daily":
                return self.scheduler.schedule_daily_applications(hour, minute, batch_callback)
            elif schedule == "hourly":
                return self.scheduler.schedule_interval_applications(hours=1, callback=batch_callback)
            elif schedule == "every_4_hours":
                return self.scheduler.schedule_interval_applications(hours=4, callback=batch_callback)
            elif schedule.count(' ') == 4:  # Cron expression
                return self.scheduler.schedule_custom_cron(schedule, batch_callback)
            else:
                self.logger.error(f"Unknown schedule format: {schedule}")
                return False
        
        except Exception as e:
            self.logger.error(f"Error scheduling batch runs: {str(e)}")
            return False
    
    async def start_scheduler(self) -> bool:
        """Start the scheduler for automated runs"""
        return await self.scheduler.start_scheduler()
    
    async def stop_scheduler(self) -> bool:
        """Stop the scheduler"""
        return await self.scheduler.stop_scheduler()
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get bot health and status information"""
        return {
            'timestamp': datetime.now().isoformat(),
            'candidates_registered': len(self.candidate_profiles),
            'active_sessions': len(self.active_sessions),
            'analytics': self.analytics.get_dashboard_summary(),
            'scheduled_jobs': self.scheduler.list_scheduled_jobs(),
            'job_stats': self.scheduler.get_job_stats(),
        }
    
    def export_analytics(self, filename: str = None) -> str:
        """Export comprehensive analytics report"""
        return self.analytics.export_report(filename)
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get quick status summary"""
        summary = self.analytics.get_summary_statistics()
        return {
            'timestamp': datetime.now().isoformat(),
            'total_applications_recorded': summary.get('total_applications', 0),
            'success_rate': summary.get('success_rate', 0),
            'active_scheduled_jobs': len(self.scheduler.list_scheduled_jobs()),
            'candidates': list(self.candidate_profiles.keys()),
        }
