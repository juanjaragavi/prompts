import os
import yaml
from typing import Dict, Any

class Config:
    """Load and validate configuration from config.yaml"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance
    
    def _load(self):
        """Load YAML config file"""
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(config_path, "r") as f:
            self.data = yaml.safe_load(f)
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """Create output directories if they don't exist"""
        dirs = [
            self.data["output"]["screenshots_dir"],
            self.data["output"]["status_dir"],
            self.data["output"]["logs_dir"],
        ]
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
    
    def get_candidate(self) -> Dict[str, Any]:
        """Get candidate profile data"""
        return self.data["candidate"]
    
    def get_resume_path(self, variant: str = "master") -> str:
        """Get resume file path by variant"""
        return self.data["resumes"].get(variant, self.data["resumes"]["master"])
    
    def get_document_path(self, doc_type: str) -> str:
        """Get document file path"""
        return self.data["documents"].get(doc_type)
    
    def get_platform_config(self, platform_name: str) -> Dict[str, Any]:
        """Get platform-specific configuration"""
        return self.data["platforms"].get(platform_name)
    
    def get_all_platforms(self) -> Dict[str, Any]:
        """Get all platform configurations"""
        return self.data["platforms"]
    
    def get_essay_template(self, template_name: str) -> str:
        """Get essay template by name"""
        return self.data["essay_templates"].get(template_name, "")
    
    def get_browser_config(self) -> Dict[str, Any]:
        """Get browser configuration"""
        return self.data["browser"]
    
    def get_output_dirs(self) -> Dict[str, str]:
        """Get output directory paths"""
        return self.data["output"]
    
    def get_anti_patterns(self) -> Dict[str, Any]:
        """Get anti-patterns for error detection"""
        return self.data["anti_patterns"]
    
    def get_candidate_detail(self, key: str, default: str = "") -> str:
        """Get detailed candidate information by key"""
        return self.data["candidate"].get(key, default)
    
    def get_core_expertise(self) -> list:
        """Get Juan's core expertise areas"""
        return self.data["candidate"].get("core_expertise", [])
    
    def get_technical_skills(self) -> Dict[str, Any]:
        """Get detailed technical skills by category"""
        return self.data["candidate"].get("technical_skills", {})
    
    def get_key_projects(self) -> list:
        """Get TopNetworks key projects"""
        return self.data["candidate"].get("key_projects", [])
    
    def get_positioning(self) -> Dict[str, str]:
        """Get professional positioning"""
        return {
            "headline": self.data["candidate"].get("positioning_headline"),
            "title": self.data["candidate"].get("professional_title"),
            "summary_short": self.data["candidate"].get("summary_short"),
            "summary_long": self.data["candidate"].get("summary_long"),
        }
    
    def get_compensation_target(self) -> Dict[str, str]:
        """Get compensation expectations"""
        return {
            "monthly_usd": self.data["candidate"].get("target_monthly_usd"),
            "annual_usd": self.data["candidate"].get("target_annual_usd"),
            "range_monthly": self.data["candidate"].get("target_range_monthly"),
            "range_annual": self.data["candidate"].get("target_range_annual"),
        }
    
    def get_work_authorization(self) -> Dict[str, Any]:
        """Get work authorization details"""
        return {
            "citizenship": self.data["candidate"].get("citizenship"),
            "based_in": self.data["candidate"].get("based_in"),
            "colombia": self.data["candidate"].get("work_auth_colombia"),
            "us": self.data["candidate"].get("work_auth_us"),
            "eu": self.data["candidate"].get("work_auth_eu"),
            "requires_sponsorship": self.data["candidate"].get("requires_visa_sponsorship"),
        }
    
    def get_language_proficiency(self) -> Dict[str, str]:
        """Get language proficiency details"""
        return {
            "native": self.data["candidate"].get("native_language"),
            "english_level": self.data["candidate"].get("english_level"),
            "english_proficiency": self.data["candidate"].get("english_proficiency"),
            "efset_level": self.data["candidate"].get("efset_certification_level"),
            "efset_score": self.data["candidate"].get("efset_score_range"),
        }
    
    def get_job_search_config(self) -> Dict[str, Any]:
        """Get job search strategy and parameters"""
        return self.data.get("job_search", {})
    
    def get_execution_plan(self) -> Dict[str, str]:
        """Get 30-day execution plan reference"""
        return self.data.get("execution_plan", {})
