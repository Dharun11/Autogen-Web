from autogen import AssistantAgent,UserProxyAgent,GroupChat,GroupChatManager
from dotenv import load_dotenv
from exception import CustomException
import os
import streamlit as st
from groq import Groq
import sys
from datetime import datetime 
import logging
load_dotenv()

log_file=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

#setting up the logs folder path
logs_folder_path = os.path.join(os.getcwd(), "logs",log_file)
## Creating a directory
os.makedirs(logs_folder_path,exist_ok=True)

log_file_path=os.path.join(logs_folder_path,log_file)

logging.basicConfig(
    filename=log_file_path,
    format="[%(asctime)s] %(lineno)d %(name)s -%(message)s",
    level=logging.INFO
)






class ClassifyContent():
    def __init__(self):
        
        self.api_key=os.getenv("GROQ_API")

        self.config_list={
                "model": "llama-3.1-70b-versatile",

            "api_type": "groq",
            "api_key": self.api_key,
        }



    def classify_content(self,link):
        self.user_proxy=UserProxyAgent(
        name="user_proxy",
        system_message="A Human Admin",
        code_execution_config={
            "last_n_messages": 3,
            "work_dir":"groupchat",
            
            "use_docker":False,
        },
        human_input_mode="TERMINATE",
        llm_config=self.config_list
        
    )

        self.coder = AssistantAgent(
            name="coder",
            system_message="""Web content extractor. Extract meaningful content from URLs while:
        - Maintaining proper HTML parsing
        - Handling different content structures
        - Managing errors gracefully
        - Providing structured output""",
            llm_config=self.config_list
        )

        self.content_classifier = AssistantAgent(
            name="content_classifier",
            system_message="""Content classifier focusing on:
        - Spam detection using key indicators
        - Clickbait assessment
        - Content quality evaluation
        - Credibility analysis
        Return classification with confidence score and reasoning.""",
            llm_config=self.config_list
        )
        self.summarizer = AssistantAgent(
            name="summarizer",
            system_message="""Content summarizer that:
        - Extracts key points
        - Maintains context
        - Identifies main themes
        - Preserves important details
        Generate concise yet comprehensive summaries.""",
            llm_config=self.config_list
        )

        self.report_generator = AssistantAgent(
            name="report_generator",
            system_message= """Report creator that:
        - Compiles analysis results
        - Structures information clearly
        - Includes all relevant metrics
        - Creates readable output""",
            llm_config=self.config_list
        )
        
        self.groupcat=GroupChat(agents=[self.user_proxy,self.coder,self.content_classifier,self.summarizer,self.report_generator],messages=[],max_round=5)
        self.manager=GroupChatManager(groupchat=self.groupcat,llm_config=self.config_list)
        chat_response=self.user_proxy.initiate_chat(
            self.manager, message=f"Analyze this content and write a summary report and classify it as spam or not: {link}"
        )  
        
        return chat_response 
        
        



def main():
    try:
        logging.info("Starting the streamlit app")
        st.title("Content Classifier")
        st.write("This app classifies content as spam or not")
        analyzer=ClassifyContent()
        
        
        with st.form("url_form"):
            url = st.text_input("Enter URL to analyze:")
            submitted = st.form_submit_button("Analyze")
        logging.info("Analyzing the content")
        if submitted and url:
            with st.spinner("Analyzing content..."):
                
                    result = analyzer.classify_content(url)
                    
                
                    messages = result.chat_history
                    
                
                    chat_tab, summary_tab = st.tabs(["Chat Flow", "Final Summary"])
                    
                    with chat_tab:
                        st.subheader("Analysis Process")
                        for msg in messages:
                            if msg['content']:  
                                with st.chat_message(msg['role']):
                                    st.markdown(msg['content'])
                    
                    with summary_tab:
                        st.subheader("Analysis Summary")
                        if result.summary:
                            st.markdown(result.summary)
            logging.info("succesfully analyzed the content")  
                   

    except Exception as e:
        raise st.write(CustomException(e,sys))

    

if __name__=="__main__":
    main()

    