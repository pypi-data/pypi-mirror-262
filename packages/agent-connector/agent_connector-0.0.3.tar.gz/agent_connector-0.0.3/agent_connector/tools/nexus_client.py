import requests
from typing import List, Dict

class NexusClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_threads(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/get_threads")
        return response.json()

    def read_messages(self, thread_id: int) -> List[Dict]:
        response = requests.get(f"{self.base_url}/read_messages/{thread_id}")
        return response.json()

    def get_agent_names(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/get_agent_names")
        return response.json()

    def get_profile_names(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/get_profile_names")
        return response.json()

    def get_action_names(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/get_action_names")
        return response.json()

    def call_agent(self, agent_call_request: Dict) -> Dict:
        response = requests.post(f"{self.base_url}/call_agent", json=agent_call_request)
        return response.json()

# Example usage
# if __name__ == "__main__":
#     client = NexusClient("http://localhost:8000")  # Adjust the base_url as needed
    
#     # Example for calling `get_threads`
#     threads = client.get_threads()
#     print("Threads:", threads)

#     # Continue for other methods as needed
