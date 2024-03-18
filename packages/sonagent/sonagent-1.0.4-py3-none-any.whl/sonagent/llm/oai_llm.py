import os
from openai import OpenAI
from langchain.prompts import PromptTemplate
import re
import logging
from sonagent.llm.prompt import (
    summary_doc, create_git_pull_request_param, 
    GITHUB_PULL_REQUEST_PROMPT, rewrite_code_with_docstring
)

logger = logging.getLogger(__name__)

def text_summary(docs):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    sum_prompt = summary_doc(docs)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "play as interactive role, tell user if there is anything else you should take into consideration with the piece of text user trying to learn about. ",
            },
            {"role": "user", "content": sum_prompt},
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content


def create_pull_request_info(docs):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    # prompt = create_git_pull_request_param(docs)
    
    prompt_temp = PromptTemplate(
        template=GITHUB_PULL_REQUEST_PROMPT,
        input_variables=["sumary_text"],
    )
    prompt = prompt_temp.format(sumary_text=docs)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "you are a sennior software engineer and you are creating a pull request for the following changes. Your results will be used in another software.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content



def create_chat_with_function(docs):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    # prompt = create_git_pull_request_param(docs)
    
    prompt_temp = PromptTemplate(
        template=GITHUB_PULL_REQUEST_PROMPT,
        input_variables=["sumary_text"],
    )
    prompt = prompt_temp.format(sumary_text=docs)
    
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": "you are a sennior software engineer and you are creating a pull request for the following changes. Your results will be used in another software.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content


def rewrite_python_code_docs_string(code: str):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    prompt = rewrite_code_with_docstring(input_code=code)
    logger.info(f"Prompt: {prompt}")    
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a python expert capable of adding doc strings and comments to user code. Please describe carefully without forgetting the keywords and try to make the description friendly to search engines",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    code = str(response.choices[0].message.content)
    logger.info(f"---------------")
    logging.info(f"Rewrite Python Code: {code}")
    logger.info(f"---------------")

    # get ```python ``` block
    try:
        # Biểu thức chính quy để tìm đoạn mã Python trong chuỗi
        pattern = r'```python(.*?)```'
        # Tìm tất cả các kết quả phù hợp
        matches = re.findall(pattern, code, re.DOTALL)
        # Lặp qua các kết quả và in ra màn hình
        string_a = ""
        for match in matches:
            string_a = match.strip()
        python_code = string_a

    except Exception as e:
        logger.error(f"--- Error: {e}")
        python_code = code
    return python_code
