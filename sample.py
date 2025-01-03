from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import streamlit as st
from groq import Groq
import requests
from typing import Annotated
import json

load_dotenv()
api_key = os.getenv("GROQ_API")

config_list = {
    "model": "llama-3.1-70b-versatile",
    "api_type": "groq",
    "api_key": api_key,
}

def crawler_tool(url: str) -> dict:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract specific content areas
        title = soup.find('h1').get_text() if soup.find('h1') else ""
        main_content = ' '.join([p.get_text() for p in soup.find_all(['p', 'article'])])
        
        return {
            "title": title,
            "content": main_content[:2000],
            "url": url
        }
    except Exception as e:
        return {"error": str(e)}

def create_report(content: dict) -> str:
    report_content = f"""
Content Analysis Report
URL: {content.get('url')}
Title: {content.get('title')}
Analysis: {content.get('analysis', '')}
Classification: {content.get('classification', '')}
Summary: {content.get('summary', '')}
    """
    
    with open("report.txt", "w") as file:
        file.write(report_content)
    return "Report created successfully"

def next_speaker(last_speaker,groupchat):
    messages=groupchat.messages
    '''
    if len(messages)<2:
        nxt="coder"
        match last:
            case "coder":
                if len(messages)>1:
                    nxt="content_classifier"
                else:
                    nxt="coder"
            case "content_classifier":
                nxt="summarizer"
            case "summarizer":
                nxt="report_generator"
                
        print(f"Messages: {len(messages)}")
        print(f"Last Speaker: {last}")
        print(f"Next Speaker: {nxt}")
    '''
    if last_speaker=="user_proxy":
        return coder
    elif last_speaker=="coder":
        return content_classifier
    elif last_speaker is content_classifier:
        if messages[-1]["content"] == "exitcode: 1":
            # retrieve --(execution failed)--> retrieve
            return coder
        else:
            # retrieve --(execution success)--> research
            return summarizer
    elif last_speaker=="content_classifier":
        return summarizer
    
        return nxt


user_proxy = UserProxyAgent(
    name="user_proxy",
    system_message="""Human admin who initiates tasks. Provide URLs for content analysis.""",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "groupchat",
        "use_docker": False
    },
    human_input_mode="TERMINATE",
    llm_config=config_list
)

coder = AssistantAgent(
    name="coder",
    system_message="""Web content extractor. Extract meaningful content from URLs while:
- Maintaining proper HTML parsing
- Handling different content structures
- Managing errors gracefully
- Providing structured output""",
    llm_config=config_list
)

content_classifier = AssistantAgent(
    name="content_classifier",
    system_message="""Content classifier focusing on:
- Spam detection using key indicators
- Clickbait assessment
- Content quality evaluation
- Credibility analysis
Return classification with confidence score and reasoning.""",
    llm_config=config_list
)

summarizer = AssistantAgent(
    name="summarizer",
    system_message="""Content summarizer that:
- Extracts key points
- Maintains context
- Identifies main themes
- Preserves important details
Generate concise yet comprehensive summaries.""",
    llm_config=config_list
)

report_generator = AssistantAgent(
    name="report_generator",
    system_message= """Report creator that:
- Compiles analysis results
- Structures information clearly
- Includes all relevant metrics
- Creates readable output""",
    llm_config=config_list
)

agents = [user_proxy, coder, content_classifier, summarizer, report_generator]
groupchat = GroupChat(
    agents=agents,
    messages=[],
    max_round=5,
   #speaker_selection_method=next_speaker
)

manager = GroupChatManager(groupchat=groupchat, llm_config=config_list)

def analyze_content(url):
    chat_response=user_proxy.initiate_chat(manager, message=f"Analyze this content and write a summary report and classify it as spam or not: {url}")
    return chat_response

if __name__ == "__main__":
    
    result=analyze_content("https://www.ndtv.com/india-news/nitish-kumars-folded-hands-response-to-lalu-yadavs-doors-open-remark-7383348")
    message=result.chat_history
    for msg in message:
        if msg['content']:
            print(msg['content'])
            
    '''
    link = "https://www.deccanchronicle.com/entertainment/nikhil-and-sreeleela-warn-against-spreading-of-fake-news-1851092"
    user_proxy.initiate_chat(manager, message=f"Analyze this content and write a summary report and classify it as spam or not: {link}")
    '''
    st.title("Web Content Analysis")
    with st.form("url form"):
        url = st.text_input("Enter a URL to analyze")
        submit_button = st.form_submit_button("Analyze")
        
    if submit_button and url:
        with st.spinner("Analyzing content..."):
            result = analyze_content(url)
            messages=result.chat_history
            chat_tab, summary_tab = st.tabs(["Chat Flow", "Final Summary"])
            
            with chat_tab:
                st.subheader("Analysis")
                #st.json(result.get('analysis', {}))
                for msg in messages:
                        if msg['content']:  # Skip empty messages
                            with st.chat_message(msg['role']):
                                st.markdown(msg['content'])
                
            with summary_tab:
                st.subheader("Analysis Summary")
                if result.summary:
                    st.markdown(result.summary)
            
                
    
    