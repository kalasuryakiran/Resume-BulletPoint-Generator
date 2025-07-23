import os
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv

# ✅ Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# ✅ Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# 🧠 Prompt builder
def build_prompt(raw_experience):
    return f"""
You're a resume writing expert helping a fresher applying for software engineering roles.
Convert the experience below into a resume bullet point that highlights technical skills, leadership, or impact.
Use strong action verbs, quantify where possible, and keep it concise.

Experience: "{raw_experience}"
"""

# 🎯 Core generation function
def generate_bullet(raw_experience):
    if not raw_experience.strip():
        return "❗ Please enter your experience."
    
    prompt = build_prompt(raw_experience)
    response = model.generate_content(prompt)
    return response.text.strip()

# 🌐 Gradio UI
with gr.Blocks(title="Resume Bullet Point Generator") as demo:
    gr.Markdown("## ✨ AI Resume Bullet Generator\nEnter your raw experience below:")
    input_exp = gr.Textbox(label="Raw Experience", placeholder="e.g. I created a frontend using React and Firebase.")
    output_exp = gr.Textbox(label="Generated Resume Bullet Point", lines=3)
    btn = gr.Button("Generate")

    btn.click(fn=generate_bullet, inputs=input_exp, outputs=output_exp)

# 🚀 Launch the app
if __name__ == "__main__":
    demo.launch()
