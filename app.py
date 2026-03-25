import gradio as gr
from summarizer import (
    summarize_long_text,
    summarize_with_focus,
    generate_tldr,
    count_words
)

def process_summary(text, summary_type, focus_area=None):
    if not text.strip():
        return "Please enter text to summarize.", ""
    
    word_count = count_words(text)
    word_info = f"📊 Word count: {word_count} | Using local model (free, private)"
    
    if summary_type == "Standard Summary":
        result = summarize_long_text(text, "concise")
    elif summary_type == "Detailed Summary":
        result = summarize_long_text(text, "detailed")
    elif summary_type == "Bullet Points":
        result = summarize_long_text(text, "bullet")
    elif summary_type == "Executive Summary":
        result = summarize_long_text(text, "executive")
    elif summary_type == "TL;DR":
        result = generate_tldr(text)
    elif summary_type == "Focus Area" and focus_area:
        result = summarize_with_focus(text, focus_area)
    else:
        result = "Please select a valid summary type"
    
    return result, word_info







with gr.Blocks(title="Local Smart Summarizer") as demo:
    gr.Markdown("""
    # 📝 Local Smart Summarizer
    
    **No API key needed!** Uses Llama 3.2 running locally via Ollama.
    Your data stays private and free.
    
    ### Setup:
    1. Install Ollama: https://ollama.com
    2. Run: `ollama pull llama3.1`
    3. Keep Ollama running in background
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            text_input = gr.Textbox(
                label="Your Text",
                placeholder="Paste your article, document, or transcript here...",
                lines=15
            )
            
            with gr.Row():
                summary_type = gr.Dropdown(
                    choices=[
                        "Standard Summary",
                        "Detailed Summary",
                        "Bullet Points",
                        "Executive Summary",
                        "TL;DR",
                        "Focus Area"
                    ],
                    label="Summary Type",
                    value="Standard Summary"
                )
                
                focus_input = gr.Textbox(
                    label="Focus Area",
                    placeholder="e.g., technical details, business implications",
                    lines=1
                )
            
            submit_btn = gr.Button("Summarize", variant="primary")
        
        with gr.Column(scale=1):
            word_info = gr.Textbox(label="Info", interactive=False)
            summary_output = gr.Textbox(label="Summary", lines=20, interactive=False)
    
    submit_btn.click(
        fn=process_summary,
        inputs=[text_input, summary_type, focus_input],
        outputs=[summary_output, word_info]
    )

if __name__ == "__main__":
    demo.launch(share=True)