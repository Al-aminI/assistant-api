# AI Assistant Application README

## Overview

This document provides a comprehensive guide to understanding and setting up the AI Assistant Application, a state-of-the-art solution designed to analyze PDF or CSV files and generate answers based on user prompts. The application uses AI techniques, integrates with multiple APIs, and leverages optimized architecture for seamless performance.

## Features

- **File Analysis**: Accepts PDF or CSV files for content analysis.
- **Prompt-based Querying**: Generates answers based on user prompts.
- **Reasoning Engine**: Executes Python code to reason through the content and prompt.
- **Database Integration**: Stores and retrieves relevant content using ChromaDB.
- **API Backend**: Built using Flask Python with structured MVC architecture.
- **Testing**: Includes comprehensive test coverage with Makefile and Docker configurations.
- **Environment Configuration**: Utilizes a `.env` file for managing environment variables.

## Architecture

The AI Assistant Application employs a world-class, industry-standard optimized architecture, encompassing the following components:

### Directory Structure

```
app/main/
│
├── controller/
│   └── .py
│
├── model/
│   └── .py
│
├── services/
│   
│   └── .py
│
├── utility/
│   └── .py
│
├── tests/
│   └── congig text
│
├── .env
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── manage.py
```

#### Components

- **Controller**: Handles API endpoints and request routing.
- **Model**: Defines the database schema and interacts with ChromaDB.
- **Services**: Contains business logic and data processing functions.
- **Utility**: Houses utility classes and functions.
- **Tests**: Includes integration tests.
- **Environment Configuration**: Stores environment variables in `.env` file.

## Setup Instructions

### Prerequisites

- Python 3.x
- Docker
- ChromaDB
- OpenAI API Key
- Fireworks API Key
- Tesseract OCR

### Installation Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Al-aminI/assistant-api.git
    cd assistant-api
    ```

2. **Set Environment Variables**

    Create a `.env` file in the root directory and set the following variables:

    ```env
    DATABASE_URL=your_database_url
    OPENAI_API_KEY=your_openai_api_key
    FIREWORKS_API_KEY=your_fireworks_api_key
    OCR=/usr/share/tesseract-ocr/4.00/tessdata
    IMAGES_UPLOAD=uploaded_images/
    FILES_UPLOAD=uploaded_files/
    ```


3. **Access API Endpoints**

    Once the application is running, you can access the API endpoints as defined in `controller/endpoints.py`.

## Testing

To run tests, execute the following command:

```bash
make test
```

This will run all the tests defined in the `tests/` directory.

## Documentation

Each function and module is thoroughly documented with comments for clarity and maintainability. The database schema is defined in `model`.


For any further assistance or inquiries, please contact alaminibrahim433@gmail.com.

---
