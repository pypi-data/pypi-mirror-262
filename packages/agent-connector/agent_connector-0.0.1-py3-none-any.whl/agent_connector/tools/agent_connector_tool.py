from typing import List
from promptflow import tool
from promptflow.connections import CustomConnection
from agent_connector.tools.nexus_client import NexusClient

@tool
def call_agent(connection: CustomConnection,
               agent_name: str,
               agent_profile: str,
               agent_actions: List[str],
               user_input: str,
               ) -> str:
    
    agent_call = {}
    agent_call["agent_actions"] = agent_actions
    agent_call["agent_name"] = agent_name
    agent_call["agent_profile"] = agent_profile
    agent_call["messages"] = [{"content": user_input, "role": "user"}]
    
    client = NexusClient(connection.base_url) 
    
    response = client.call_agent(agent_call)["response"]
    return response