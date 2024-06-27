import gradio as gr
import asyncio
from index import async_parse_resume, async_generate_cover_letter, load_config

# Load YAML configuration
config = load_config('index.yaml')

# Define Asyncflows tasks based on YAML flow definition
async def run_flow(resume_content, job_description):
    # Call Asyncflows backend functions
    parsed_resume = await async_parse_resume(resume_content)
    result = await async_generate_cover_letter(parsed_resume, job_description, config)
    
    return result

# Gradio interface function
def cover_letter_generator(resume_file, job_description):
    # Extract resume content from NamedString object
    resume_content = resume_file
    
    # Call Asyncflows flow defined in YAML
    result = asyncio.run(run_flow(resume_content, job_description))
    
    return result

# Define Gradio interface components inside the function to avoid circular import issues
inputs = [
    gr.File(label="Upload Resume", type="filepath"),  # File upload component
    gr.Textbox(label="Job Description")  # Text input component for job description
]

output_text = gr.Textbox(label="Cover Letter", placeholder="Generated Cover Letter will appear here.")

# Create Gradio interface using 'gr.Interface' directly from Gradio module
interface = gr.Interface(fn=cover_letter_generator, inputs=inputs, outputs=output_text)

# Launch the Gradio interface
if __name__ == "__main__":
    interface.launch()
