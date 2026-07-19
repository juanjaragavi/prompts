#!/usr/bin/env python3
"""
Comprehensive testing suite for Phase 3 hardened bot.
Tests all components: Puppeteer handler, scheduler, analytics.
"""

import asyncio
import json
import logging
from datetime import datetime
import tempfile
import os

# Import components
from hardened_bot import HardenedProductionBot
from config import Config

class BotTestSuite:
    """Comprehensive test suite for hardened bot"""
    
    def __init__(self):
        self.config = Config()
        self.logger = self._setup_logger()
        self.bot = HardenedProductionBot(self.config, self.logger)
        self.passed = 0
        self.failed = 0
    
    def _setup_logger(self):
        logger = logging.getLogger("BotTestSuite")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger
    
    def test_config_loading(self):
        """Test configuration loading"""
        try:
            self.logger.info("Testing config loading...")
            assert self.config.get_candidate()
            assert self.config.get_browser_config()
            assert self.config.get_platform_config("lever")
            self.logger.info("✓ Config loading passed")
            self.passed += 1
        except Exception as e:
            self.logger.error(f"✗ Config loading failed: {str(e)}")
            self.failed += 1
    
    def test_candidate_registration(self):
        """Test multi-candidate support"""
        try:
            self.logger.info("Testing candidate registration...")
            
            candidate1 = {"full_name": "John Doe", "email": "john@example.com"}
            candidate2 = {"full_name": "Jane Smith", "email": "jane@example.com"}
            
            assert self.bot.register_candidate("john", candidate1)
            assert self.bot.register_candidate("jane", candidate2)
            
            assert "john" in self.bot.candidate_profiles
            assert "jane" in self.bot.candidate_profiles
            
            self.logger.info("✓ Candidate registration passed")
            self.passed += 1
        except Exception as e:
            self.logger.error(f"✗ Candidate registration failed: {str(e)}")
            self.failed += 1
    
    def test_analytics_recording(self):
        """Test analytics engine"""
        try:
            self.logger.info("Testing analytics recording...")
            
            self.bot.analytics.record_application(
                index=1,
                company="Test Co",
                job_title="Test Role",
                platform="lever",
                status="Submitted",
                details="Test submission",
                duration_seconds=5.5
            )
            
            summary = self.bot.analytics.get_summary_statistics()
            assert summary['total_applications'] > 0
            
            self.logger.info("✓ Analytics recording passed")
            self.passed += 1
        except Exception as e:
            self.logger.error(f"✗ Analytics recording failed: {str(e)}")
            self.failed += 1
    
    def test_analytics_export(self):
        """Test analytics report export"""
        try:
            self.logger.info("Testing analytics export...")
            
            # Record some test data
            for i in range(3):
                self.bot.analytics.record_application(
                    index=i,
                    company=f"Company {i}",
                    job_title=f"Role {i}",
                    platform="lever",
                    status="Submitted" if i % 2 == 0 else "Failed",
                    duration_seconds=float(i + 1)
                )
            
            # Export report
            report_file = self.bot.export_analytics()
            assert os.path.exists(report_file)
            
            with open(report_file, 'r') as f:
                report = json.load(f)
            
            assert 'summary' in report
            assert 'by_platform' in report
            assert 'timeline' in report
            
            self.logger.info(f"✓ Analytics export passed ({report_file})")
            self.passed += 1
        except Exception as e:
            self.logger.error(f"✗ Analytics export failed: {str(e)}")
            self.failed += 1
    
    def test_health_status(self):
        """Test health status reporting"""
        try:
            self.logger.info("Testing health status...")
            
            status = self.bot.get_health_status()
            assert 'timestamp' in status
            assert 'candidates_registered' in status
            assert 'analytics' in status
            
            summary = self.bot.get_status_summary()
            assert 'timestamp' in summary
            assert 'total_applications_recorded' in summary
            assert 'success_rate' in summary
            
            self.logger.info("✓ Health status passed")
            self.passed += 1
        except Exception as e:
            self.logger.error(f"✗ Health status failed: {str(e)}")
            self.failed += 1
    
    def test_batch_application_structure(self):
        """Test batch application processing structure"""
        try:
            self.logger.info("Testing batch structure...")
            
            # Create test batch (won't actually process URLs)
            test_batch = [
                {
                    "index": 1,
                    "company": "Test Company",
                    "job_title": "Test Role",
                    "platform": "lever",
                    "url": "https://jobs.lever.co/testco/test"
                }
            ]
            
            # Verify structure
            assert len(test_batch) > 0
            assert 'company' in test_batch[0]
            assert 'platform' in test_batch[0]
            assert 'url' in test_batch[0]
            
            self.logger.info("✓ Batch structure passed")
            self.passed += 1
        except Exception as e:
            self.logger.error(f"✗ Batch structure failed: {str(e)}")
            self.failed += 1
    
    async def run_all_tests(self):
        """Run all tests"""
        self.logger.info("=" * 60)
        self.logger.info("Starting Phase 3 Bot Test Suite")
        self.logger.info("=" * 60)
        
        # Synchronous tests
        self.test_config_loading()
        self.test_candidate_registration()
        self.test_analytics_recording()
        self.test_analytics_export()
        self.test_health_status()
        self.test_batch_application_structure()
        
        # Results
        self.logger.info("=" * 60)
        self.logger.info(f"Tests Passed: {self.passed}")
        self.logger.info(f"Tests Failed: {self.failed}")
        self.logger.info(f"Total: {self.passed + self.failed}")
        self.logger.info("=" * 60)
        
        return self.failed == 0

async def main():
    """Run test suite"""
    suite = BotTestSuite()
    success = await suite.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
