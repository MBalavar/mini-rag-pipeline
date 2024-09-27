# Dockerized RAG Pipeline

![Build Status](https://img.shields.io/github/actions/workflow/status/yourusername/rag-pipeline/build.yml?branch=main)
![License](https://img.shields.io/github/license/yourusername/rag-pipeline)
![Docker Image Size](https://img.shields.io/docker/image-size/yourusername/rag-pipeline/latest)


## 📖 Introduction

The Dockerized RAG Pipeline is a Retrieve and Generate (RAG) pipeline designed for efficient document processing and query handling. This pipeline leverages ChromaDB for embedding storage and retrieval and uses the “t5-small” model to synthesise the final response as the generator. Dockerization ensures consistent environments across development and production, simplifying deployment and scaling.

## 🚀 Features

- Document Processing:** Efficiently process and store documents in `.docx` format.
- Embedding Storage:** Utilise ChromaDB for scalable and fast embedding storage.
- Dockerized Setup:** Simplify deployment with Docker, ensuring consistency across environments.
- Leveraging "t5-small" model for synthesising the final response.

## 🔧 Installation

### Prerequisites

Ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/) (version 20.10.0 or higher)
- [Git](https://git-scm.com/downloads)

To Process another .docx file, please upload your file as sample.docx in the root directory of the project.

To modify the query, please update the query in the test.py file.

### Clone the Repository

```bash
git clone https://github.com/yourusername/rag-pipeline.git
cd rag-pipeline

## Build the Docker Image
docker build -t mini-rag-pipeline:latest .

## Run the Docker Container
docker run --name rag-container mini-rag-pipeline:latest


