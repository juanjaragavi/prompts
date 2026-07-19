#!/usr/bin/env python3
"""
Scheduler runner for Phase 3 - Automated job application processing.
"""

import asyncio
import json
import logging
import sys
import os
from datetime import datetime

from hardened_bot import HardenedProductionBot
from config import Config

def setup_logging():
    """Setup application logging"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger("SchedulerRunner")
    logger.setLevel(logging.INFO)
    
    # File handler
    fh = logging.FileHandler(
        os.path.join(log_dir, f"scheduler_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)
    
    return logger

async def main():
    """Main scheduler runner"""
    logger = setup_logging()
    
    logger.info("=" * 70)
    logger.info("PHASE 3 JOB APPLICATION BOT - SCHEDULER RUNNER")
    logger.info("=" * 70)
    
    try:
        # Initialize bot
        config = Config()
        bot = HardenedProductionBot(config, logger)
        
        # Register default candidate (from config)
        logger.info("Loading candidate profile...")
        default_candidate = config.get_candidate()
        bot.register_candidate("default", default_candidate)
        logger.info(f"✓ Candidate registered: {default_candidate.get('full_name')}")
        
        # Load applications inventory
        inventory_file = "open_applications_inventory_expanded.json"
        if not os.path.exists(inventory_file):
            inventory_file = "open_applications_inventory.json"
        
        if not os.path.exists(inventory_file):
            logger.error(f"No inventory file found: {inventory_file}")
            return 1
        
        with open(inventory_file) as f:
            applications = json.load(f)
        logger.info(f"✓ Loaded {len(applications)} applications from {inventory_file}")
        
        # Show configuration menu
        logger.info("\n" + "=" * 70)
        logger.info("SCHEDULING OPTIONS")
        logger.info("=" * 70)
        logger.info("1. One-time batch run (process all applications now)")
        logger.info("2. Schedule daily runs (9 AM every day)")
        logger.info("3. Schedule every 4 hours")
        logger.info("4. Custom schedule (enter cron expression)")
        logger.info("=" * 70)
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == "1":
            # One-time run
            logger.info("\nStarting one-time batch run...")
            logger.info(f"Processing {len(applications)} applications...")
            
            results = await bot.process_batch(applications, candidate_name="default")
            
            # Summarize results
            logger.info("\n" + "=" * 70)
            logger.info("BATCH PROCESSING COMPLETE")
            logger.info("=" * 70)
            
            submitted = sum(1 for r in results if isinstance(r, dict) and r.get('status') == 'Submitted')
            failed = sum(1 for r in results if isinstance(r, dict) and r.get('status') in ['Failed', 'Error'])
            
            logger.info(f"Total processed: {len(results)}")
            logger.info(f"Submitted: {submitted}")
            logger.info(f"Failed: {failed}")
            
            # Export analytics
            report_file = bot.export_analytics()
            logger.info(f"Analytics report: {report_file}")
            
            logger.info("\n✓ One-time run complete")
            return 0
        
        elif choice == "2":
            # Daily schedule
            logger.info("\nScheduling daily runs at 09:00...")
            
            if not await bot.schedule_batch_runs(
                applications_file=inventory_file,
                schedule="daily",
                hour=9,
                minute=0,
                candidate_name="default"
            ):
                logger.error("Failed to schedule daily runs")
                return 1
            
            await bot.start_scheduler()
            logger.info("✓ Scheduler started - Daily runs scheduled at 09:00")
            
        elif choice == "3":
            # Every 4 hours
            logger.info("\nScheduling runs every 4 hours...")
            
            if not await bot.schedule_batch_runs(
                applications_file=inventory_file,
                schedule="every_4_hours",
                candidate_name="default"
            ):
                logger.error("Failed to schedule interval runs")
                return 1
            
            await bot.start_scheduler()
            logger.info("✓ Scheduler started - Runs scheduled every 4 hours")
        
        elif choice == "4":
            # Custom cron
            cron = input("Enter cron expression (minute hour day month weekday): ").strip()
            logger.info(f"\nScheduling with cron: {cron}")
            
            if not await bot.schedule_batch_runs(
                applications_file=inventory_file,
                schedule=cron,
                candidate_name="default"
            ):
                logger.error("Failed to schedule with custom cron")
                return 1
            
            await bot.start_scheduler()
            logger.info(f"✓ Scheduler started - Custom cron: {cron}")
        
        else:
            logger.error("Invalid option")
            return 1
        
        # Show active jobs
        jobs = bot.scheduler.list_scheduled_jobs()
        logger.info("\nActive Scheduled Jobs:")
        for job in jobs:
            logger.info(f"  - {job['id']}: {job['name']}")
            logger.info(f"    Next run: {job['next_run']}")
        
        # Keep scheduler running
        logger.info("\n" + "=" * 70)
        logger.info("SCHEDULER RUNNING - Press Ctrl+C to stop")
        logger.info("=" * 70)
        
        try:
            while True:
                await asyncio.sleep(60)
                
                # Show periodic status
                status = bot.get_status_summary()
                logger.debug(f"Status: {json.dumps(status, indent=2)}")
        
        except KeyboardInterrupt:
            logger.info("\nShutting down scheduler...")
            await bot.stop_scheduler()
            logger.info("✓ Scheduler stopped")
            return 0
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
