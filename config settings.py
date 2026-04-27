"""Configuration settings for the test framework."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration."""
    
    # Base URLs
    BASE_URL: str = os.getenv('BASE_URL', 'https://skyeng-test-api.ru')
    UI_BASE_URL: str = os.getenv('UI_BASE_URL', 'https://teacher.skyeng.ru')
    
    # API Configuration
    API_TOKEN: Optional[str] = os.getenv('API_TOKEN')
    API_VERSION: str = os.getenv('API_VERSION', 'v1')
    
    # Test credentials
    TEST_EMAIL: str = os.getenv('TEST_EMAIL', 'test_teacher@skyeng.ru')
    TEST_PASSWORD: str = os.getenv('TEST_PASSWORD', 'TestPassword123')
    
    # Test data
    TEST_USER_ID: int = int(os.getenv('TEST_USER_ID', '12345'))
    TEST_SCHOOL_ID: int = int(os.getenv('TEST_SCHOOL_ID', '6789'))
    
    # Timeouts
    DEFAULT_TIMEOUT: int = int(os.getenv('DEFAULT_TIMEOUT', '10'))
    IMPLICIT_WAIT: int = int(os.getenv('IMPLICIT_WAIT', '5'))
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    REPORTS_DIR: Path = BASE_DIR / 'reports'
    DATA_DIR: Path = BASE_DIR / 'data'
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        cls.REPORTS_DIR.mkdir(exist_ok=True)
        cls.DATA_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def get_api_url(cls, endpoint: str) -> str:
        """Get full API URL for endpoint."""
        return f"{cls.BASE_URL}/{cls.API_VERSION}{endpoint}"

# Initialize directories
Settings.ensure_directories()