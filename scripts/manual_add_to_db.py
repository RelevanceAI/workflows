from relevanceai import Client

# TODO: Add Github Action
client = Client(token="")

ds = client.Dataset("workflows-data")

COLAB_PREFIX = "https://colab.research.google.com/github/RelevanceAI/workflows/blob/main/"
DOCS = [
        {
            "_id" : "bias-detection",
            "title": "Bias Detection",
            "description": "Detect bias in your vectorizers",
            "colab_link": COLAB_PREFIX + "workflows/bias-detection/✨Vector_Based_Bias_Detection_With_Relevance_AI.ipynb",
            "use_cases": ["Gender bias", "Category bias", "Unsupervised bias detection"],
            "documentation_links": [{"title": "SDK Reference", "url": "https://relevanceai.readthedocs.io/en/development/relevanceai.bias_detection.html"}],
            "video_links": [],
            "new": True,
            "prerequisites": ["List of bias categories", "List of data items (images/text) to vectorize", "Vectorizer"],
        },
        {
            "_id" : "cluster-reports",
            "colab_link": COLAB_PREFIX + "workflows/cluster-reporting/%F0%9F%91%8D_Cluster_Reports_With_Relevance_AI.ipynb",
            "title": "Cluster Evaluation Report",
            "description": "Automatically analyse your clusters using a variety of metrics to improve cluster performance",
            "prerequisites": ["A dataset with vectors and clusters OR", "An X array with cluster labels and clustering model"],
            "use_cases": ["Ensuring proper topics are extracted", "Ensuring customers are properly segmented"],
            "documentation_links": [{"title": "SDK Reference", "url": "https://relevanceai.readthedocs.io/en/development/relevanceai.cluster_report.html#"}],
            "video_links": [],
            "new": True
        },
        {
            "_id" : "subclustering",
            "colab_link": COLAB_PREFIX + "workflows/subclustering/basic_subclustering.ipynb",
            "title": "Subclustering",
            "description": "Clustering within clusters",
            "prerequisites": ["A dataset with vectors and clusters"],
            "use_cases": ["Infinitely drilling down into your clusters to see what they comprise of"],
            "documentation_links": [{"title": "SDK Reference", "url": "https://relevanceai.readthedocs.io/en/development/subclustering.html"}],
            "video_links": [],
            "new": True
        },
        {
            "_id": "twitter-analysis",
            "colab_link": "https://colab.research.google.com/drive/1mPxekiRFEPea6XuOMIHMq54kCGBtMe26?usp=sharing",
            "title": "Twitter Analysis",
            "description": "Analyse your tweets and view which images and tweets are the most/least popular!",
            "prerequisites": ["No requirements."],
            "use_cases": ["Analysing which tweets are the most popular."],
            "documentation_links": [],
            "video_links": [],
            "new": True
        }
    ]

results = ds.upsert_documents(DOCS)
print(results)