# AccountantAI

## Overview
AccountantAI is a project designed to assist with financial tasks using AI-powered solutions.

## Setup Instructions

### Step 1: Clone the Repository
Clone this repository to your local machine:
```bash
git clone <repository-url>
```

### Step 2: Create a Virtual Environment
Navigate to the project directory and create a virtual environment:
```bash
cd AccountantAI
python -m venv venv
```

Activate the virtual environment:
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### Step 3: Install Dependencies
Install the required dependencies using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 4: Create a `.env` File
To use the OpenAI API, you need to create a `.env` file in the root of the project directory. This file will store your OpenAI API key securely.

1. In the root directory of the project, create a file named `.env`.
2. Add the following line to the file, replacing `your-api-key` with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key
   ```

### Step 5: Run the Application
Start the application using the following command:
```bash
python main.py
```

## Notes
- Ensure that your `.env` file is not shared or committed to version control to keep your API key secure.
- For more information about obtaining an OpenAI API key, visit [OpenAI's API documentation](https://platform.openai.com/docs/).

