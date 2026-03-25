# Smart Text Summarizer

A text summarization tool that runs locally using Ollama. Free, private, no API keys needed.

## Features

- Multiple summary types: concise, detailed, bullet points, executive summary, TL;DR
- Focus on specific topics (e.g., "summarize focusing on challenges")
- Handles long texts by automatic chunking
- Web interface with Gradio

## Installation

1. Install Ollama for windows: https://ollama.com OR install Ollama for Linux curl -fsSL https://ollama.com/install.sh | sh

2. Pull a model:
   ```bash
   ollama pull llama3.1 



3. install python packages 
pip install gradio requests 




## Usage 
python app.py 

and open the local host on your browser 




## How It Works
1. Text is split into chunks if too long
2. Each chunk is sent to Ollama for summarization
3. Chunk summaries are combined into final summary



## Files

- summarizer.py - Core summarization logic
- app.py - Gradio web interface