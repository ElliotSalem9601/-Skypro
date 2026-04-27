"""Login page object for Skyeng teacher portal."""

from selenium.webdriver.common.by import By
import allure
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Login page object."""
    
    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    
    @allure.step("Enter email: {email}")
    def enter_email(self, email: str) -> None:
        """
        Enter email in the login field.
        
        Args:
            email: User email address
        """
        self.input_text(self.EMAIL_INPUT, email)
    
    @allure.step("Enter password")
    def enter_password(self, password: str) -> None:
        """
        Enter password in the password field.
        
        Args:
            password: User password
        """
        self.input_text(self.PASSWORD_INPUT, password)
    
    @allure.step("Click login button")
    def click_login_button(self) -> None:
        """Click the login button."""
        self.click(self.LOGIN_BUTTON)
    
    @allure.step("Login with credentials")
    def login(self, email: str, password: str) -> None:
        """
        Complete login process.
        
        Args:
            email: User email
            password: User password
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
    
    @allure.step("Get error message")
    def get_error_message(self) -> str:
        """
        Get error message text.
        
        Returns:
            Error message text
        """
        return self.get_text(self.ERROR_MESSAGE)
    
    @allure.step("Check if login was successful")
    def is_login_successful(self) -> bool:
        """
        Check if login was successful by checking URL change.
        
        Returns:
            True if login successful, False otherwise
        """
        return "/dashboard" in self.get_current_url() or "/calendar" in self.get_current_url()