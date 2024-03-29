"""
This file uploads 2 things:
- workflows
- recipes

Workflows go into "workflows-data"
Recipes go into "workflows-recipes"
"""
import os
from relevanceai import Client

import argparse


# def main(args):

client = Client(token=os.getenv("SUPPORT_ACTIVATION_TOKEN"))

ds = client.Dataset("workflows-recipes")

COLAB_PREFIX = (
    "https://colab.research.google.com/github/RelevanceAI/workflows/blob/main/"
)
WORKFLOWS = [
    ############### CORE WORKFLOWS
    {
        "_id": "core-vectorize",
        "type": "core-workflow",
        "title": "Vectorizing with Relevance AI",
        "description": "Vectorize your data with Relevance AI",
        "colab_link": COLAB_PREFIX
        + "workflows/vectorize/Vectorize_Your_Data_with_Relevance_AI.ipynb",
        "use_cases": ["Encoding data for further downstream tasks"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/latest/operations/vectorize.html",
            }
        ],
        "video_links": [],
        "new": False,
        "prerequisites": ["Uploaded dataset with text or image fields"],
        ## https://api-dev.ap-southeast-2.relevance.ai/latest/documentation#tag/workflows `notebook_path` parameter refers to `suffix`
        "suffix": "vectorize/Vectorize_Your_Data_with_Relevance_AI_params.ipynb",
    },
    {
        "_id": "core-dr",
        "type": "core-workflow",
        "colab_link": COLAB_PREFIX
        + "workflows/dr/Reduce_the_Dimensions_of_Your_Data_with_Relevance_AI.ipynb",
        "title": "Reduce the Dimensions of Your Data with Relevance AI",
        "description": "Reduce vector fields in your dataset down to fewer dimensions for easier visualisation (e.g. our 3D projector)",
        "prerequisites": ["Vectorised text or image fields in your dataset"],
        "use_cases": [],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "SDK Reference": "https://relevanceai.readthedocs.io/en/latest/operations/dim_reduction.html",
            }
        ],
        "video_links": [
            {"dr-workflows": "https://files.relevance.ai/v/2kFOGHU2jN6sKOx4NGl4"}
        ],
        "new": False,
        "core": True,
        ## https://api-dev.ap-southeast-2.relevance.ai/latest/documentation#tag/workflows `notebook_path` parameter refers to `suffix`
        "suffix": "dr/Reduce_the_Dimensions_of_Your_Data_with_Relevance_AI_params.ipynb",
    },
    {
        "_id": "core-cluster",
        "type": "core-workflow",
        "title": "Clustering with Relevance AI",
        "description": "Cluster your data with Relevance AI",
        "colab_link": COLAB_PREFIX
        + "workflows/cluster/Cluster_Your_Data_with_Relevance_AI.ipynb",
        "use_cases": ["Unsupervised clustering of data", "Finding themes in your data"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/latest/operations/cluster/basic.html",
            }
        ],
        "video_links": [],
        "new": False,
        "prerequisites": ["Vectorised some fields in your data"],
        ## https://api-dev.ap-southeast-2.relevance.ai/latest/documentation#tag/workflows `notebook_path` parameter refers to `suffix`
        "suffix": "cluster/Cluster_Your_Data_with_Relevance_AI_params.ipynb",
    },
    {
        "_id": "core-subclustering",
        "type": "core-workflow",
        "title": "Subclustering",
        "description": "Dive deeper into your clusters with subclustering",
        "colab_link": COLAB_PREFIX + "workflows/subclustering/core_subclustering.ipynb",
        "use_cases": ["Drilling down into your clusters with subclustering"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/latest/operations/cluster/subclustering.html",
            }
        ],
        "video_links": [],
        "new": False,
        "prerequisites": ["Vectorised text or image fields in your dataset"],
        ## https://api-dev.ap-southeast-2.relevance.ai/latest/documentation#tag/workflows `notebook_path` parameter refers to `suffix`
        "suffix": "subclustering/core_subclustering_params.ipynb",
    },
    # {
    #     "_id": "bias-detection",
    #     "type": "workflow",
    #     "title": "Bias Detection",
    #     "description": "Detect bias in your vectorizers",
    #     "colab_link": COLAB_PREFIX
    #     + "workflows/bias-detection/✨Vector_Based_Bias_Detection_With_Relevance_AI.ipynb",
    #     "use_cases": ["Gender bias", "Category bias", "Unsupervised bias detection"],
    #     "documentation_links": [
    #         {
    #             "title": "SDK Reference",
    #             "url": "https://relevanceai.readthedocs.io/en/latest/autoapi/relevanceai/utils/bias_detection/bias_plot/index.html",
    #         }
    #     ],
    #     "video_links": [],
    #     "new": False,
    #     "prerequisites": [
    #         "List of bias categories",
    #         "List of data items (images/text) to vectorize",
    #         "Vectorizer",
    #     ],
    #     ## workflows-deploy reads notebook_path from these fields
    #     "suffix": "bias-detection/✨Vector_Based_Bias_Detection_With_Relevance_AI_params.ipynb",
    #     "s3_url": {
    #         "dev": "s3://relevanceai-workflows-701405094693-ap-southeast-2/dev/bias-detection/✨Vector_Based_Bias_Detection_With_Relevance_AI_params.ipynb",
    #         "stg": "s3://relevanceai-workflows/dev/bias-detection/✨Vector_Based_Bias_Detection_With_Relevance_AI_params.ipynb",
    #     },
    # },
    {
        "_id": "taxonomy",
        "type": "workflow",
        "title": "Add Taxonomy",
        "description": "Insert your taxonomy into Relevance AI",
        "colab_link": COLAB_PREFIX + "workflows/taxonomy/Taxonomy.ipynb",
        "use_cases": ["Label your data with a pre-determined taxonomy."],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/development/operations/label.html",
            }
        ],
        "video_links": [],
        "new": False,
        "prerequisites": ["Taxonomy you would like to insert", "Dataset with text"],
        ## https://api-dev.ap-southeast-2.relevance.ai/latest/documentation#tag/workflows `notebook_path` parameter refers to `suffix`
        "suffix": "workflows/taxonomy/Taxonomy_Core_params.ipynb",
    },
    # {
    #     "_id": "cluster-reports",
    #     "colab_link": COLAB_PREFIX
    #     + "workflows/cluster-reporting/👍_Cluster_Reports_With_Relevance_AI.ipynb",
    #     "type": "workflow",
    #     "title": "Cluster Evaluation Report",
    #     "description": "Automatically analyse your clusters using a variety of metrics to improve cluster performance",
    #     "prerequisites": [
    #         "A dataset with vectors and clusters OR",
    #         "An X array with cluster labels and clustering model",
    #     ],
    #     "use_cases": [
    #         "Ensuring proper topics are extracted",
    #         "Ensuring customers are properly segmented",
    #     ],
    #     "documentation_links": [
    #         {
    #             "title": "SDK Reference",
    #             "url": "https://relevanceai.readthedocs.io/en/latest/operations/cluster/report.html",
    #         }
    #     ],
    #     "video_links": [],
    #     "new": False,
    #     ## workflows-deploy reads notebook_path from these fields
    #     "suffix": "cluster-reporting/👍_Cluster_Reports_With_Relevance_AI_params.ipynb",
    #     "s3_url": {
    #         "dev": "s3://relevanceai-workflows-701405094693-ap-southeast-2/dev/cluster-reporting/👍_Cluster_Reports_With_Relevance_AI_params.ipynb",
    #         "stg": "s3://relevanceai-workflows/dev/cluster-reporting/👍_Cluster_Reports_With_Relevance_AI_params.ipynb",
    #     },
    # },
    {
        "_id": "subclustering",
        "type": "workflow",
        "colab_link": COLAB_PREFIX
        + "workflows/subclustering/basic_subclustering.ipynb",
        "title": "Advanced Subclustering",
        "description": "Clustering within clusters",
        "prerequisites": ["A dataset with vectors and clusters"],
        "use_cases": [
            "Infinitely drilling down into your clusters to see what they comprise of"
        ],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/development/subclustering.html",
            }
        ],
        "video_links": [],
        "new": False,
        ## workflows-deploy reads notebook_path from these fields
        "suffix": "subclustering/basic_subclustering_params.ipynb",
    },
    ##### Non core workflows
    #     {
    #         "_id": "impact-analysis",
    #         "type": "workflow",
    #         "colab_link": COLAB_PREFIX + "workflows/impact-analysis/impact-analysis.ipynb",
    #         "title": "Feature/Impact Analysis",
    #         "description": "Analyse the impact of your features and directly assess how important they are and their local/global impact on the KPI or metric.",
    #         "prerequisites": [
    #             "Dataset with encoded vectors and a variable to measure importance."
    #         ],
    #         "use_cases": ["KPI Measurement", "Impact Analysis"],
    #         "documentation_links": [],
    #         "video_links": [],
    #         "new": True,
    #         "coming_soon": False,
    #         ## https://api-dev.ap-southeast-2.relevance.ai/latest/documentation#tag/workflows `notebook_path` parameter refers to `suffix`
    #         "suffix": "impact-analysis/impact-analysis_params.ipynb"
    #     },
    {
        "_id": "keyphrases",
        "type": "workflow",
        "colab_link": COLAB_PREFIX + "workflows/keyphrases/KeyPhrases_Workflow.ipynb",
        "title": "Keyphrases",
        "description": "Identify the most common keyphrases in a text field and clusters and see how we enable infinite hacking to finetune your keyphrases.",
        "prerequisites": ["Text fields", "(Optional) Cluster fields"],
        "use_cases": ["Automated keyphrase detection in clusters"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/latest/operations/label.html?highlight=keyphrases#relevanceai.operations.labels.labels.LabelOps.keyphrases",
            }
        ],
        "video_links": [],
        "new": False,
        ## https://api-dev.ap-southeast-2.relevance.ai/latest/documentation#tag/workflows `notebook_path` parameter refers to `suffix`
        "suffix": "keyphrases/KeyPhrases_Workflow_params.ipynb",
    },
    {
        "_id": "vector-rake",
        "title": "Vector-Rake Keyphrases",
        "description": "Keyphrase extraction using a nearest-neighbor algorithm on top of the normal RAKE algorithm",
        "colab_link": COLAB_PREFIX + "workflows/vector-rake/vector_rake.ipynb",
        "use_cases": ["auto-labeling documents"],
        "documentation_links": [],
        "video_links": [],
        "new": False,
        "prerequisites": [
            "dataset with text field",
            "vectorized text field",
            "vectorizer",
        ],
        ## https://api-dev.ap-southeast-2.relevance.ai/latest/documentation#tag/workflows `notebook_path` parameter refers to `suffix`
        "suffix": "vector-rake/vector_rake_params.ipynb",
    },
    {
        "_id": "most-common-words-in-clusters",
        "type": "workflow",
        "colab_link": COLAB_PREFIX
        + "workflows/most-common-words-in-clusters/most-common-words-in-clusters.ipynb",
        "title": "Most Frequent Phrases In Clusters",
        "description": "Update your cluster explorer with the most frequently occurring word labels!",
        "prerequisites": ["Text fields", "Cluster fields", "Existing Deployable"],
        "use_cases": ["Automated Cluster Labelling"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/latest/operations/label.html",
            }
        ],
        "video_links": [],
        "new": False,
        "coming_soon": False,
        ## https://api-dev.ap-southeast-2.relevance.ai/latest/documentation#tag/workflows `notebook_path` parameter refers to `suffix`
        "suffix": "most-common-words-in-clusters/most-common-words-in-clusters_params.ipynb",
    },
    {
        "_id": "community-detection",
        "type": "workflow",
        "colab_link": COLAB_PREFIX
        + "workflows/community-detection/Community_Detection_with_Relevance_AI.ipynb",
        "title": "Community Detection",
        "description": "Detect communities, or clusters, among embedding-transformed text fields or vectors.",
        "prerequisites": ["Text fields", "(Optional) Cluster fields"],
        "use_cases": ["Community detection of text fields and vectors"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/latest/operations/cluster/basic.html",
            }
        ],
        "video_links": [],
        "new": False,
        ## workflows-deploy reads notebook_path from these fields
        "suffix": "community-detection/Community_Detection_with_Relevance_AI_params.ipynb",
    },
    {
        "_id": "media-upload",
        "type": "workflow",
        "colab_link": COLAB_PREFIX
        + "workflows/media_upload/💡_Upload_Audio_Images_Videos_Flow.ipynb",
        "title": "Media Upload",
        "description": "Learn how to upload images/videos/audio files to Relevance AI!",
        "prerequisites": [
            "Images or other media files to upload. These can be local or hosted online somewhere else already."
        ],
        "use_cases": ["Processing local files with RelevanceAI!"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/latest",
            }
        ],
        "video_links": [],
        "new": False,
        "core": False,
        ## https://api-dev.ap-southeast-2.relevance.ai/latest/documentation#tag/workflows `notebook_path` parameter refers to `suffix`
        "suffix": "media_upload/💡_Upload_Audio_Images_Videos_Flow_params.ipynb",
    },
    {
        "_id": "sentiment",
        "type": "workflow",
        "colab_link": COLAB_PREFIX + "workflows/sentiment/Sentiment.ipynb",
        "title": "Advanced Sentiment",
        "description": "Add positive/negative/neutral sentiment to your text fields.",
        "prerequisites": ["Dataset with text field"],
        "use_cases": ["Sentiment analysis."],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/latest/operations/sentiment.html",
            }
        ],
        "video_links": [],
        "new": False,
        "core": False,
        "suffix": "sentiment/Sentiment_core_params.ipynb",
    },
        {
        "_id": "tag-comparison-export",
        "type": "workflow",
        "colab_link": COLAB_PREFIX + "workflows/export/Tag_Comparison_Export.ipynb",
        "title": "Tag Comparison Export",
        "description": "Export for tag comparison",
        "prerequisites": ["Dataset with tags"],
        "use_cases": ["QResearch Tag Comparisons"],
        "documentation_links": [
        ],
        "video_links": [],
        "new": False,
        "core": False,
        # "suffix": "sentiment/Sentiment_core_params.ipynb",
    },
    # {
    #     "_id": "emotion",
    #     "type": "workflow",
    #     "colab_link": COLAB_PREFIX + "workflows/emotion/emotion_form.ipynb",
    #     "title": "Extract Emotion",
    #     "description": "Extract emotion from text field",
    #     "prerequisites": ["Dataset with text field"],
    #     "use_cases": ["Extracting emotion from text fields"],
    #     "documentation_links": [
    #         {
    #             "title": "SDK Reference",
    #             "url": "https://relevanceai.readthedocs.io/en/latest/autoapi/relevanceai/operations_new/ops/index.html?highlight=extract_ner#relevanceai.operations_new.ops.Operations.extract_emotion",
    #         }
    #     ],
    #     "video_links": [],
    #     "new": True,
    #     "core": False,
    #     "suffix": "emotion/emotion_params.ipynb",
    # },
    {
        "_id": "explain-text-clusters",
        "type": "workflow",
        "colab_link": COLAB_PREFIX
        + "workflows/explain-text-clusters/explain-text-clusters_form.ipynb",
        "title": "Highlight/Explain text clusters",
        "description": "Explain text clusters by highlighting the parts that are most relevant",
        "prerequisites": ["Dataset with text field", "Ran clustering workflow"],
        "use_cases": ["Explaining text clusters"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/development/operations/cluster/explain_text_clusters.html",
            }
        ],
        "video_links": [],
        "new": False,
        "core": False,
    },
    {
        "_id": "fit-to-smaller-dataset",
        "type": "workflow",
        "colab_link": COLAB_PREFIX
        + "workflows/filter_to_smaller_dataset/Filter_To_Smaller_Dataset.ipynb",
        "title": "Filter to smaller dataset",
        "description": "Speed up dashboards as operations run on smaller amounts of data. They can also be great for testing functions really quickly.",
        "prerequisites": ["Dataset"],
        "use_cases": ["Faster dashboards", "Bigger Focus", "Testing"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/latest/core/dataset/useful_utilities.html",
            }
        ],
        "video_links": [],
        "new": False,
        "core": False,
    },
    # {
    #     "_id": "automated-taxonomy-builder",
    #     "type": "workflow",
    #     "colab_link": COLAB_PREFIX
    #     + "workflows/automated_taxonomy_builder_keyphrase/auto_taxonomy_builder_keyphrase.ipynb",
    #     "title": "Automated Taxonomy Builder",
    #     "description": "An automated taxonomy builder without requiring an input list.",
    #     "prerequisites": ["Dataset with text fields"],
    #     "use_cases": [
    #         "Allow data to drive insights automatically based on keyphrase extraction"
    #     ],
    #     "documentation_links": [
    #         {
    #             "title": "SDK Reference",
    #             "url": "https://relevanceai.readthedocs.io/en/latest/core/dataset/useful_utilities.html",
    #         }
    #     ],
    #     "video_links": [],
    #     "new": False,
    #     "core": False,
    # },
    # {
    #     "_id": "automated-taxonomy-builder-advaned",
    #     "type": "workflow",
    #     "colab_link": COLAB_PREFIX
    #     + "workflows/automated_taxonomy_builder_keyphrase/auto_taxonomy_builder_keyphrase_advanced.ipynb",
    #     "title": "Advanced Automated Taxonomy Builder",
    #     "description": "An advanced automated taxonomy builder without requiring an input list.",
    #     "prerequisites": ["Dataset with text fields"],
    #     "use_cases": [
    #         "Allow data to drive insights automatically based on keyphrase extraction"
    #     ],
    #     "documentation_links": [
    #         {
    #             "title": "SDK Reference",
    #             "url": "https://relevanceai.readthedocs.io/en/latest/core/dataset/useful_utilities.html",
    #         }
    #     ],
    #     "video_links": [],
    #     "new": False,
    #     "core": False,
    # },
    {
        "_id": "sentiment-wordbubbles",
        "type": "workflow",
        "colab_link": COLAB_PREFIX
        + "workflows/sentiment_wordbubbles/sentiment_word_bubbles.ipynb",
        "title": "Sentiment Wordbubbles",
        "description": "Sentiment wordbubbles help you quickly identify which groups to dive further into",
        "prerequisites": [
            "Dataset with sentiment field - must have run sentiment workflow."
        ],
        "use_cases": ["A sentiment overview to identify areas to explore more into."],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/latest/core/dataset/useful_utilities.html",
            }
        ],
        "video_links": [],
        "new": False,
        "core": False,
    },
    {
        "_id": "byo-clusters",
        "type": "workflow",
        "colab_link": COLAB_PREFIX
        + "workflows/insertion/byo_cluster/byo_cluster.ipynb",
        "title": "BYO Clusters",
        "description": "Bring your own clusters into Relevance AI and unlock all our powerful functionality",
        "prerequisites": ["Vector field", "Your own categories"],
        "use_cases": ["Bring your own clusters to view breakdowns of your own data!"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/latest/core/dataset/useful_utilities.html",
            }
        ],
        "video_links": [],
        "new": False,
        "core": False,
        # "suffix": "insertion/byo_cluster/byo_cluster.ipynb",
    },
    {
        "_id": "insert-excel",
        "type": "workflow",
        "colab_link": COLAB_PREFIX
        + "workflows/insertion/inserting_excel_files/inserting_excel_files.ipynb",
        "title": "Inserting Excel File",
        "description": "Insert an .xlsx file or other type of Excel file.",
        "prerequisites": ["Excel file"],
        "use_cases": ["Insert an Excel file with Relevance AI"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/latest/core/dataset/useful_utilities.html",
            }
        ],
        "video_links": [],
        "new": False,
        "core": False,
        # "suffix": "insertion//byo_cluster.ipynb",
    },
    {
        "_id": "csv-insert",
        "type": "workflow",
        "colab_link": COLAB_PREFIX + "workflows/insertion/insert_csvs/Insert_CSV_Workflow.ipynb",
        "title": "Insert CSV with Colab",
        "description": "Insert a CSV reliably using Colab. This can be used as an alternative way to uploading via the UI.",
        "prerequisites": ["A CSV file"],
        "use_cases": [],
        "documentation_links": [
            {
                "title": "Insert CSV",
                "url": "https://sdk.relevance.ai/docs/inserting-files",
            }
        ],
        "video_links": [],
        "new": False,
        "core": False,
    },
    {
        "_id": "bulk-apply",
        "type": "workflow",
        "colab_link": COLAB_PREFIX + "workflows/bulk_apply/Bulk_Apply.ipynb",
        "title": "Bulk Apply",
        "description": "Process documents incredibly fast with Relevance AI",
        "prerequisites": ["Dataset"],
        "use_cases": [],
        "documentation_links": [
            {
                "title": "Process documents incredibly fast with Relevance AI",
                "url": "https://relevanceai.readthedocs.io/en/latest/core/dataset/useful_utilities.html",
            }
        ],
        "video_links": [],
        "new": False,
        "core": False,
    },
    {
        "_id": "export-to-csv",
        "type": "workflow",
        "colab_link": COLAB_PREFIX + "workflows/export/Export_to_CSV.ipynb",
        "title": "Export to CSV",
        "description": "Export datasets to CSV.",
        "prerequisites": ["Dataset"],
        "use_cases": [],
        "documentation_links": [],
        "video_links": [],
        "new": False,
        "core": False,
    },
    ############### COMING SOON WORKFLOWS
    {
        "_id": "pdf-ingestion",
        "type": "workflow",
        "colab_link": None,
        "title": "Insert PDFs",
        "description": "Insert highly unstructured PDFs in order to search images, flowcharts and build other vector applications/insights.",
        #             "prerequisites": ["Mp4 video"],
        #             "use_cases": ["Video Search"],
        #             "documentation_links": [{"title":"SDK Reference", "url":  "https://relevanceai.readthedocs.io/en/latest/dataset.html#relevanceai.dataset_api.dataset_operations.Operations.keyphrases"}],
        #             "video_links": [],
        # "new": True,
        "coming_soon": True,
    },
    {
        "_id": "multi-vector-field-clustering",
        "type": "workflow",
        "colab_link": None,
        "title": "Multi vector field clustering",
        "description": "Multi-vector field clustering",
        #             "prerequisites": ["Mp4 video"],
        #             "use_cases": ["Video Search"],
        #             "documentation_links": [{"title":"SDK Reference", "url":  "https://relevanceai.readthedocs.io/en/latest/dataset.html#relevanceai.dataset_api.dataset_operations.Operations.keyphrases"}],
        #             "video_links": [],
        # "new": True,
        "coming_soon": True,
    },
    {
        "_id": "video-clusters",
        "type": "workflow",
        # "colab_link": COLAB_PREFIX + "workflows/keyphrases/KeyPhrases_Workflow.ipynb",
        "title": "Video Clustering",
        "description": "Get clusters to determine key different scenes in your video.",
        #             "prerequisites": ["Mp4 video"],
        #             "use_cases": ["Video Search"],
        #             "documentation_links": [{"title":"SDK Reference", "url": "https://relevanceai.readthedocs.io/en/latest/dataset.html#relevanceai.dataset_api.dataset_operations.Operations.keyphrases"}],
        #             "video_links": [],
        #             "new": True,
        "coming_soon": True,
    },
    {
        "_id": "video-search",
        "type": "workflow",
        # "colab_link": COLAB_PREFIX + "workflows/keyphrases/KeyPhrases_Workflow.ipynb",
        "title": "Video Search",
        "description": "Search videos using text to find the right frame you want.",
        "prerequisites": ["Mp4 video"],
        "use_cases": ["Video Search"],
        # "documentation_links": [
        #     {
        #         "title":"SDK Reference", "url": "https://relevanceai.readthedocs.io/en/latest/dataset.html#relevanceai.dataset_api.dataset_operations.Operations.keyphrases"
        #     }
        # ],
        # "video_links": [],
        # "new": True,
        "coming_soon": True,
    },
    ############### RECIPES
    {
        "_id": "dummy-datasets",
        "type": "dummy-dataset",
        "colab_link": COLAB_PREFIX
        + "workflows/dummy-datasets/Dummy_Datasets_Workflow.ipynb",
        "title": "Insert A Dummy Dataset",
        "description": "Insert a dummy dataset with this workflow.",
        "prerequisites": [],
        "use_cases": [],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/development/core/available_datasets.html",
            }
        ],
        "video_links": [],
        "new": False,
        "core": False,
        "suffix": "dummy-datasets/Dummy_Datasets_Workflow.ipynb",
    },
    {
        "_id": "pdf-search",
        "type": "recipe",
        "colab_link": None,
        "title": "PDF Search",
        "description": "Be able to search through all text and images in PDFs.",
        "prerequisites": ["PDFs"],
        "use_cases": ["PDF Search", "Flowchart Search"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/development/operations/search.html",
            }
        ],
        "video_links": [],
        #             "new": True,
        "coming": True,
    },
    {
        "_id": "figma-search",
        "type": "recipe",
        "colab_link": None,
        "title": "Figma Illustration Search",
        "description": "Upload all figma images and instantly be able to search them.",
        "prerequisites": ["Figma account"],
        "use_cases": ["Image Search", "Illustration search", "Designer Showcase"],
        "documentation_links": [
            {
                "title": "SDK Reference",
                "url": "https://relevanceai.readthedocs.io/en/development/operations/search.html",
            }
        ],
        "video_links": [],
        #             "new": True,
        "coming": True,
    },
    {
        "_id": "figma-clusters",
        "type": "recipe",
        "colab_link": None,
        "title": "Figma Illustration Clusters",
        "description": "Group your illustrations to promote natural discovery of your illustrations.",
        "prerequisites": ["Figma account"],
        "use_cases": ["Illustration Search", "Designer Discovery", "Drawing Discovery"],
        "documentation_links": [],
        "video_links": [],
        #             "new": True,
        "coming": True,
    },
    {
        "_id": "crunchbase-clusters",
        "type": "recipe",
        "colab_link": None,
        "title": "Crunchbase Cluster Analysis",
        "description": "Group companies to discover similar properties between your companies.",
        "prerequisites": ["Crunchbase account"],
        "use_cases": ["Competitor Analysis", "Crunchbase"],
        "documentation_links": [],
        "video_links": [],
        #             "new": True,
        "coming": True,
    },
    {
        "_id": "twitter-analysis",
        "type": "recipe",
        "colab_link": COLAB_PREFIX
        + "recipes/twitter-analysis/AI_Twitter_Analysis_by_Relevance_AI.ipynb",
        "title": "Twitter Analysis",
        "description": "Analyse your tweets and view which images and tweets are the most/least popular!",
        "prerequisites": ["No requirements."],  # not needed in future
        "use_cases": [
            "Analysing which tweets are the most popular."
        ],  # not needed in future
        "documentation_links": [],  # not needed in future
        "video_links": [],  # not needed in future
        "new": False,
        "recipe": True,  # Required for recipes
        "feature_image_url": "https://relevance.ai/wp-content/uploads/2022/03/image-6.png",
        "blog_link": "https://relevance.ai/twitter-data-workflow-how-to-run-twitter-account-data-analysis/",
        "recipe_url": "https://relevance.ai",
        "logo_url": "https://www.svgrepo.com/show/22159/twitter.svg",
        "suffix": "twitter-analysis/AI_Twitter_Analysis_by_Relevance_AI.ipynb",
    },
]


ds.delete()
results = ds.upsert_documents(WORKFLOWS)
print(results)


# if __name__ == "__main__":

#     parser = argparse.ArgumentParser()
#     parser.add_argument("-d", "--debug", action="store_true", help="Run debug mode")
#     parser.add_argument("-p", "--path", default=ROOT_PATH, help="Path of root folder")
#     parser.add_argument(
#         "-r", "--region", default="ap-southeast-2", help="Default region"
#     )
#     parser.add_argument(
#         "-n",
#         "--notebooks",
#         nargs="+",
#         default=None,
#         help="List of notebooks to execute",
#     )
#     parser.add_argument(
#         "-v",
#         "--version",
#         default=None,
#         help="Package Version",
#     )
#     parser.add_argument("-s", "--save", action="store_true", help="Run debug mode")
#     args = parser.parse_args()
#     main(args)
