---
title: "LangChain Agents for Noobs: A Complete Practical Guide"
url: https://medium.com/p/e231b6c71a4a
---

# LangChain Agents for Noobs: A Complete Practical Guide

[Original](https://medium.com/p/e231b6c71a4a)

# LangChain Agents for Noobs: A Complete Practical Guide

[![Mehulpratapsingh](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*h-1AnFCwUy_fxLF_)](/@mehulpratapsingh?source=post_page---byline--e231b6c71a4a---------------------------------------)

[Mehulpratapsingh](/@mehulpratapsingh?source=post_page---byline--e231b6c71a4a---------------------------------------)

6 min read

·

Nov 6, 2024

--

Listen

Share

More

Press enter or click to view image in full size

![]()

## **Introduction**

LangChain is revolutionizing how we build AI applications by providing a powerful framework for creating agents that can think, reason, and take actions. In this comprehensive guide, we’ll explore everything you need to know about LangChain agents — from basic concepts to advanced implementations. Whether you’re just starting with AI or looking to build sophisticated applications, this guide will help you master LangChain agents.

## Table of Contents

1. Setting Up Your Environment

2. Understanding LangChain Agents

3. Basic Agent Implementation

4. Tools and Tool Usage

5. Advanced Agent Patterns

6. Real-World Applications

7. Best Practices

8. Troubleshooting Guide

## 1. Setting Up Your Environment

First, let’s set up our development environment with the necessary packages:

```
# Install required packages  
!pip install langchain openai python-dotenv google-search-results wikipedia  
  
# Import essential libraries  
import os  
from dotenv import load_dotenv  
from langchain.agents import load_tools  
from langchain.agents import initialize_agent  
from langchain.agents import AgentType  
from langchain.llms import OpenAI  
from langchain.chains import LLMChain  
from langchain.prompts import PromptTemplate  
  
# Load environment variables  
load_dotenv()  
  
# Initialize OpenAI API key  
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

## 2. Understanding LangChain Agents

LangChain agents are AI-powered entities that can:

* Process natural language instructions
* Use tools to gather information
* Make decisions based on context
* Execute actions to accomplish tasks

Let’s create our first simple agent:

```
# Initialize the language model  
llm = OpenAI(temperature=0)  
  
# Load basic tools  
tools = load_tools(["wikipedia", "llm-math"], llm=llm)  
  
# Initialize the agent  
agent = initialize_agent(  
    tools,   
    llm,   
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  
    verbose=True  
)  
  
# Test the agent  
response = agent.run(  
    "What is the square root of the year Wikipedia was founded?"  
)  
print(response)
```

## 3. Basic Agent Implementation

Let’s create a custom research agent that can gather and synthesize information:

```
from langchain.agents import Tool  
from langchain.memory import ConversationBufferMemory  
  
class ResearchAgent:  
    def __init__(self, llm):  
        self.llm = llm  
        self.memory = ConversationBufferMemory(memory_key="chat_history")  
          
        # Define tools  
        self.tools = [  
            Tool(  
                name="Wikipedia",  
                func=self.search_wikipedia,  
                description="Useful for searching Wikipedia articles"  
            ),  
            Tool(  
                name="Calculator",  
                func=self.calculate,  
                description="Useful for performing mathematical calculations"  
            )  
        ]  
          
        # Initialize agent  
        self.agent = initialize_agent(  
            self.tools,  
            self.llm,  
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,  
            memory=self.memory,  
            verbose=True  
        )  
      
    def search_wikipedia(self, query):  
        from langchain.tools import WikipediaQueryRun  
        wikipedia = WikipediaQueryRun(api_wrapper=Wikipedia())  
        return wikipedia.run(query)  
      
    def calculate(self, expression):  
        return eval(expression)  
      
    def run(self, query):  
        return self.agent.run(query)  
  
# Usage example  
research_agent = ResearchAgent(OpenAI(temperature=0))  
result = research_agent.run("Tell me about artificial intelligence and calculate how many years since it was first coined as a term in 1956.")  
print(result)
```

## 4. Tools and Tool Usage

Tools are fundamental to LangChain agents. Let’s create some custom tools:

```
from langchain.tools import BaseTool  
from typing import Optional, Type  
from pydantic import BaseModel, Field  
  
# Define input schema for our custom tool  
class StockPriceCheckInput(BaseModel):  
    symbol: str = Field(description="Stock symbol to check")  
  
class StockPriceTool(BaseTool):  
    name = "stock_price_checker"  
    description = "Useful for checking current stock prices"  
    args_schema: Type[BaseModel] = StockPriceCheckInput  
      
    def _run(self, symbol: str) -> str:  
        # Mock implementation - replace with real API call  
        import random  
        price = random.uniform(10, 1000)  
        return f"The current price of {symbol} is ${price:.2f}"  
      
    def _arun(self, symbol: str):  
        raise NotImplementedError("Async not implemented")  
  
# Create an agent with custom tools  
custom_tools = [  
    StockPriceTool(),  
]  
  
agent_with_custom_tools = initialize_agent(  
    custom_tools,  
    llm,  
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  
    verbose=True  
)  
  
# Test custom tool  
result = agent_with_custom_tools.run("What is the current price of AAPL stock?")  
print(result)
```

## 5. Advanced Agent Patterns

**5.1 Agent with Chain of Thought**

Let’s implement an agent that shows its reasoning process:

```
from langchain.agents import create_csv_agent  
from langchain.prompts import PromptTemplate  
  
class AnalyticalAgent:  
    def __init__(self, llm):  
        self.llm = llm  
          
        # Define the reasoning chain prompt  
        self.reasoning_prompt = PromptTemplate(  
            input_variables=["question"],  
            template="""  
            Question: {question}  
              
            Let's approach this step by step:  
            1) First, let's understand what we're being asked  
            2) Then, let's identify the tools we need  
            3) Finally, let's execute the plan  
              
            Reasoning:  
            """  
        )  
          
        # Create reasoning chain  
        self.reasoning_chain = LLMChain(  
            llm=self.llm,  
            prompt=self.reasoning_prompt  
        )  
      
    def analyze(self, question):  
        # Get reasoning steps  
        reasoning = self.reasoning_chain.run(question)  
          
        # Execute actual analysis  
        # This is where you'd implement the specific analysis logic  
          
        return {  
            "reasoning": reasoning,  
            "answer": "Final answer based on analysis"  
        }  
  
# Usage  
analytical_agent = AnalyticalAgent(OpenAI(temperature=0))  
result = analytical_agent.analyze("What factors influence stock market trends?")  
print(result["reasoning"])  
print("\nFinal Answer:", result["answer"])
```

**5.2 Multi-Agent System**

Let’s create a system where multiple agents collaborate:

```
class MultiAgentSystem:  
    def __init__(self, llm):  
        self.llm = llm  
        self.researcher = ResearchAgent(llm)  
        self.analyzer = AnalyticalAgent(llm)  
          
        # Coordinator prompt  
        self.coordinator_prompt = PromptTemplate(  
            input_variables=["task"],  
            template="""  
            Task: {task}  
              
            This task requires coordination between research and analysis.  
              
            Plan:  
            1) Research Phase:  
               - What information do we need?  
               - What sources should we consult?  
              
            2) Analysis Phase:  
               - How should we process the information?  
               - What insights should we look for?  
              
            3) Synthesis:  
               - How do we combine the findings?  
               - What conclusions can we draw?  
              
            Let's proceed step by step.  
            """  
        )  
          
        self.coordinator_chain = LLMChain(  
            llm=self.llm,  
            prompt=self.coordinator_prompt  
        )  
      
    def execute_task(self, task):  
        # Get coordination plan  
        plan = self.coordinator_chain.run(task)  
          
        # Execute research  
        research_results = self.researcher.run(task)  
          
        # Analyze findings  
        analysis = self.analyzer.analyze(research_results)  
          
        return {  
            "plan": plan,  
            "research": research_results,  
            "analysis": analysis  
        }  
  
# Usage  
multi_agent_system = MultiAgentSystem(OpenAI(temperature=0))  
result = multi_agent_system.execute_task(  
    "Analyze the impact of artificial intelligence on job markets"  
)
```

## 6. Real-World Applications

**6.1 Document Processing Agent**

```
from langchain.document_loaders import PyPDFLoader  
from langchain.text_splitter import RecursiveCharacterTextSplitter  
  
class DocumentProcessor:  
    def __init__(self, llm):  
        self.llm = llm  
        self.text_splitter = RecursiveCharacterTextSplitter(  
            chunk_size=1000,  
            chunk_overlap=200  
        )  
      
    def process_pdf(self, pdf_path):  
        # Load PDF  
        loader = PyPDFLoader(pdf_path)  
        documents = loader.load()  
          
        # Split text into chunks  
        texts = self.text_splitter.split_documents(documents)  
          
        # Process each chunk  
        summaries = []  
        for chunk in texts:  
            summary = self.llm(f"Summarize this text: {chunk.page_content}")  
            summaries.append(summary)  
          
        return "\n".join(summaries)  
  
# Usage  
doc_processor = DocumentProcessor(OpenAI(temperature=0))  
summary = doc_processor.process_pdf("example.pdf")
```

**6.2 Customer Service Agent**

```
class CustomerServiceAgent:  
    def __init__(self, llm):  
        self.llm = llm  
          
        # Define response templates  
        self.templates = {  
            "greeting": PromptTemplate(  
                input_variables=["customer_name"],  
                template="Hello {customer_name}! How can I assist you today?"  
            ),  
            "problem_solving": PromptTemplate(  
                input_variables=["problem", "context"],  
                template="""  
                I understand you're having an issue with {problem}.  
                  
                Context: {context}  
                  
                Let me help you resolve this:  
                1) First, let's identify the specific issue  
                2) Then, we'll look at possible solutions  
                3) Finally, we'll implement the best solution  
                  
                Please provide more details about your situation.  
                """  
            )  
        }  
          
        # Initialize chains  
        self.chains = {  
            name: LLMChain(llm=self.llm, prompt=prompt)  
            for name, prompt in self.templates.items()  
        }  
      
    def greet_customer(self, customer_name):  
        return self.chains["greeting"].run(customer_name=customer_name)  
      
    def handle_problem(self, problem, context):  
        return self.chains["problem_solving"].run(  
            problem=problem,  
            context=context  
        )  
  
# Usage  
cs_agent = CustomerServiceAgent(OpenAI(temperature=0.7))  
response = cs_agent.handle_problem(  
    "login issues",  
    "Customer cannot access their account after password reset"  
)
```

## 7. Best Practices

**7.1 Error Handling**

```
class RobustAgent:  
    def __init__(self, llm):  
        self.llm = llm  
      
    def safe_execute(self, func, *args, **kwargs):  
        try:  
            return func(*args, **kwargs)  
        except Exception as e:  
            return {  
                "error": str(e),  
                "status": "failed",  
                "recovery_action": self.get_recovery_action(e)  
            }  
      
    def get_recovery_action(self, error):  
        # Ask LLM for recovery suggestions  
        prompt = f"How should we handle this error: {str(error)}"  
        return self.llm(prompt)
```

**7.2 Memory Management**

```
from langchain.memory import ConversationBufferWindowMemory  
  
class MemoryEfficientAgent:  
    def __init__(self, llm, window_size=5):  
        self.memory = ConversationBufferWindowMemory(  
            k=window_size,  
            return_messages=True  
        )  
      
    def update_memory(self, input_text, output_text):  
        self.memory.save_context(  
            {"input": input_text},  
            {"output": output_text}  
        )  
      
    def get_context(self):  
        return self.memory.load_memory_variables({})
```

## 8. Troubleshooting Guide

Common issues and solutions:

```
class AgentDiagnostics:  
    @staticmethod  
    def check_api_keys():  
        required_keys = ["OPENAI_API_KEY", "SERPAPI_API_KEY"]  
        missing_keys = [  
            key for key in required_keys   
            if not os.getenv(key)  
        ]  
        return {  
            "status": "ok" if not missing_keys else "missing_keys",  
            "missing_keys": missing_keys  
        }  
      
    @staticmethod  
    def test_llm_connection(llm):  
        try:  
            response = llm("Test message")  
            return {"status": "ok", "response": response}  
        except Exception as e:  
            return {"status": "error", "error": str(e)}  
      
    @staticmethod  
    def validate_tools(tools):  
        return {  
            tool.name: {  
                "description": tool.description,  
                "status": "ok" if callable(getattr(tool, "_run", None)) else "error"  
            }  
            for tool in tools  
        }  
  
# Usage  
diagnostics = AgentDiagnostics()  
status = diagnostics.check_api_keys()
```

## Conclusion

LangChain agents provide a powerful framework for building sophisticated AI applications. By understanding the fundamentals and following best practices, you can create agents that efficiently solve complex problems. Remember to:

1. Start with simple agents and gradually add complexity
2. Use appropriate tools for specific tasks
3. Implement proper error handling and memory management
4. Test thoroughly before deployment
5. Monitor performance and iterate based on feedback

The code examples provided here serve as a foundation — feel free to modify and extend them based on your specific needs. Happy coding!

## Further Resources

1. [LangChain Documentation](https://python.langchain.com/docs/introduction/)
2. [OpenAI API Documentation](https://platform.openai.com/docs/api-reference/introduction)
3. [Python Best Practices Guide](https://realpython.com/tutorials/best-practices/)
4. [AI Agent Design Patterns](https://www.deeplearning.ai/short-courses/ai-agentic-design-patterns-with-autogen/)

Connect with me on [LinkedIn](https://www.linkedin.com/in/mehul-pratap-singh-3653481a1/)