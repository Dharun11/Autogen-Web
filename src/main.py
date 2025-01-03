from autogen import AssistantAgent,UserProxyAgent,GroupChat,GroupChatManager,ConversableAgent
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import streamlit as st
from groq import Groq
import requests
from typing import Annotated

load_dotenv()
api_key=os.getenv("GROQ_API")

config_list={
        "model": "llama-3.1-70b-versatile",

    "api_type": "groq",
    "api_key": api_key,
}


## Defining the required tools

def crawler_tool(urls):
    
    response = requests.get(urls)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.get_text(separator="\n")
    return content.split()[:2000]

def create_report(text: Annotated[str, "The query to search in the vector store"]):
    filename="report.txt"
    with open(filename, "w") as file:
        file.write(text)
    

user_proxy=UserProxyAgent(
    name="user_proxy",
    system_message="A Human Admin",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir":"groupchat",
        
        "use_docker":False,
    },
    human_input_mode="TERMINATE",
    llm_config=config_list
    
)

coder=AssistantAgent(
    name="coder",
    llm_config=config_list,
    #system_message="Write a code to crawl and extract the content of the given link return the content in length 2000",
    #system_message="A Human Admin",
)
pm=AssistantAgent(
    name="pm",
    llm_config=config_list,
    system_message="Classifyt eh content as spam or not spam ",
)
summary=AssistantAgent(
    name="summary",
    llm_config=config_list,
    system_message="Summarize the content and create a report of the summary",
)

summary.register_for_llm(name="create_report",description="Create a report of the summary")(create_report)
user_proxy.register_for_execution(name="create_report")(create_report)
gc=GroupChat(agents=[user_proxy,coder,pm,summary],messages=[],max_round=10)
manager=GroupChatManager(groupchat=gc,llm_config=config_list)
    

if __name__=="__main__":
    link="https://www.ndtv.com/india-news/nitish-kumars-folded-hands-response-to-lalu-yadavs-doors-open-remark-7383348"
    
    user_proxy.initiate_chat(
    manager, message=f"classify this content as a spam or not {link}"
)
# type exit to terminate the chat
    