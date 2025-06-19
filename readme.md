# 🧠 RAG Application

A Retrieval-Augmented Generation (RAG) system built with vector database integration.

## Prerequisites

- Docker and Docker Compose
- Python 3.x

## 🚀 Setup Instructions

### 1. Start Vector Database

First, start the vector database using Docker Compose:

```bash
docker-compose up -d
```

**📌 Note:** For newer versions of Docker Compose, use `docker compose up -d` (without the hyphen).

### 2. Create Data Model

Initialize the database schema by running:

```bash
python -m db.model
```

### 3. Populate Database

Fill the database with initial data:

```bash
python -m db.populate
```

## Quick Start

Follow these steps in order:

1. `docker-compose up -d` (or `docker compose up -d` for newer versions)
2. `python -m db.model`
3. `python -m db.populate`

Your RAG system should now be ready to use!