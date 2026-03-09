---
title: "Ollama Pydantic Project: Integrating MCP Server with a Local LLM Chatbot"
url: https://medium.com/p/30e25becdaa2
---

# Ollama Pydantic Project: Integrating MCP Server with a Local LLM Chatbot

[Original](https://medium.com/p/30e25becdaa2)

Member-only story

# Ollama Pydantic Project: Integrating MCP Server with a Local LLM Chatbot

[![Jageen Shukla](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*USuuuhOUCAdATko1)](/@jageenshukla?source=post_page---byline--30e25becdaa2---------------------------------------)

[Jageen Shukla](/@jageenshukla?source=post_page---byline--30e25becdaa2---------------------------------------)

4 min read

·

Apr 7, 2025

--

Listen

Share

More

Press enter or click to view image in full size

![]()

This project demonstrates how to build an intelligent chatbot using a local Ollama model, the Pydantic AI framework for agent management, and an MCP server for tool integration. The chatbot is accessible via a user-friendly Streamlit interface, making it easy to interact with the agent. The main goal is to showcase how these components work together, particularly focusing on the integration between the Pydantic agent and the MCP server.

For the full code, visit the [GitHub repository](https://github.com/jageenshukla/ollama-pydantic-project).

## Why This Project Matters

Most AI chatbots rely on cloud-based models, which can raise privacy concerns and introduce latency. This project offers a different approach:

* Local LLM with Ollama: Runs entirely on your machine for privacy and speed.
* Pydantic for Structure: Ensures data consistency when interacting with external tools.
* MCP Server for Extensibility: Allows the agent to call external tools (e.g., a math calculator) dynamically.
* Streamlit for Interaction: Provides a simple web interface for chatting with the agent.

This setup is ideal for developers who want a flexible, privacy-first chatbot that can be extended with custom tools.

## System Architecture

The chatbot system consists of four main components:

* Streamlit UI: Where users input their queries.
* Pydantic Agent: Manages the interaction with the Ollama model and decides when to call tools via the MCP server.
* Ollama Model: A local large language model (LLM) that processes queries.
* MCP Server: Hosts tools (e.g., a math operations tool) that the agent can use to perform specific tasks.

Here’s a simplified sequence diagram showing how a user query flows through the system:

Press enter or click to view image in full size

![]()

This diagram illustrates the key interactions: the user types a query in Streamlit, the Pydantic agent processes it (potentially calling the MCP server for tool-based tasks), and the response is displayed back in the UI.

## Technical Details

Let’s explore the core components of the project, using the actual code from the repository.

### 1. BaseAgent Abstract Class

The BaseAgent class defines the interface for all agents in the system, ensuring a consistent structure.

```
from abc import ABC, abstractmethod  
  
class BaseAgent(ABC):  
    @abstractmethod  
    def run(self, query: str):  
        pass
```

* **Purpose**: Provides a blueprint for agent implementations, requiring each to have a run method for processing queries.
* **Extensibility**: Allows for future agent variations while maintaining a uniform interface.

### 2. OllamaAgent Class

The OllamaAgent class implements the agent logic, connecting to the local Ollama model and the MCP server.

```
from pydantic_ai import Agent, Tool  
from pydantic_ai.models.openai import OpenAIModel  
from pydantic_ai.providers.openai import OpenAIProvider  
from pydantic import BaseModel  
from pydantic_ai.mcp import MCPServerHTTP  
import logging  
import streamlit as st  
  
class OllamaAgent:  
    mcp_server = MCPServerHTTP(url='http://localhost:4000/sse')   
    def __init__(self, model_name: str, base_url: str):  
        self.model = OpenAIModel(model_name=model_name, provider=OpenAIProvider(base_url=base_url))  
        self.agent = Agent(  
            self.model,  
            system_prompt=(  
                "You are chat bot assistant."  
                "You can use available tools to help users when required."  
            ),  
            mcp_servers=[self.mcp_server],  
        )  
    async def run(self, query: str):  
        async with self.agent.run_mcp_servers():  
            result = await self.agent.run(query)  
        return result
```

**Initialization**:

* Connects to the local Ollama model using OpenAIModel and OpenAIProvider (e.g., <http://localhost:11434/v1).>
* Sets up the Agent with a system prompt and connects it to the MCP server at <http://localhost:4000/sse.>

**Run Method**:

* Processes user queries asynchronously, leveraging the MCP server when tools are required.
* Returns the result directly from the pydantic\_ai framework.

### 3. Streamlit UI

The Streamlit app provides a chat interface for users to interact with the OllamaAgent.

```
import streamlit as st  
from agents.ollama_agent import OllamaAgent  
from pydantic import BaseModel  
import asyncio   
  
class FreeFormResponse(BaseModel):  
    content: str  
  
# Initialize the Ollama agent  
agent = OllamaAgent(  
    model_name="llama3.2:3b-instruct-fp16",  
    base_url="http://localhost:11434/v1",  
)  
  
# Initialize session state for conversation history  
if "messages" not in st.session_state:  
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]  
  
# Streamlit UI  
st.title("💬 Chat with Ollama Agent")  
st.caption("🚀 A chatbot powered by Ollama Agent")  
  
# Display conversation history  
for msg in st.session_state["messages"]:  
    st.chat_message(msg["role"]).write(msg["content"])  
  
# Input box for user query at the bottom  
if user_query := st.chat_input("Type your message here..."):  
    # Add user message to session state  
    st.session_state["messages"].append({"role": "user", "content": user_query})  
    st.chat_message("user").write(user_query)  
  
    # Agent response  
    with st.spinner("Agent is thinking..."):  
        try:  
            # Run the agent and get the result  
            result = asyncio.run(agent.run(user_query))  
              
            # Extract the 'content' field from the JSON response  
            response_content = result.data  # Assuming result.data is parsed into FreeFormResponse  
  
            # Add agent response to session state  
            st.session_state["messages"].append({"role": "assistant", "content": response_content})  
            st.chat_message("assistant").write(response_content)  
  
        except Exception as e:  
            error_message = f"An error occurred: {e}"  
            st.session_state["messages"].append({"role": "assistant", "content": error_message})  
            st.chat_message("assistant").write(error_message)
```

**Setup**:

* Initializes the OllamaAgent with the llama3.2:3b-instruct-fp16 model.
* Uses st.session\_state to manage conversation history, starting with a welcome message.

**UI**:

* Displays a title, caption, and chat history.
* Provides a chat input box for user queries.

**Query Handling**:

* Sends the user query to the agent’s run method using asyncio.run.
* Extracts and displays the response from result.data, with error handling for robustness.

## How It Works: Real Examples

Press enter or click to view image in full size

![]()

Left hand side we are running our [MCP server](https://github.com/jageenshukla/hello-world-mcp-server) and on right hand side we have used math tools.

## Conclusion

This project demonstrates a powerful yet simple way to integrate a local LLM with external tools via an MCP server, all managed through the Pydantic AI framework. The setup is modular, private, and easy to extend — perfect for developers who want to build custom, privacy-conscious chatbots.

Explore the code, try out the examples, and see how you can adapt this for your own use cases. The future of AI is local and extensible — this project is your starting point.

References

* [Ollama Documentation](https://ollama.com/)
* [Pydantic AI Framework](https://ai.pydantic.dev/agents/)
* [Streamlit Documentation](https://docs.streamlit.io/)
* [MCP Server Sample](https://github.com/jageenshukla/hello-world-mcp-server)
* [TypeScript MCP Server Blog](/@jageenshukla/building-a-typescript-mcp-server-a-guide-for-integrating-existing-services-5bde3fc13b23)