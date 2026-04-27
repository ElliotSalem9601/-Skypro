"""Base Page Object with common methods."""

from typing import Optional, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import allure

class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize BasePage.
        
        Args:
            driver: WebDriver instance
            timeout: Default timeout for waits in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    @allure.step("Open URL: {url}")
    def open(self, url: str) -> None:
        """
        Open a URL in the browser.
        
        Args:
            url: URL to open
        """
        self.driver.get(url)
    
    @allure.step("Find element: {locator}")
    def find_element(self, locator: tuple, timeout: Optional[int] = None) -> Optional[WebElement]:
        """
        Find a single element.
        
        Args:
            locator: Tuple of (By strategy, selector)
            timeout: Custom timeout for this operation
            
        Returns:
            WebElement if found, None otherwise
        """
        wait_timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, wait_timeout)
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="element_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            return None
    
    @allure.step("Find elements: {locator}")
    def find_elements(self, locator: tuple) -> List[WebElement]:
        """
        Find multiple elements.
        
        Args:
            locator: Tuple of (By strategy, selector)
            
        Returns:
            List of WebElements
        """
        return self.driver.find_elements(*locator)
    
    @allure.step("Click element: {locator}")
    def click(self, locator: tuple, timeout: Optional[int] = None) -> None:
        """
        Click on an element.
        
        Args:
            locator: Tuple of (By strategy, selector)
            timeout: Custom timeout for this operation
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    @allure.step("Input text '{text}' into element: {locator}")
    def input_text(self, locator: tuple, text: str, clear_first: bool = True) -> None:
        """
        Input text into an element.
        
        Args:
            locator: Tuple of (By strategy, selector)
            text: Text to input
            clear_first: Whether to clear the field first
        """
        element = self.find_element(locator)
        if element:
            if clear_first:
                element.clear()
            element.send_keys(text)
    
    @allure.step("Get text from element: {locator}")
    def get_text(self, locator: tuple) -> str:
        """
        Get text from an element.
        
        Args:
            locator: Tuple of (By strategy, selector)
            
        Returns:
            Text content of the element
        """
        element = self.find_element(locator)
        return element.text if element else ""
    
    @allure.step("Check if element is visible: {locator}")
    def is_element_visible(self, locator: tuple, timeout: Optional[int] = None) -> bool:
        """
        Check if an element is visible.
        
        Args:
            locator: Tuple of (By strategy, selector)
            timeout: Custom timeout for this operation
            
        Returns:
            True if visible, False otherwise
        """
        wait_timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, wait_timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    @allure.step("Check if element is present: {locator}")
    def is_element_present(self, locator: tuple) -> bool:
        """
        Check if element exists in DOM.
        
        Args:
            locator: Tuple of (By strategy, selector)
            
        Returns:
            True if present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    @allure.step("Wait for element to disappear: {locator}")
    def wait_for_disappear(self, locator: tuple, timeout: Optional[int] = None) -> bool:
        """
        Wait for element to disappear from DOM.
        
        Args:
            locator: Tuple of (By strategy, selector)
            timeout: Custom timeout for this operation
            
        Returns:
            True if disappeared, False if still present
        """
        wait_timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, wait_timeout)
            wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    @allure.step("Get current URL")
    def get_current_url(self) -> str:
        """
        Get current page URL.
        
        Returns:
            Current URL string
        """
        return self.driver.current_url
    
    @allure.step("Refresh page")
    def refresh_page(self) -> None:
        """Refresh the current page."""
        self.driver.refresh()