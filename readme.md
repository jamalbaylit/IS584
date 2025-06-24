# 🧠 RAG Application

A Retrieval-Augmented Generation (RAG) system built with vector database integration.

## Prerequisites

- Docker and Docker Compose
- Python 3.x
- pip (Python package manager)

**⚠️ Note:** It is recommended to use Ubuntu operating system


## 🚀 Setup Instructions

### 1. Install Tkinter for Ubuntu

Install the Tkinter for figures:

```bash
pip install -r requirements.txt
```
### 1. Install Python Dependencies

```bash
sudo apt-get install python3-tk

### 2. Start Vector Database

First, start the vector database using Docker Compose:

```bash
docker-compose up -d
```

**📌 Note:** For newer versions of Docker Compose, use `docker compose up -d` (without the hyphen).

### 3. Create Data Model

Initialize the database schema by running:

```bash
python -m src.db.models
```

### 4. Populate Database

Fill the database with initial data:

```bash
python -m src.db.populate
```

## Quick Start

Follow these steps in order to create and populate database:

1. `docker-compose up -d` (or `docker compose up -d` for newer versions)
2. `python -m src.db.models`
3. `python -m src.db.populate`

Your RAG system should now be ready to use!































