"""
Production-grade scheduling system with APScheduler.
Enables automated job application processing on a schedule.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Callable, Optional
import os

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.triggers.interval import IntervalTrigger
    SCHEDULER_AVAILABLE = True
except ImportError:
    SCHEDULER_AVAILABLE = False

class ScheduledJobManager:
    """
    Manages scheduled job application runs with:
    - Cron-based scheduling
    - Interval-based scheduling
    - Execution history tracking
    - Error handling and recovery
    - Multi-job support
    """
    
    def __init__(self, logger: logging.Logger, config: Any):
        self.logger = logger
        self.config = config
        self.scheduler = None
        self.execution_history = []
        self.job_runs = {}
        self.max_history = 1000
        
        if SCHEDULER_AVAILABLE:
            self.scheduler = AsyncIOScheduler(
                job_defaults={
                    'coalesce': True,
                    'max_instances': 1,
                    'misfire_grace_time': 120,
                }
            )
        else:
            self.logger.warning("APScheduler not installed. Install: pip install apscheduler")

        self._load_execution_history()

    def _history_file(self) -> str:
        return os.path.join(self.config.get_output_dirs()['logs_dir'], 'execution_history.json')

    def _load_execution_history(self):
        """Load persisted history if available."""
        history_file = self._history_file()
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    self.execution_history = json.load(f)

                for record in self.execution_history[-50:]:
                    if isinstance(record, dict) and 'job_id' in record:
                        self.job_runs[record['job_id']] = record
        except Exception as e:
            self.logger.warning(f"Could not load execution history: {str(e)}")
            self.execution_history = []
    
    def schedule_daily_applications(
        self,
        hour: int = 9,
        minute: int = 0,
        callback: Optional[Callable] = None,
        job_id: str = "daily_applications"
    ) -> bool:
        """Schedule daily application runs at specified time"""
        try:
            if not self.scheduler:
                self.logger.error("Scheduler not initialized")
                return False
            
            self.logger.info(f"Scheduling daily applications at {hour:02d}:{minute:02d}")
            
            trigger = CronTrigger(hour=hour, minute=minute)
            
            self.scheduler.add_job(
                self._run_scheduled_job,
                trigger=trigger,
                args=[callback, job_id],
                id=job_id,
                name=f"Daily applications at {hour:02d}:{minute:02d}",
                replace_existing=True,
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Error scheduling daily applications: {str(e)}")
            return False
    
    def schedule_interval_applications(
        self,
        hours: int = 4,
        callback: Optional[Callable] = None,
        job_id: str = "interval_applications"
    ) -> bool:
        """Schedule applications to run every N hours"""
        try:
            if not self.scheduler:
                self.logger.error("Scheduler not initialized")
                return False
            
            self.logger.info(f"Scheduling applications every {hours} hours")
            
            trigger = IntervalTrigger(hours=hours)
            
            self.scheduler.add_job(
                self._run_scheduled_job,
                trigger=trigger,
                args=[callback, job_id],
                id=job_id,
                name=f"Applications every {hours} hours",
                replace_existing=True,
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Error scheduling interval applications: {str(e)}")
            return False
    
    def schedule_custom_cron(
        self,
        cron_expression: str,
        callback: Optional[Callable] = None,
        job_id: str = "custom_cron"
    ) -> bool:
        """Schedule applications using custom cron expression"""
        try:
            if not self.scheduler:
                self.logger.error("Scheduler not initialized")
                return False
            
            self.logger.info(f"Scheduling applications with cron: {cron_expression}")
            
            # Parse cron expression (format: minute hour day month weekday)
            parts = cron_expression.split()
            if len(parts) != 5:
                raise ValueError("Cron expression must have 5 parts (minute hour day month weekday)")
            
            trigger = CronTrigger(
                minute=parts[0],
                hour=parts[1],
                day=parts[2],
                month=parts[3],
                day_of_week=parts[4]
            )
            
            self.scheduler.add_job(
                self._run_scheduled_job,
                trigger=trigger,
                args=[callback, job_id],
                id=job_id,
                name=f"Custom cron: {cron_expression}",
                replace_existing=True,
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Error scheduling custom cron: {str(e)}")
            return False
    
    async def _run_scheduled_job(self, callback: Optional[Callable], job_id: str):
        """Internal handler for scheduled job execution"""
        start_time = datetime.now()
        execution_record = {
            'job_id': job_id,
            'start_time': start_time.isoformat(),
            'status': 'running',
        }

        try:
            self.logger.info(f"Starting scheduled job: {job_id}")

            # Execute callback if provided
            if callback:
                if asyncio.iscoroutinefunction(callback):
                    result = await callback()
                else:
                    result = callback()
                    if asyncio.iscoroutine(result):
                        result = await result

                execution_record['result'] = result
            execution_record['status'] = 'completed'
            
            end_time = datetime.now()
            execution_record['end_time'] = end_time.isoformat()
            execution_record['duration_seconds'] = (end_time - start_time).total_seconds()

            self.execution_history.append(execution_record)
            self.execution_history = self.execution_history[-self.max_history:]
            self.job_runs[job_id] = execution_record
            
            self.logger.info(
                f"Scheduled job completed: {job_id} "
                f"({execution_record['duration_seconds']:.1f}s)"
            )
            
            # Save execution history
            await self._save_execution_history()
            
        except Exception as e:
            self.logger.error(f"Error executing scheduled job {job_id}: {str(e)}")
            execution_record['status'] = 'failed'
            execution_record['error'] = str(e)
            execution_record['end_time'] = datetime.now().isoformat()

            self.execution_history.append(execution_record)
            self.execution_history = self.execution_history[-self.max_history:]
            self.job_runs[job_id] = execution_record

            await self._save_execution_history()
    
    async def start_scheduler(self):
        """Start the scheduler"""
        try:
            if not self.scheduler:
                self.logger.error("Scheduler not initialized")
                return False
            
            if not self.scheduler.running:
                self.scheduler.start()
                self.logger.info("Scheduler started")
                return True
            else:
                self.logger.warning("Scheduler already running")
                return True
        except Exception as e:
            self.logger.error(f"Error starting scheduler: {str(e)}")
            return False
    
    async def stop_scheduler(self):
        """Stop the scheduler"""
        try:
            if self.scheduler and self.scheduler.running:
                self.scheduler.shutdown(wait=True)
                self.logger.info("Scheduler stopped")
                return True
        except Exception as e:
            self.logger.error(f"Error stopping scheduler: {str(e)}")
            return False
    
    def list_scheduled_jobs(self) -> list:
        """List all scheduled jobs"""
        try:
            if not self.scheduler:
                return []
            
            jobs = []
            for job in self.scheduler.get_jobs():
                jobs.append({
                    'id': job.id,
                    'name': job.name,
                    'trigger': str(job.trigger),
                    'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                })
            
            return jobs
        except Exception as e:
            self.logger.error(f"Error listing scheduled jobs: {str(e)}")
            return []
    
    async def _save_execution_history(self):
        """Save execution history to file"""
        try:
            history_file = self._history_file()
            
            with open(history_file, 'w') as f:
                json.dump(self.execution_history, f, indent=2)
            
            self.logger.debug(f"Execution history saved: {history_file}")
        except Exception as e:
            self.logger.warning(f"Could not save execution history: {str(e)}")
    
    def get_execution_history(self, limit: int = 100) -> list:
        """Get recent execution history"""
        return self.execution_history[-limit:]
    
    def get_job_stats(self) -> Dict[str, Any]:
        """Get statistics about scheduled job executions"""
        try:
            total_runs = len(self.execution_history)
            successful = sum(1 for r in self.execution_history if r['status'] == 'completed')
            failed = sum(1 for r in self.execution_history if r['status'] == 'failed')
            
            durations = [
                r['duration_seconds'] 
                for r in self.execution_history 
                if 'duration_seconds' in r
            ]
            
            avg_duration = sum(durations) / len(durations) if durations else 0
            
            return {
                'total_runs': total_runs,
                'successful': successful,
                'failed': failed,
                'success_rate': successful / total_runs * 100 if total_runs > 0 else 0,
                'avg_duration_seconds': avg_duration,
                'last_run': self.execution_history[-1] if self.execution_history else None,
            }
        except Exception as e:
            self.logger.error(f"Error calculating job stats: {str(e)}")
            return {}
