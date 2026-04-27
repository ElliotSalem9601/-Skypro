"""Calendar page object for managing personal events."""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import allure
from pages.base_page import BasePage

class CalendarPage(BasePage):
    """Calendar page object for personal events."""
    
    # Locators
    ADD_EVENT_BUTTON = (By.CSS_SELECTOR, "[data-testid='add-event-button']")
    EVENT_TITLE_INPUT = (By.CSS_SELECTOR, "[data-testid='event-title-input']")
    EVENT_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "[data-testid='event-description-input']")
    EVENT_START_TIME = (By.CSS_SELECTOR, "[data-testid='event-start-time']")
    EVENT_END_TIME = (By.CSS_SELECTOR, "[data-testid='event-end-time']")
    EVENT_COLOR_PICKER = (By.CSS_SELECTOR, "[data-testid='event-color-picker']")
    SAVE_EVENT_BUTTON = (By.CSS_SELECTOR, "[data-testid='save-event-button']")
    DELETE_EVENT_BUTTON = (By.CSS_SELECTOR, "[data-testid='delete-event-button']")
    CONFIRM_DELETE_BUTTON = (By.CSS_SELECTOR, "[data-testid='confirm-delete']")
    EVENT_ITEM = (By.CSS_SELECTOR, "[data-testid='event-item']")
    EVENT_TITLE_TEXT = (By.CSS_SELECTOR, "[data-testid='event-title']")
    CALENDAR_CELL = (By.CSS_SELECTOR, "[data-testid='calendar-cell']")
    ERROR_TOAST = (By.CSS_SELECTOR, "[data-testid='error-toast']")
    SUCCESS_TOAST = (By.CSS_SELECTOR, "[data-testid='success-toast']")
    EVENT_MODAL = (By.CSS_SELECTOR, "[data-testid='event-modal']")
    
    @allure.step("Open add event modal")
    def open_add_event_modal(self, time_slot: Optional[datetime] = None) -> None:
        """
        Open the add event modal by clicking on a time slot.
        
        Args:
            time_slot: Specific time slot to click (optional)
        """
        if time_slot:
            # Click specific time slot
            slot_locator = (By.CSS_SELECTOR, f"[data-time='{time_slot.strftime('%H:%M')}']")
            self.click(slot_locator)
        else:
            self.click(self.ADD_EVENT_BUTTON)
    
    @allure.step("Set event title: {title}")
    def set_event_title(self, title: str) -> None:
        """
        Set event title.
        
        Args:
            title: Event title (max 40 characters)
        """
        self.input_text(self.EVENT_TITLE_INPUT, title)
    
    @allure.step("Set event description: {description}")
    def set_event_description(self, description: str) -> None:
        """
        Set event description with markdown support.
        
        Args:
            description: Event description text
        """
        self.input_text(self.EVENT_DESCRIPTION_INPUT, description)
    
    @allure.step("Set event time: start={start_time}, end={end_time}")
    def set_event_time(self, start_time: str, end_time: str) -> None:
        """
        Set event start and end times.
        
        Args:
            start_time: Start time in format "HH:MM"
            end_time: End time in format "HH:MM"
        """
        self.input_text(self.EVENT_START_TIME, start_time)
        self.input_text(self.EVENT_END_TIME, end_time)
    
    @allure.step("Select event color: {color}")
    def select_event_color(self, color: str) -> None:
        """
        Select color for the event.
        
        Args:
            color: Color name (e.g., "red", "blue", "green")
        """
        self.click(self.EVENT_COLOR_PICKER)
        color_option = (By.CSS_SELECTOR, f"[data-color='{color}']")
        self.click(color_option)
    
    @allure.step("Save event")
    def save_event(self) -> None:
        """Save the event."""
        self.click(self.SAVE_EVENT_BUTTON)
    
    @allure.step("Create new personal event")
    def create_personal_event(self, title: str, description: str = "", 
                              start_time: str = "10:00", end_time: str = "11:00",
                              color: str = "gray") -> None:
        """
        Create a new personal event.
        
        Args:
            title: Event title
            description: Event description
            start_time: Start time
            end_time: End time
            color: Event color
        """
        self.set_event_title(title)
        if description:
            self.set_event_description(description)
        self.set_event_time(start_time, end_time)
        if color != "gray":
            self.select_event_color(color)
        self.save_event()
    
    @allure.step("Click on event: {title}")
    def click_on_event(self, title: str) -> None:
        """
        Click on an existing event to open edit modal.
        
        Args:
            title: Event title to click
        """
        event_locator = (By.XPATH, f"//div[@data-testid='event-item']//span[text()='{title}']")
        self.click(event_locator)
    
    @allure.step("Delete current event")
    def delete_current_event(self) -> None:
        """Delete the currently opened event."""
        self.click(self.DELETE_EVENT_BUTTON)
        self.click(self.CONFIRM_DELETE_BUTTON)
    
    @allure.step("Edit event title: {new_title}")
    def edit_event_title(self, new_title: str) -> None:
        """
        Edit event title.
        
        Args:
            new_title: New event title
        """
        self.set_event_title(new_title)
        self.save_event()
    
    @allure.step("Check if event exists: {title}")
    def is_event_present(self, title: str) -> bool:
        """
        Check if an event with given title exists.
        
        Args:
            title: Event title to check
            
        Returns:
            True if event exists, False otherwise
        """
        event_locator = (By.XPATH, f"//div[@data-testid='event-item']//span[text()='{title}']")
        return self.is_element_present(event_locator)
    
    @allure.step("Get all event titles")
    def get_all_event_titles(self) -> List[str]:
        """
        Get titles of all events on the calendar.
        
        Returns:
            List of event titles
        """
        events = self.find_elements(self.EVENT_ITEM)
        titles = []
        for event in events:
            title_elem = event.find_element(*self.EVENT_TITLE_TEXT)
            titles.append(title_elem.text)
        return titles
    
    @allure.step("Check if lessons appear above personal events")
    def are_lessons_above_events(self) -> bool:
        """
        Verify that lessons are displayed above personal events.
        
        Returns:
            True if lessons are above events, False otherwise
        """
        # This would check the DOM order
        calendar_items = self.find_elements(self.CALENDAR_CELL)
        lesson_found = False
        event_found = False
        
        for item in calendar_items:
            if "lesson" in item.get_attribute("class"):
                lesson_found = True
            if "personal-event" in item.get_attribute("class") and lesson_found:
                event_found = True
                break
        
        return lesson_found and event_found
    
    @allure.step("Get error message text")
    def get_error_message(self) -> str:
        """
        Get error message from toast notification.
        
        Returns:
            Error message text
        """
        return self.get_text(self.ERROR_TOAST)
    
    @allure.step("Check if event modal is visible")
    def is_event_modal_visible(self) -> bool:
        """
        Check if event modal is visible.
        
        Returns:
            True if modal is visible, False otherwise
        """
        return self.is_element_visible(self.EVENT_MODAL, timeout=5)