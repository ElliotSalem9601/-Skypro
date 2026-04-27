"""API client for testing Skyeng calendar API."""

import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
import allure
from config.settings import Settings

class APIClient:
    """HTTP client for Skyeng API testing."""
    
    def __init__(self, base_url: str = None, token: str = None):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API endpoints
            token: Authentication token
        """
        self.base_url = base_url or Settings.BASE_URL
        self.token = token or Settings.API_TOKEN
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        })
    
    @allure.step("GET request to {endpoint}")
    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """
        Perform GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        self._attach_response_details(response)
        return response
    
    @allure.step("POST request to {endpoint}")
    def post(self, endpoint: str, data: Optional[Dict] = None, 
             json: Optional[Dict] = None) -> requests.Response:
        """
        Perform POST request.
        
        Args:
            endpoint: API endpoint
            data: Form data
            json: JSON data
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, data=data, json=json)
        self._attach_response_details(response)
        return response
    
    @allure.step("PUT request to {endpoint}")
    def put(self, endpoint: str, json: Optional[Dict] = None) -> requests.Response:
        """
        Perform PUT request.
        
        Args:
            endpoint: API endpoint
            json: JSON data
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, json=json)
        self._attach_response_details(response)
        return response
    
    @allure.step("DELETE request to {endpoint}")
    def delete(self, endpoint: str) -> requests.Response:
        """
        Perform DELETE request.
        
        Args:
            endpoint: API endpoint
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url)
        self._attach_response_details(response)
        return response
    
    @allure.step("PATCH request to {endpoint}")
    def patch(self, endpoint: str, json: Optional[Dict] = None) -> requests.Response:
        """
        Perform PATCH request.
        
        Args:
            endpoint: API endpoint
            json: JSON data
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.patch(url, json=json)
        self._attach_response_details(response)
        return response
    
    def _attach_response_details(self, response: requests.Response) -> None:
        """
        Attach response details to Allure report.
        
        Args:
            response: Response object
        """
        allure.attach(
            str(response.status_code),
            name="Response Status Code",
            attachment_type=allure.attachment_type.TEXT
        )
        
        if response.text:
            try:
                allure.attach(
                    response.text,
                    name="Response Body",
                    attachment_type=allure.attachment_type.JSON
                )
            except:
                allure.attach(
                    response.text,
                    name="Response Body",
                    attachment_type=allure.attachment_type.TEXT
                )
    
    # Calendar-specific API methods
    @allure.step("Create personal event via API")
    def create_personal_event(self, title: str, start_time: str, end_time: str,
                              description: str = "", color: str = "gray",
                              user_id: int = None) -> Dict[str, Any]:
        """
        Create a personal event via API.
        
        Args:
            title: Event title (max 40 chars)
            start_time: Start time in ISO format
            end_time: End time in ISO format
            description: Event description
            color: Event color
            user_id: User ID
            
        Returns:
            Created event data
        """
        user_id = user_id or Settings.TEST_USER_ID
        event_data = {
            "userId": user_id,
            "title": title[:40],  # Enforce 40 char limit
            "startTime": start_time,
            "endTime": end_time,
            "description": description,
            "color": color
        }
        
        response = self.post("/events", json=event_data)
        assert response.status_code in [200, 201], f"Failed to create event: {response.text}"
        return response.json()
    
    @allure.step("Get personal events for user")
    def get_user_events(self, user_id: int = None, start_date: str = None, 
                        end_date: str = None) -> List[Dict[str, Any]]:
        """
        Get personal events for a user.
        
        Args:
            user_id: User ID
            start_date: Start date filter (ISO format)
            end_date: End date filter (ISO format)
            
        Returns:
            List of events
        """
        user_id = user_id or Settings.TEST_USER_ID
        params = {"userId": user_id}
        
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        
        response = self.get("/events", params=params)
        assert response.status_code == 200, f"Failed to get events: {response.text}"
        return response.json()
    
    @allure.step("Update personal event via API")
    def update_event(self, event_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a personal event via API.
        
        Args:
            event_id: Event ID
            update_data: Data to update
            
        Returns:
            Updated event data
        """
        response = self.put(f"/events/{event_id}", json=update_data)
        assert response.status_code == 200, f"Failed to update event: {response.text}"
        return response.json()
    
    @allure.step("Delete personal event via API")
    def delete_event(self, event_id: str) -> bool:
        """
        Delete a personal event via API.
        
        Args:
            event_id: Event ID
            
        Returns:
            True if deleted successfully
        """
        response = self.delete(f"/events/{event_id}")
        return response.status_code in [200, 204]