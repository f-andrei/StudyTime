from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from .custom_tools import tools
from config import model


prefix = """Assist a human by answering the following questions as best you can. 
If there are more than one question, after answering the first, start from the beginning again.
Remember for each question you have to first learn about the database structure,
finally execute the SQL query. Pay attention if the task is repeatable, if so, insert the day number
into the repeat_days table using the last row id.
Give the most information possible without going too technical.
You have access to the following tools"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)

memory = ConversationBufferMemory(memory_key="chat_history", input_key='input', output_key="output")

# Create LLMChain with the model and prompt
llm_chain = LLMChain(llm=model, prompt=prompt)

# Instantiate ZeroShotAgent with LLMChain and tools
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools)

# Create AgentExecutor from agent and tools
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory, max_iterations=5,
)
# Set return_intermediate_steps to True (returns the model's thought process as dict)
agent_chain.return_intermediate_steps = True
# Set parsing errors handling
agent_chain.handle_parsing_errors = True


async def invoke_chat(question):
    message = agent_chain.invoke({"input":question})
    return message['output']









