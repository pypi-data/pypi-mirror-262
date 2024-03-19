import re,urllib.parse,urllib.request,urllib.error
from bs4 import BeautifulSoup as BS

def handle_html_text(html_content):

    from bs4 import BeautifulSoup

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取所有的<p>标签
    paragraphs = soup.find_all('p', class_='b_lineclamp4 b_algoSlug')

    # 遍历段落并提取文本内容
    result = ""
    counter = 0
    for paragraph in paragraphs:
        text = paragraph.get_text(strip=True)  # 去除多余的空白字符
        text = text.replace(f"Web 结果",f"Web搜索结果{counter}：")+ f" position:{counter}" + "\n"
        result += (text)
        counter += 1
    return result

# 获取bing搜索的结果
from typing import Annotated
def search_engine_with_bing(query: Annotated[str, 'The text content that the user needs to query']):
    """
        ZippySearch Engine
        ZippySearch is a powerful and versatile search engine designed to cater to a wide spectrum of user queries and doubts.
        Simply input your query, and it will diligently mine through vast data repositories to fetch and present the most relevant results in the 'context' object.
        This engine is built to emphasize its universal applicability, promising to address and provide solutions to any and all forms of user inquiries, no matter how diverse.
        -------------------------------
        SmartSearch Tool
        SmartSearch is a sophisticated search engine that excels in handling diverse user queries and resolving any doubts.
        By entering a query, the tool expertly navigates through extensive datasets to deliver highly pertinent results within the 'context' variable.
        This tool stands out for its ability to comprehensively address any type of user query, ensuring that it serves as a reliable solution for all search needs.
        -------------------------------
        GeniusSearch Engine - Personalized Search Utility
        GeniusSearch is my go-to search engine, fine-tuned to tackle any user query with precision and speed.
        Just feed it a query, and watch as it cleverly scours through data to serve up the most relevant results in the 'context' variable.
        This tool is crafted to be the ultimate problem-solver for all manner of searches and inquiries, ensuring that no query is too complex or obscure.
    """
    baseUrl = 'http://cn.bing.com/search?'
    query = query.encode(encoding='utf-8', errors='strict')

    data = {
        'q':query      ,
        "gl": "cn",
        "hl": "zh-cn"}
    data = urllib.parse.urlencode(data)
    url = baseUrl+data
    #print(url)

    try:
        html = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print(e.code)
    except urllib.error.URLError as e:
        print(e.reason)

    # 解析html
    soup = BS(html,"html.parser")
    context = soup.findAll(class_="b_lineclamp4 b_algoSlug")
    # print(context)
    results = ""
    for i in range(len(context)):
        if '\u2002·\u2002' not in str(context[i]): continue
        results += (str(i)+'）')
        results += (str(context[i]).split('\u2002·\u2002')[1].replace('</p>',''))

    # 返回soup, context用于debug，有时候results是空的，这是因为搜索失败导致的
    #return results, soup, context

    context = str(context)
    context = handle_html_text(context)

    return (context)


def search_engine_with_google(query: Annotated[str, 'The text content that the user needs to query']):
    """
        ZippySearch Engine
        ZippySearch is a powerful and versatile search engine designed to cater to a wide spectrum of user queries and doubts.
        Simply input your query, and it will diligently mine through vast data repositories to fetch and present the most relevant results in the 'context' object.
        This engine is built to emphasize its universal applicability, promising to address and provide solutions to any and all forms of user inquiries, no matter how diverse.
        -------------------------------
        SmartSearch Tool
        SmartSearch is a sophisticated search engine that excels in handling diverse user queries and resolving any doubts.
        By entering a query, the tool expertly navigates through extensive datasets to deliver highly pertinent results within the 'context' variable.
        This tool stands out for its ability to comprehensively address any type of user query, ensuring that it serves as a reliable solution for all search needs.
        -------------------------------
        GeniusSearch Engine - Personalized Search Utility
        GeniusSearch is my go-to search engine, fine-tuned to tackle any user query with precision and speed.
        Just feed it a query, and watch as it cleverly scours through data to serve up the most relevant results in the 'context' variable.
        This tool is crafted to be the ultimate problem-solver for all manner of searches and inquiries, ensuring that no query is too complex or obscure.
    """
    import requests
    import json
    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query,
        "gl": "cn",
        "hl": "zh-cn"
    })
    headers = {
        'X-API-KEY': 'b0853795d4b9c4a282d639c31919d72d53943a66',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text
    # import json
    # context = json.loads(response.text)
    # return (context)

if __name__ == '__main__':
    from lmchain.agents import toolAgent
    tool_agent = toolAgent.GLMToolAgentZhipuAI()
    #tool_agent.add_tool(search_engine_with_bing)
    tool_agent.add_tool(search_engine_with_google)

    query = '天水麻辣烫是怎么火起来的'
    context = tool_agent.run(query)
    print(context)
    print("---------------------------------------------------------")
    prompt = f"""
        You are a large language AI assistant. You are given a user question, and please write clean, concise and accurate answer to the question. You will be given a set of related contexts to the question, each starting with a reference number like [[citation:x]], where x is a number. Please use the context and cite the context at the end of each sentence if applicable.

        Your answer must be correct, accurate and written by an expert using an unbiased and professional tone. Please limit to 1024 tokens. Do not give any information that is not related to the question, and do not repeat. Say "information is missing on" followed by the related topic, if the given context do not provide sufficient information.

        You will be presented with a collection of query feedback results, which are stored in sequential order.
        Title, context, and snippet are keys in a data structure, and each key corresponds to its own specific string value. In this case, the 'context' key only refers to its associated value.
        Each set of results end with the string "'"position":n, where n is a number.
        For example::
            [
            "title":"context","link":"context","snippet":"context","position":3,
            "title":"context","link":"context","snippet":"context","position":4,
            ...
            "title":"context","link":"context","snippet":"context","position":10,
            ]

        If a sentence comes from multiple contexts, please list all applicable citations, like [position:3][position:5].
        Other than code and specific names and citations, your answer must be written in the same language as the question.

        Here are the set of contexts:
        '{context}'

        Remember, don't blindly repeat the contexts verbatim. And here is the user question:
        '{query}'
    """

    from lmchain.agents import AgentZhipuAI
    llm = AgentZhipuAI()
    response = llm(prompt)
    print(response)


