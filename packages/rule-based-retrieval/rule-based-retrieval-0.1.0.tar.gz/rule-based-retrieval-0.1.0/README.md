# WhyHow Rule-based Retrieval SDK

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)

The WhyHow Rule-based Retrieval SDK is a powerful Python package that enables you to create and manage Retrieval Augmented Generation (RAG) applications with advanced filtering capabilities. It seamlessly integrates with OpenAI for text generation and Pinecone for efficient vector database management.

# Installation

### Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Pinecone API key

### Install

To install the package you can first clone the repo

```shell
git clone git@github.com:whyhow-ai/rule-based-retrieval.git
cd rule-based-retrieval
pip install .

export OPENAI_API_KEY=<your open ai api key>
export PINECONE_API_KEY=<your pinecone api key>
```

### Developer Install 
For a developer installation, use an editable install and include the development dependencies:

```shell
pip install -e .[dev]
```

For ZSH:
```shell
pip install -e ".[dev]"
```

If you want to install the package directly without explicitly cloning yourself
run

```shell
pip install git+ssh://git@github.com/whyhow-ai/rule-based-retrieval
```


# Documentation
To serve the docs locally run

```shell
pip install -e .[docs]
mkdocs serve
```

For ZSH:
```shell
pip install -e ".[docs]"
mkdocs serve
```

Navigate to http://127.0.0.1:8000/ in your browser to view the documentation.

# Examples

Check out the `examples/` directory for sample scripts demonstrating how to use the WhyHow Rule-based Retrieval SDK.

# How to

## Create index & upload

```shell
from whyhow import Client

# Configure parameters
index_name = "whyhow-demo"
namespace = "demo"
pdfs = ["harry_potter_book_1.pdf"]

# Initialize client
client = Client()

# Create index
index = client.get_index(index_name)

# Upload, split, chunk, and vectorize documents in Pinecone
client.upload_documents(index=index, documents=pdfs, namespace=namespace)
```

## Query with rules

```shell
from whyhow import Client, Rule

# Configure query parameters
index_name = "whyhow-demo"
namespace = "demo"
question = "What does Harry wear?"
top_k = 5

# Initialize client
client = Client()

# Create rules
rules = [
    Rule(
        filename="harry_potter_book_1.pdf",
        page_numbers=[21, 22, 23]
    ),
    Rule(
        filename="harry_potter_book_1.pdf",
        page_numbers=[151, 152, 153, 154]
    )
]

# Run query
result = client.query(
    question=question,
    index=index,
    namespace=namespace,
    rules=rules,
    top_k=top_k,
)

answer = result["answer"]
used_contexts = [
    result["matches"][i]["metadata"]["text"] for i in result["used_contexts"]
]
print(f"Answer: {answer}")
print(
    f"The model used {len(used_contexts)} chunk(s) from the DB to answer the question"
)
```

# Contributing
We welcome contributions to improve the WhyHow Rule-based Retrieval SDK! If you have any ideas, bug reports, or feature requests, please open an issue on the GitHub repository.

If you'd like to contribute code, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with descriptive messages
4. Push your changes to your forked repository
5. Open a pull request to the main repository

### License
This project is licensed under the MIT License.

### Support
If you have any questions or need assistance, please contact us at team@whyhow.ai. We're here to help!
