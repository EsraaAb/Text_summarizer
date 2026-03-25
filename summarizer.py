import requests 

def count_words(text):
    return len(text.split())


def chunk_text(text, max_words=2000, overlap=200):
    words = text.split()  
    chunks = []   
    start = 0    
    
    while start < len(words):   
        end = start + max_words  
        chunk_words = words[start:end]  
        chunk_text = " ".join(chunk_words) 
        chunks.append(chunk_text) 
        start = end - overlap  
    
    return chunks




def summarize_chunk(chunk, style="concise"):
    style_prompts = {
        "concise": "Summarize this in 2-3 sentences:",
        "detailed": "Provide a detailed summary covering key points:",
        "bullet": "Summarize these key points as bullet points:",
        "executive": "Write an executive summary with main takeaways:"
    }
    
    prompt = f"""{style_prompts[style]}

Text:
{chunk}

Summary:"""
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1", 
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3, 
                "num_predict": 500   
            }
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        return result.get("response", "Error generating summary")
    else:
        return f"Error: {response.status_code} - Make sure Ollama is running"




def summarize_long_text(text, style="concise"):
    word_count = count_words(text)
    print(f"Total words: {word_count}")
    
    if word_count < 2000:
        return summarize_chunk(text, style)
    
    chunks = chunk_text(text)
    print(f"Split into {len(chunks)} chunks")
    
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarize_chunk(chunk, style)
        chunk_summaries.append(summary)
    
    combined_summaries = "\n\n".join(chunk_summaries)
    final_summary = summarize_chunk(combined_summaries, style)
    
    return final_summary






def summarize_with_focus(text, focus_area):
    prompt = f"""Summarize the following text, focusing specifically on {focus_area}.

Text:
{text}

Focus Area: {focus_area}

Summary focusing on {focus_area}:"""
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.3, "num_predict": 500}
        }
    )
    
    if response.status_code == 200:
        return response.json().get("response", "")
    return "Error"




def generate_tldr(text):
    prompt = f"Provide a one-sentence TL;DR for this text:\n\n{text}\n\nTL;DR:"
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.5, "num_predict": 100}
        }
    )
    
    if response.status_code == 200:
        return response.json().get("response", "")
    return "Error"