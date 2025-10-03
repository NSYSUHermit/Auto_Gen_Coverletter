

import os
import google.generativeai as genai
import configparser
from dotenv import load_dotenv
import datetime
import PyPDF2
import docx

def load_api_key():
    """Loads the Google API key from the .env file."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file. Please create a .env file and add your API key.")
    return api_key

def read_file_content(file_path):
    """Reads and returns the content of a file, supporting both .txt and .pdf."""
    try:
        _, file_extension = os.path.splitext(file_path)
        
        if file_extension.lower() == '.pdf':
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                return text
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()

    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file at {file_path} was not found.")
    except Exception as e:
        raise Exception(f"An error occurred while reading {file_path}: {e}")

def generate_cover_letter(resume, job_description, prompt_template):
    """Generates a cover letter using the Gemini API."""
    try:
        genai.configure(api_key=load_api_key())
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = prompt_template.format(resume=resume, job_description=job_description)
        
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        raise Exception(f"An error occurred during AI generation: {e}")

def save_cover_letter(content, output_path, job_description_filename):
    """Saves the generated cover letter to a .docx file."""
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = os.path.splitext(os.path.basename(job_description_filename))[0]
        file_name = f"{base_filename}_cover_letter_{timestamp}.docx"
        
        full_path = os.path.join(output_path, file_name)
        
        document = docx.Document()
        document.add_paragraph(content)
        document.save(full_path)
            
        print(f"Cover letter saved successfully to: {full_path}")
    except Exception as e:
        raise Exception(f"An error occurred while saving the file: {e}")

def main():
    """Main function to run the cover letter generator."""
    try:
        # Read configs
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        paths = config['paths']
        resume_path = paths.get('resume')
        output_path = paths.get('output_directory')
        prompt_path = paths.get('prompt_template')

        jd_directory = os.path.dirname(paths.get('job_description', 'input/'))

        if not all([resume_path, output_path, prompt_path]):
            raise ValueError("Please ensure resume, output_directory, and prompt_template are set in config.ini.")

        # --- Interactive Job Description Selection ---
        try:
            jd_files = [f for f in os.listdir(jd_directory) if os.path.isfile(os.path.join(jd_directory, f)) and not f.startswith('.')]
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The job description directory '{jd_directory}' was not found.")

        if not jd_files:
            raise FileNotFoundError(f"No job description files found in the '{jd_directory}' directory.")

        print("\nPlease select a job description file:")
        for i, filename in enumerate(jd_files):
            print(f"  {i + 1}: {filename}")

        while True:
            try:
                choice = int(input(f"\nEnter the number (1-{len(jd_files)}): "))
                if 1 <= choice <= len(jd_files):
                    job_description_filename = jd_files[choice - 1]
                    job_description_path = os.path.join(jd_directory, job_description_filename)
                    break
                else:
                    print(f"Invalid number. Please enter a number between 1 and {len(jd_files)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        # --- End of Interactive Selection ---

        resume_content = read_file_content(resume_path)
        job_description_content = read_file_content(job_description_path)
        prompt_template_content = read_file_content(prompt_path)
        
        print("\nGenerating your cover letter...")
        
        generated_letter = generate_cover_letter(
            resume=resume_content,
            job_description=job_description_content,
            prompt_template=prompt_template_content
        )
        
        save_cover_letter(generated_letter, output_path, job_description_path)
        
    except (ValueError, FileNotFoundError, Exception) as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
