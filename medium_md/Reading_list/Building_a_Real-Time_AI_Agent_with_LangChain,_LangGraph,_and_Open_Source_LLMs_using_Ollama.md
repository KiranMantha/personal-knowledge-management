---
title: "Building a Real-Time AI Agent with LangChain, LangGraph, and Open Source LLMs using Ollama"
url: https://medium.com/p/3602fc77c7c3
---

# Building a Real-Time AI Agent with LangChain, LangGraph, and Open Source LLMs using Ollama

[Original](https://medium.com/p/3602fc77c7c3)

# Building a Real-Time AI Agent with LangChain, LangGraph, and Open Source LLMs using Ollama

[![Manoj Mukherjee](https://miro.medium.com/v2/resize:fill:64:64/1*G8qDGnaaDehoLl_iBm5ksg.jpeg)](/@manojmukherjee777?source=post_page---byline--3602fc77c7c3---------------------------------------)

[Manoj Mukherjee](/@manojmukherjee777?source=post_page---byline--3602fc77c7c3---------------------------------------)

6 min read

·

Sep 14, 2024

--

2

Listen

Share

More

As AI capabilities continue to advance, engineers are exploring powerful new ways to build intelligent applications. In this post, we’ll walk through creating a proof-of-concept AI search agent using cutting-edge open source tools and frameworks. We’ll leverage LangGraph for workflow orchestration, LangChain for LLM integration, Ollama for running open source models like Llama3.1, and Next.js for the full stack Hybrid web app. Let’s dive in!

Press enter or click to view image in full size

![]()

### Setting Up the Environment

To get started, you’ll need a ***JavaScript/TypeScript*** development environment. Here are the key technologies we’ll be using:

* ***Node.js and npm***
* ***TypeScript***
* ***Next.js***
* ***Zod***
* ***LangChain***
* ***LangGraph***
* ***Ollama (for running Llama 3.1)***
* ***LangSmith (for observability)***

Make sure you have Node.js installed (LTS Version v20+), then create a new Next.js project:

```
npx create-next-app@latest poc-ai  
cd poc-ai  
npm i
```

Install the required dependencies:

```
npm i @langchain/community @langchain/core @langchain/langgraph @langchain/ollama nanoid zod
```

### **Project Structure:**

```
poc-ai/  
  ├── src/  
  │   ├── ai/  
  │   │   ├── agents/  
  │   │   │   └── index.ts  
  │   │   ├── llm-model/  
  │   │   │   ├── index.ts  
  │   │   │   └── ollama.ts  
  │   │   └── tools/  
  │   │       ├── index.ts  
  │   │       └── searchTool.ts  
  │   ├── app/  
  │   │   └── api/  
  │   │       └── ai/  
  │   │           └── route.ts  
  │   └── ...  
  ├── .env.local  
  ├── .eslintrc.json  
  ├── .gitignore  
  ├── next-env.d.ts  
  ├── next.config.mjs  
  ├── package-lock.json  
  ├── package.json  
  ├── postcss.config.js  
  ├── README.md  
  ├── tailwind.config.ts  
  └── tsconfig.json
```

### Implementing the AI Agent:

Let’s break down the key components:

**LLM Model Setup (**[**Ollama**](https://ollama.com/) **With Llama3.1):**

This code sets up our language model using **Ollama** and binds it with custom tools.

```
// src/ai/llm-model/ollama.ts  
import { ChatOllama } from "@langchain/ollama";  
  
const MODEL_NAME = "llama3.1";  
  
export const llm = new ChatOllama({  
  model: MODEL_NAME,  
  temperature: 0,  
});
```

```
// src/ai/llm-model/index.ts  
import { tools } from "../tools";  
import { llm } from "./ollama";  
  
export const model = llm.bindTools(tools);
```

**LangGraph Agent (Langchain setup):**

This sets up our **LangGraph** workflow, defining the agent’s decision-making process and tool usage.

```
// src/ai/index.ts  
  
import { MemorySaver, StateGraph } from "@langchain/langgraph";  
import { callModel, shouldContinue, StateAnnotation } from "./agents";  
import { toolNode } from "./tools";  
import { HumanMessage } from "@langchain/core/messages";  
  
// Define a new graph  
export const workflow = new StateGraph(StateAnnotation)  
  .addNode("agent", callModel)  
  .addNode("tools", toolNode)  
  .addEdge("__start__", "agent")  
  .addConditionalEdges("agent", shouldContinue)  
  .addEdge("tools", "agent");  
  
// Initialize memory to persist state between graph runs  
const checkpointer = new MemorySaver();  
  
export const startRunnable = async (query: string, thread_id: string) => {  
  // Finally, we compile it!  
  // This compiles it into a LangChain Runnable.  
  // Note that we're (optionally) passing the memory when compiling the graph  
  const app = workflow.compile({ checkpointer });  
  // Use the Runnable  
  const finalState = await app.invoke(  
    {  
      messages: [new HumanMessage(query)],  
    },  
    { configurable: { thread_id: thread_id } }  
  );  
  
  return finalState.messages[finalState.messages.length - 1].content;  
};
```

```
// src/ai/agents/index.ts  
  
import {  
  AIMessage,  
  BaseMessage,  
  SystemMessage,  
} from "@langchain/core/messages";  
import { Annotation } from "@langchain/langgraph";  
import { model } from "../llm-model";  
  
export const StateAnnotation = Annotation.Root({  
  messages: Annotation<BaseMessage[]>({  
    reducer: (x, y) => x.concat(y),  
  }),  
});  
  
// Define the function that determines whether to continue or not  
// We can extract the state typing via `StateAnnotation.State`  
export function shouldContinue(state: typeof StateAnnotation.State) {  
  const messages = state.messages;  
  const lastMessage = messages[messages.length - 1] as AIMessage;  
  
  // If the LLM makes a tool call, then we route to the "tools" node  
  if (lastMessage.tool_calls?.length) {  
    return "tools";  
  }  
  // Otherwise, we stop (reply to the user)  
  return "__end__";  
}  
  
// Define the function that calls the model  
export async function callModel(state: typeof StateAnnotation.State) {  
  const messages = state.messages;  
  const response = await model.invoke([  
    new SystemMessage(`You are a journalist delivering news information.   
      Please summarize the sentence according to the following REQUEST.  
  
REQUEST:  
  
1. Summarize the article in the first sentence, keeping it less than 5 lines.  
  
2. Summarize the main points in bullet points in HINDI.  
  
3. DO NOT translate any technical terms.  
  
4. DO NOT include any unnecessary information.  
  
You have tools to search in internet and get data then make summary  
  
SUMMARY:  
`),  
    ...messages,  
  ]);  
  
  // We return a list, because this will get added to the existing list  
  return { messages: [response] };  
}
```

**Custom Search Tool (Search Tool using** [**Tavily**](https://tavily.com)**):**

We’re using the **Tavily** search API as our custom tool for retrieving real-world data.

```
// src/ai/tools/searchTool.ts  
import { TavilySearchResults } from "@langchain/community/tools/tavily_search";  
  
export const searchTool = new TavilySearchResults({  
  maxResults: 10,  
});
```

```
// src/ai/tools/index.ts  
import { ToolNode } from "@langchain/langgraph/prebuilt";  
import { searchTool } from "./searchTool";  
  
export const tools = [searchTool];  
export const toolNode = new ToolNode(tools);
```

**API Route Create—** [**Nextjs (App Route)**](https://nextjs.org/docs/app/building-your-application/routing)**:**

This sets up our **Next.js** API route to handle incoming requests and interact with our AI agent.

```
// src/app/api/ai/route.ts  
import { startRunnable } from "@/ai";  
import { nanoid } from "nanoid";  
import { z } from "zod";  
  
const InputBodySchema = z.object({  
  message: z.string().min(1),  
  chatId: z.string().optional(),  
});  
  
type InputBodyType = z.infer<typeof InputBodySchema>;  
  
export async function POST(req: Request) {  
  const { message, chatId }: InputBodyType = await req.json();  
  const result = InputBodySchema.safeParse({ message, chatId });  
  
  if (!result.success) {  
    return Response.json({ data: null, error: result?.error }, { status: 500 });  
  }  
  const res = await startRunnable(message, chatId ?? nanoid());  
  
  return Response.json({ data: JSON.stringify(res) });  
}
```

Configure environment variables: Create a `.env.local` file in the root directory and add your API keys:

```
LANGCHAIN_TRACING_V2=true  
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"  
LANGCHAIN_API_KEY="your_langchain_api_key"  
LANGCHAIN_PROJECT="your_project_name"  
TAVILY_API_KEY="our_tavily_api_key"  
LANGCHAIN_CALLBACKS_BACKGROUND=true
```

### Leveraging LangSmith for Observability

[LangSmith](https://www.langchain.com/langsmith) provides powerful tracing and debugging capabilities for our LangChain applications. In the screenshots, we can see how LangSmith visualizes our agent’s decision-making process, tool usage, and overall performance.

Here is Link of this [POC view Langsmith](https://smith.langchain.com/public/970995f4-707c-4381-b797-74f8b84ae927/r)

### Key benefits of using LangSmith:

1. Detailed tracing of each step in the agent’s workflow
2. Performance metrics and latency analysis
3. Easy debugging of complex AI pipelines

**Running the Application**

1. Start your Ollama server with the Llama 3.1 model

```
Ollama run llama3.1
```

1. Run your Next.js development server: `npm run dev`
2. Send a POST request to `http://localhost:3000/api/ai` with a JSON body containing a `message` field

*Here I am using REST Client in VS Code*

Press enter or click to view image in full size

![]()

### Example query and response:

> Query: What is happening in West Bengal about protests?

### Response:

```
{  
  "data": "\"Here is a summary of the article in one sentence:\\n\\nProtests have been taking place in West Bengal, India, following the brutal rape and murder of a trainee doctor at a state-run hospital, with thousands of protesters blocking train tracks, halting buses, and shouting slogans.\\n\\nThe main points summarized in Hindi:\\n\\n1. पश्चिम बंगाल में एक सरकारी अस्पताल में एक प्रशिक्षु डॉक्टर के साथ बलात्कार और हत्या की घटना हुई है।\\n2. इस घटना के विरोध में हजारों लोग सड़कों पर उतर आए हैं।\\n3. प्रदर्शनकारियों ने ट्रेन की पटरियों को अवरुद्ध कर दिया है और बसों को रोक दिया है।\\n4. लोग नारेबाजी कर रहे हैं और न्याय की मांग कर रहे हैं।\\n5. यह घटना राज्य में कानून व्यवस्था की स्थिति पर सवाल उठा रही है।\""  
}
```

### Conclusion

We’ve explored building an AI-powered search agent using LangGraph, LangChain, and open-source LLMs. We’ve seen how these tools can be combined to create powerful, flexible AI applications. By leveraging LangSmith for observability, we can easily debug and optimize our AI workflows.

This proof-of-concept demonstrates the potential of these technologies for creating intelligent, context-aware applications. As you continue to explore and build with these tools, remember to consider ethical implications and potential biases in AI systems.

**Enjoyed the content?**  
If you’d like to support my work, consider buying me a coffee! Your support helps me continue creating helpful content.  
[**Buy me a coffee here**](https://buymeacoffee.com/2manoj1)**. ☕💻**

> If you’re interested in learning more about this project or discussing AI engineering in general, feel free to connect with me on [LinkedIn: Manoj Mukherjee](https://www.linkedin.com/in/manoj-mukherjee/)

***I’m always looking to network and grow my career in the AI field. If you’d like to collaborate or discuss potential opportunities, don’t hesitate to reach out. I’m open to sharing more details about this project and exploring how we can push the boundaries of AI technology together.***

*Happy coding, and I look forward to connecting with fellow AI enthusiasts and professionals!*

Press enter or click to view image in full size

![]()