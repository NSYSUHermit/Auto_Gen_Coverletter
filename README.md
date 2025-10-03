# AI Cover Letter Generator

This script uses the Google Gemini API to automatically generate a professional and customized cover letter based on your resume and a specific job description.

## Features

- **AI-Powered**: Leverages the Gemini Pro model to create human-like, relevant content.
- **Configurable**: Easily change input files (resume, job description) and output directory via a `config.ini` file.
- **Customizable Prompt**: Modify the `prompt.txt` file to fine-tune the tone, style, and structure of the generated cover letter.
- **Safe API Key Handling**: Uses a `.env` file to keep your API key secure and out of the source code.

## Project Structure

```
cover-letter-generator/
├── generate_cover_letter.py  # The main Python script
├── config.ini                # Configuration for file paths
├── prompt.txt                # The prompt template for the AI
├── README.md                 # This file
├── .env                      # For storing your API key (create this yourself) 
├── input/
│   ├── my_resume.txt         # Your resume file
│   └── job_description.txt   # The job description file
└── output/
    └── (Generated cover letters will be saved here)
```

## Setup

1.  **Clone the repository or download the files.**

2.  **Install dependencies:**
    Make sure you have Python 3 installed. Then, install the required packages using pip:
    ```bash
    pip install google-generativeai python-dotenv
    ```

3.  **Get your API Key:**
    - Go to Google AI Studio.
    - Click "Create API key" to generate a new key.

4.  **Configure your API Key:**
    - In the root directory of the project (`cover-letter-generator/`), create a new file named `.env`.
    - Add your API key to the `.env` file like this:
      ```
      GOOGLE_API_KEY="YOUR_API_KEY_HERE"
      ```

5.  **Update Configuration (Optional):**
    - The `config.ini` file is pre-configured to use the files in the `input/` directory. If your files have different names or locations, update the paths in `config.ini`.

## Usage

1.  **Add your files:**
    - Place your resume content in `input/my_resume.txt`.
    - Place the job description you are applying for in `input/job_description.txt`.

2.  **Run the script:**
    - Open your terminal, navigate to the `cover-letter-generator` directory, and run the script:
      ```bash
      python generate_cover_letter.py
      ```

3.  **Find your cover letter:**
    - The script will generate a new cover letter and save it as a `.txt` file in the `output/` directory. The filename will include the job description's base name and a timestamp.
