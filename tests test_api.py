"""API tests for personal events functionality based on manual testing requirements."""

import pytest
import allure
from datetime import datetime, timedelta
from typing import Dict, Any
from config.settings import Settings
from utils.api_client import APIClient
from faker import Faker

fake = Faker()

@allure.epic("Personal Events API Testing")
@allure.feature("CRUD Operations for Personal Events")
class TestPersonalEventsAPI:
    """Test suite for personal events API based on manual testing test cases."""
    
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        """Setup test fixtures."""
        self.client = APIClient()
        self.test_user_id = Settings.TEST_USER_ID
        
        # Test data
        self.valid_event_title = "Test Meeting"
        self.long_title = "A" * 41  # 41 characters
        self.valid_start_time = datetime.now().isoformat()
        self.valid_end_time = (datetime.now() + timedelta(hours=1)).isoformat()
    
    @allure.title("API: Create personal event with valid data")
    @allure.story("Create Event")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_create_personal_event_valid_data(self) -> None:
        """Test creating a personal event with valid data."""
        event_data = {
            "title": self.valid_event_title,
            "startTime": self.valid_start_time,
            "endTime": self.valid_end_time,
            "description": "This is a test event",
            "color": "blue"
        }
        
        with allure.step("Send request to create event"):
            response = self.client.post("/events", json=event_data)
        
        with allure.step("Verify response status code is 201"):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        with allure.step("Verify response contains event data"):
            created_event = response.json()
            assert "id" in created_event, "Event ID should be returned"
            assert created_event["title"] == event_data["title"]
            assert created_event["color"] == event_data["color"]
    
    @allure.title("API: Create event with title exceeding 40 characters")
    @allure.story("Create Event Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.p1
    def test_create_event_title_exceeds_40_chars(self) -> None:
        """Test creating event with title longer than 40 characters."""
        event_data = {
            "title": self.long_title,
            "startTime": self.valid_start_time,
            "endTime": self.valid_end_time,
            "description": "Test description"
        }
        
        with allure.step("Send request with too long title"):
            response = self.client.post("/events", json=event_data)
        
        with allure.step("Verify error response (400 or truncation)"):
            # According to manual testing, system should return error or truncate
            assert response.status_code in [400, 422], \
                f"Expected error status code, got {response.status_code}"
            
            if response.status_code == 400:
                error_data = response.json()
                assert "error" in error_data or "message" in error_data
    
    @allure.title("API: Create event in the past (backdating)")
    @allure.story("Create Event - Backdating")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_event_in_past(self) -> None:
        """Test creating an event with a past date (requirement for Anastasia Petrova)."""
        past_time = (datetime.now() - timedelta(days=7)).isoformat()
        end_time = (datetime.now() - timedelta(days=7, hours=-1)).isoformat()
        
        event_data = {
            "title": "Past event test",
            "startTime": past_time,
            "endTime": end_time,
            "description": "Event created backdated"
        }
        
        with allure.step("Send request to create past-dated event"):
            response = self.client.post("/events", json=event_data)
        
        with allure.step("Verify past-dated event creation is allowed"):
            # According to manual testing requirements, backdating is allowed
            assert response.status_code == 201, \
                f"Backdating should be allowed, got {response.status_code}"
            
            if response.status_code == 201:
                event = response.json()
                assert event["startTime"] == past_time
    
    @allure.title("API: Edit personal event")
    @allure.story("Edit Event")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_edit_personal_event(self) -> None:
        """Test editing an existing personal event."""
        # First create an event
        with allure.step("Create test event via API"):
            create_response = self.client.post("/events", json={
                "title": "Original Title",
                "startTime": self.valid_start_time,
                "endTime": self.valid_end_time,
                "description": "Original description"
            })
            assert create_response.status_code == 201
            event_id = create_response.json()["id"]
        
        # Then edit it
        with allure.step("Edit the created event"):
            update_data = {
                "title": "Updated Title",
                "description": "Updated description"
            }
            update_response = self.client.put(f"/events/{event_id}", json=update_data)
        
        with allure.step("Verify edit was successful"):
            assert update_response.status_code == 200, \
                f"Expected 200, got {update_response.status_code}"
            updated_event = update_response.json()
            assert updated_event["title"] == "Updated Title"
    
    @allure.title("API: Delete personal event")
    @allure.story("Delete Event")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.p0
    def test_delete_personal_event(self) -> None:
        """Test deleting a personal event."""
        # Create an event first
        with allure.step("Create test event for deletion"):
            create_response = self.client.post("/events", json={
                "title": "Event to Delete",
                "startTime": self.valid_start_time,
                "endTime": self.valid_end_time
            })
            assert create_response.status_code == 201
            event_id = create_response.json()["id"]
        
        # Delete the event
        with allure.step("Delete the created event"):
            delete_response = self.client.delete(f"/events/{event_id}")
        
        with allure.step("Verify event was deleted"):
            assert delete_response.status_code in [200, 204], \
                f"Expected 200/204, got {delete_response.status_code}"
        
        # Verify event no longer exists
        with allure.step("Verify event no longer exists"):
            get_response = self.client.get(f"/events/{event_id}")
            assert get_response.status_code == 404, \
                "Event should not exist after deletion"
    
    @allure.title("API: Get events with time conflict")
    @allure.story("Event Conflicts")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_event_time_conflict(self) -> None:
        """Test creating events with overlapping times."""
        # Create first event
        with allure.step("Create first event"):
            start_time = datetime.now().isoformat()
            end_time = (datetime.now() + timedelta(hours=2)).isoformat()
            
            response1 = self.client.post("/events", json={
                "title": "First Event",
                "startTime": start_time,
                "endTime": end_time
            })
            assert response1.status_code == 201
        
        # Try to create overlapping event
        with allure.step("Attempt to create overlapping event"):
            overlap_start = (datetime.now() + timedelta(hours=1)).isoformat()
            overlap_end = (datetime.now() + timedelta(hours=3)).isoformat()
            
            response2 = self.client.post("/events", json={
                "title": "Overlapping Event",
                "startTime": overlap_start,
                "endTime": overlap_end
            })
        
        with allure.step("Verify conflict handling"):
            # System should either prevent conflict or allow with warning
            if response2.status_code == 409:
                assert "conflict" in response2.json().get("message", "").lower()
    
    @allure.title("API: Change event time updates event ID")
    @allure.story("Event ID Management")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_change_event_time_updates_id(self) -> None:
        """Test that changing event end time may change event ID."""
        # Create event
        with allure.step("Create initial event"):
            start_time = datetime.now().isoformat()
            end_time = (datetime.now() + timedelta(hours=1)).isoformat()
            
            create_response = self.client.post("/events", json={
                "title": "Time Change Test",
                "startTime": start_time,
                "endTime": end_time
            })
            assert create_response.status_code == 201
            original_event = create_response.json()
            original_id = original_event["id"]
        
        # Change end time
        with allure.step("Change event end time"):
            new_end_time = (datetime.now() + timedelta(hours=2)).isoformat()
            update_response = self.client.put(f"/events/{original_id}", json={
                "endTime": new_end_time
            })
        
        with allure.step("Verify ID may change based on backend logic"):
            assert update_response.status_code == 200
            updated_event = update_response.json()
            # Note: Based on manual testing, ID may change when time changes
            allure.attach(
                f"Original ID: {original_id}, Updated ID: {updated_event.get('id', original_id)}",
                name="ID Change Info",
                attachment_type=allure.attachment_type.TEXT
            )