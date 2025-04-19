from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState
from typing import  Annotated
import operator
from openai import OpenAI
from langgraph.graph import START, END, StateGraph
# import markdown
# from weasyprint import HTML
import streamlit as st
import os

import prompts as pts


OPENAI_MODEL = "gpt-4o-mini"
PDF_NAME = "design_output.pdf"


# environment variables
os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGCHAIN_PROJECT"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]


# set the openai model
llm = ChatOpenAI(model = OPENAI_MODEL, temperature=0)
# create client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# class state
class BotState(MessagesState):
    requirements: str
    design: str


# def markdown_to_pdf(markdown_text, output_pdf_path):
#     # Convert markdown text to HTML
#     html_text = markdown.markdown(markdown_text)

#     # Convert HTML to PDF using WeasyPrint
#     HTML(string=html_text).write_pdf(output_pdf_path)


def get_architect_design(state: BotState):
    requirements_ = state["requirements"]

    # generate the prompt as a system message
    system_message_prompt = [SystemMessage(pts.ARCHITECT_DESIGN_PROMPT.format(requirements = requirements_ ))]
    # invoke the llm
    design_content = llm.invoke(system_message_prompt)

    return {"design": design_content.content}


# def pdf_creator(state: BotState):
#     proposed_design = state["design"]

#     # save the pdf
#     markdown_to_pdf(proposed_design, PDF_NAME)


# add nodes and edges
helper_builder = StateGraph(BotState)
helper_builder.add_node("get_architect_design", get_architect_design)
# helper_builder.add_node("pdf_creator", pdf_creator)

# build graph
helper_builder.add_edge(START, "get_architect_design")
# helper_builder.add_edge("get_architect_design", "pdf_creator")
helper_builder.add_edge("get_architect_design", END)

# compile the graph
helper_graph = helper_builder.compile()

