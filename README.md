# Dockerized RAG Pipeline

![Build Status](https://img.shields.io/github/actions/workflow/status/yourusername/rag-pipeline/build.yml?branch=main)
![License](https://img.shields.io/github/license/yourusername/rag-pipeline)
![Docker Image Size](https://img.shields.io/docker/image-size/yourusername/rag-pipeline/latest)

## Table of Contents

- [📖 Introduction](#-introduction)
- [🚀 Features](#-features)
- [🔧 Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Build the Docker Image](#build-the-docker-image)
- [🐳 Usage](#-usage)
  - [Running the Container](#running-the-container)
  - [Using Volume Mounts](#using-volume-mounts)
- [🛠️ Development](#️-development)
  - [Running Locally](#running-locally)
  - [Testing](#testing)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [📫 Contact](#-contact)
- [🙏 Acknowledgements](#-acknowledgements)

## 📖 Introduction

The **Dockerized RAG Pipeline** is a **Retrieve and Generate (RAG)** pipeline designed for efficient document processing and query handling. This pipeline leverages **ChromaDB** for embedding storage and retrieval, and **FastAPI** for providing a robust API interface. Dockerization ensures consistent environments across development and production, simplifying deployment and scaling.

## 🚀 Features

- **Document Processing:** Efficiently process and store documents in `.docx` format.
- **Embedding Storage:** Utilize ChromaDB for scalable and fast embedding storage.
- **API Interface:** Interact with the pipeline through a FastAPI-powered API.
- **Dockerized Setup:** Simplify deployment with Docker, ensuring consistency across environments.
- **Scalable Architecture:** Designed to handle large volumes of documents and queries.

## 🔧 Installation

### Prerequisites

Ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/) (version 20.10.0 or higher)
- [Git](https://git-scm.com/downloads)

### Clone the Repository

```bash
git clone https://github.com/yourusername/rag-pipeline.git
cd rag-pipeline
