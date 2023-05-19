# python deps
# streamlit - used to build the app
# langchain - used to build the LLM workflow
# openai - needed to use openai gpt
# wikipedia - used to connect GPT to wikipedia
# chromadb - vector storage
# tiktoken - backedn tokenizer for openai

# To install deps:
# pip install streamlit langchain openai wikipedia chromadb tiktoken
# To run the app:
# streamlit run app.py

# Bring in deps
import os 
from apikey import apikey 

import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

os.environ['OPENAI_API_KEY'] = apikey

# App framework
st.title('✍🏻 Gartner GPT Writer')
prompt = st.text_input('To generate a title and research note, specify a topic below') 

# Prompt templates for the research note title
title_template = PromptTemplate(
    input_variables = ['topic'], 
    template='write me a Gartner style research note title about {topic}'
)

# Prompt template for the research note
script_template = PromptTemplate(
    input_variables = ['title', 'wikipedia_research'], 
    template='write me a Gartner style research note based on this title TITLE: {title} while leveraging this wikipedia reserch:{wikipedia_research} '
)

title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')


# Llms
llm = OpenAI(temperature=0.9) 
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)

wiki = WikipediaAPIWrapper()

# Show stuff to the screen if there's a prompt
if prompt: 
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt) 
    script = script_chain.run(title=title, wikipedia_research=wiki_research)

    st.write(title) 
    st.write(script) 

    with st.expander('Title History'): 
        st.info(title_memory.buffer)

    with st.expander('Script History'): 
        st.info(script_memory.buffer)

    with st.expander('Wikipedia Research'): 
        st.info(wiki_research)
