import os
import requests

class cms:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("CMS_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided or found in environment variables")

        self.base_url = self._get_ngrok_link()
        self.validate_key_url = f"{self.base_url}/validate_key"
        self.check_image_url = f"{self.base_url}/check_image"

    def _get_ngrok_link(self):
        # Fetch the ngrok link from the provided URL
        response = requests.get("https://gist.githubusercontent.com/TanmayDoesAI/37c473526f8cdaf2b6e96c5029bd52a6/raw/")
        response.raise_for_status()
        ngrok_link = response.text.strip()
        return ngrok_link

    def validate_key(self):
        # Send API key to the validate endpoint
        response = requests.post(self.validate_key_url, json={"key": self.api_key})
        response.raise_for_status()
        return response.json()

    def check_image(self, image_url, params_json):
        # Validate the key first
        validation_response = self.validate_key()
        if validation_response.get("status") != "success":
            raise ValueError("API key validation failed")

        # Send request to check_image endpoint
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"image_url": image_url, "params": params_json}
        response = requests.get(self.check_image_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

# # Create an instance of CMS with API key
# cms = CMS(api_key="4$...")

# # Example usage:
# image_url = "https://example.com/image.jpg"
# params_json = {"model": "0010", "other_param": "value"}
# result = cms.check_image(image_url, params_json)
# print(result)
