"""UI tests for personal events functionality based on manual testing checklist."""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import allure
from config.settings import Settings
from pages.login_page import LoginPage
from pages.calendar_page import CalendarPage
from faker import Faker

fake = Faker()

@allure.epic("Personal Events UI Testing")
@allure.feature("Calendar UI Tests")
class TestPersonalEventsUI:
    """Test suite for personal events UI based on manual testing checklist."""
    
    @pytest.fixture
    def driver(self):
        """Setup WebDriver instance."""
        with allure.step("Initialize Chrome WebDriver"):
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            driver.implicitly_wait(Settings.IMPLICIT_WAIT)
        
        yield driver
        
        with allure.step("Close WebDriver"):
            driver.quit()
    
    @pytest.fixture
    def logged_in_driver(self, driver):
        """Setup logged in driver instance."""
        with allure.step("Login to application"):
            login_page = LoginPage(driver)
            driver.get(Settings.UI_BASE_URL)
            login_page.login(Settings.TEST_EMAIL, Settings.TEST_PASSWORD)
            
            # Wait for login to complete
            assert login_page.is_login_successful(), "Login failed"
        
        yield driver
    
    @allure.title("UI: Create personal event with valid data")
    @allure.story("Create Event")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_create_personal_event_valid_data(self, logged_in_driver) -> None:
        """Test creating a personal event with valid data."""
        calendar_page = CalendarPage(logged_in_driver)
        event_title = fake.sentence(nb_words=3)[:40]
        
        with allure.step("Open add event modal"):
            calendar_page.open_add_event_modal()
        
        with allure.step("Fill event details"):
            calendar_page.create_personal_event(
                title=event_title,
                description="Test event description",
                start_time="14:00",
                end_time="15:00",
                color="blue"
            )
        
        with allure.step("Verify event was created"):
            assert calendar_page.is_event_present(event_title), \
                f"Event '{event_title}' should be visible on calendar"
        
        with allure.step("Verify success message appears"):
            assert calendar_page.is_element_visible(
                calendar_page.SUCCESS_TOAST, timeout=5
            ), "Success message should be displayed"
    
    @allure.title("UI: Create event with title exceeding 40 characters")
    @allure.story("Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    @pytest.mark.regression
    @pytest.mark.p1
    def test_create_event_title_40_char_limit(self, logged_in_driver) -> None:
        """Test validation for event title length limit."""
        calendar_page = CalendarPage(logged_in_driver)
        long_title = "A" * 41  # 41 characters
        expected_error = "название события ограничено 40 символами"
        
        with allure.step("Open add event modal"):
            calendar_page.open_add_event_modal()
        
        with allure.step("Enter title longer than 40 characters"):
            calendar_page.set_event_title(long_title)
            calendar_page.set_event_time("14:00", "15:00")
            calendar_page.save_event()
        
        with allure.step("Verify error message is displayed"):
            error_message = calendar_page.get_error_message()
            assert expected_error in error_message or "40" in error_message, \
                f"Expected error about 40 char limit, got: {error_message}"
    
    @allure.title("UI: Edit personal event title")
    @allure.story("Edit Event")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_edit_personal_event_title(self, logged_in_driver) -> None:
        """Test editing an existing personal event title."""
        calendar_page = CalendarPage(logged_in_driver)
        original_title = fake.sentence(nb_words=3)[:30]
        new_title = f"Edited: {fake.sentence(nb_words=2)[:25]}"
        
        with allure.step("Create test event"):
            calendar_page.open_add_event_modal()
            calendar_page.create_personal_event(
                title=original_title,
                start_time="16:00",
                end_time="17:00"
            )
            assert calendar_page.is_event_present(original_title)
        
        with allure.step("Open event for editing"):
            calendar_page.click_on_event(original_title)
        
        with allure.step("Edit event title"):
            calendar_page.edit_event_title(new_title)
        
        with allure.step("Verify title was updated"):
            assert calendar_page.is_event_present(new_title), \
                f"Event with new title '{new_title}' should exist"
    
    @allure.title("UI: Delete personal event")
    @allure.story("Delete Event")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_delete_personal_event(self, logged_in_driver) -> None:
        """Test deleting a personal event."""
        calendar_page = CalendarPage(logged_in_driver)
        event_title = fake.sentence(nb_words=3)[:35]
        
        with allure.step("Create test event"):
            calendar_page.open_add_event_modal()
            calendar_page.create_personal_event(
                title=event_title,
                start_time="11:00",
                end_time="12:00"
            )
            assert calendar_page.is_event_present(event_title)
        
        with allure.step("Open event for deletion"):
            calendar_page.click_on_event(event_title)
        
        with allure.step("Delete the event"):
            calendar_page.delete_current_event()
        
        with allure.step("Verify event was deleted from calendar"):
            assert not calendar_page.is_event_present(event_title), \
                f"Event '{event_title}' should not exist after deletion"
            
            # Note: Based on manual testing, there's a bug P3
            # "Событие не удаляется из расписания после подтверждения удаления"
            # This test will fail until bug is fixed
    
    @allure.title("UI: Color selection for personal events")
    @allure.story("Color Marking")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    @pytest.mark.regression
    def test_event_color_selection(self, logged_in_driver) -> None:
        """Test different color options for events."""
        calendar_page = CalendarPage(logged_in_driver)
        colors = ["red", "blue", "green", "yellow", "purple"]
        
        for color in colors:
            event_title = f"Color test {color}"
            
            with allure.step(f"Create event with {color} color"):
                calendar_page.open_add_event_modal()
                calendar_page.create_personal_event(
                    title=event_title,
                    start_time="09:00",
                    end_time="10:00",
                    color=color
                )
                
                # Verify event created
                assert calendar_page.is_event_present(event_title)
                
                # Check color class on event
                event_locator = (By.XPATH, f"//div[@data-testid='event-item'][contains(@class, '{color}')]")
                assert calendar_page.is_element_present(event_locator), \
                    f"Event should have {color} color class"
                
                # Clean up
                calendar_page.click_on_event(event_title)
                calendar_page.delete_current_event()
    
    @allure.title("UI: Lessons priority over personal events")
    @allure.story("Display Priority")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    @pytest.mark.regression
    def test_lessons_displayed_above_events(self, logged_in_driver) -> None:
        """Test that lessons are displayed above personal events in the same time slot."""
        calendar_page = CalendarPage(logged_in_driver)
        
        with allure.step("Create personal event in a time slot"):
            calendar_page.open_add_event_modal()
            calendar_page.create_personal_event(
                title="Personal Event Priority Test",
                start_time="13:00",
                end_time="14:00"
            )
        
        with allure.step("Verify ordering of lessons vs events"):
            # This checks DOM order - lessons should come before events
            assert calendar_page.are_lessons_above_events(), \
                "Lessons should be displayed above personal events"