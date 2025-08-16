"""Module providing a langchain agent to answer user queries."""
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents import OpenAIFunctionsAgent
from langchain.memory import  ConversationBufferWindowMemory, RedisChatMessageHistory
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder

from ..core.config import settings
from ..tools.retriever import get_code_context

output_instructions = """Respond in structure:
{
  "answer": "<your answer in markdown>",
  "related_files": ["/path/to/file1", "/path/to/file2", ...]
}
"""

def get_chat_agent(session_id = None):

    memory=ConversationBufferWindowMemory(k=settings.DOC_RETRIEVAL_TOP_K, return_messages=True, memory_key='memory')

    prompt_message = """You are a professional AI assistant designed to onboard new developers to a codebase.

                        Your job is to:
                        1. Carefully listen to the user's question, which may relate to a bug, a new feature, or understanding existing functionality.
                        2. Retrieve the most relevant source code chunks using vector similarity from the codebase (stored in FAISS).
                        3. Use the retrieved context as a reference — do not make assumptions beyond it.
                        4. Analyze the context deeply and respond with a step-by-step answer that:
                        - Explains the related part of the code.
                        - Guides the developer toward a solution.
                        - Suggests relevant files, classes, or functions that are important.
                        - If applicable, recommends best practices or hints for next steps.

                        You must ensure your response is:
                        - Technically accurate.
                        - Easy to understand for a new developer.
                        - Fully grounded in the retrieved code context.

                        If the context is insufficient to answer the query confidently, ask a clarifying question.

                        Examples of supported queries:
                        - "Where should I fix this bug?"
                        - "How do I add a new payment gateway?"
                        - "Which function is responsible for creating the user?"

                        Be precise, contextual, and helpful.

    """
    system_prompt=SystemMessage(content=prompt_message + "\n\n" + output_instructions)

    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_prompt,
        extra_prompt_messages=[MessagesPlaceholder(variable_name="memory")],
    )

    llm = ChatOpenAI(temperature=0, model=settings.OPENAI_MODEL_NAME, streaming=True, verbose=True)
    tools = [get_code_context]

    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True, max_iterations=5, max_execution_time=50)

