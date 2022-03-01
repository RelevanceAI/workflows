"""Setting up the client
"""
import re
import emoji
from relevanceai import Client
from pathlib import Path
from read_nb import (
    get_description,
    get_documentation_link,
    get_prerequisites,
    get_use_cases,
    get_video_link,
)

# Support Relevance AI Account
client = Client()

ds = client.Dataset("workflows-data")

files = list(Path("workflows").rglob("*.ipynb"))
# This generate the following file name
# 'workflows/bias-detection/✨Vector_Based_Bias_Detection_With_Relevance_AI.ipynb'
# https://colab.research.google.com/github/RelevanceAI/workflows/blob/main/cluster-reporting/%F0%9F%91%8D_Cluster_Reports_With_Relevance_AI.ipynb

def get_colab_link(fn):
    # Converts from 1st row to second row
    # 'workflows/bias-detection/✨Vector_Based_Bias_Detection_With_Relevance_AI.ipynb'
    # https://colab.research.google.com/github/RelevanceAI/workflows/blob/main/cluster-reporting/%F0%9F%91%8D_Cluster_Reports_With_Relevance_AI.ipynb
    colab_link = f"https://colab.research.google.com/github/RelevanceAI/workflows/blob/main/{fn}"
    return colab_link

def deEmojify(text):
    regrex_pattern = re.compile(
        pattern="["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    return regrex_pattern.sub(r"", text)

def remove_emoji(string):
    return emoji.get_emoji_regexp().sub("", string)

documents = []

# for fn in files:
#     doc = {}
#     fn_string = fn.__str__()
#     fn_string = fn_string.split("/")[-1].split(".")[0].replace("_", " ")
#     fn_string = fn_string.lower().replace("with relevance ai", "")
#     fn_string = fn_string.title()
#     fn_string = remove_emoji(fn_string).strip()
#     doc["_id"] = fn_string.replace(" ", "-").lower()
#     doc["title"] = fn_string
#     doc["description"] = get_description(fn)
#     doc["colab_link"] = get_colab_link(fn)
#     doc["prerequisites"] = get_prerequisites(fn)
#     doc["use_cases"] = get_use_cases(fn)
#     doc["documentation_link"] = get_documentation_link(fn)
#     doc["video_link"] = get_video_link(fn)

# import json
# json.dump(documents, open("sample_documents.json", "w"))

bias_document = {
    "_id" : "bias-detection",
    "title": "Bias Detection",
    "description": "Detect bias in your NLP models.",
    "colab_link": "https://colab.research.google.com/github/RelevanceAI/workflows/blob/main/cluster-reporting/%F0%9F%91%8D_Cluster_Reports_With_Relevance_AI.ipynb",
    "use_cases": ["Gender bias"],
    "documentation_links": [],
    "video_links": [],
    "prerequisites": ["Dataset with vectors"],
}

vectorize_document = {
    "_id" : "cluster-reports",
    "colab_link": "https://colab.research.google.com/github/RelevanceAI/workflows/blob/main/cluster-reporting/%F0%9F%91%8D_Cluster_Reports_With_Relevance_AI.ipynb",
    "title": "Cluster Evaluation Report",
    "description": "Metrics and analysis reports for cluster models",
    "prerequisites": ["Clustered Dataset with vectors"],
    "use_cases": [],
    "documentation_links": [{"title": "Cluster Evaluation Report", "url": "https://relevanceai.readthedocs.io/en/development/relevanceai.cluster_report.html#"}],
    "video_links": []
}

results = ds.upsert_documents(
    [bias_document, vectorize_document]
)
print(results)

# results = client.admin.request_read_api_key(read_username="workflow-dashboard")
# print(results)
