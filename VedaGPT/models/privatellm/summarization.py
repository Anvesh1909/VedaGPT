from transformers import pipeline

def LLM(message):
    result = ""
    summarizer = pipeline(
        task="summarization",
        model="t5-small",
        min_length=20,
        max_length=128,  
        truncation=True,
        temperature= 0.1,top_p=0.9,repetition_penalty= 1,
        model_kwargs={"cache_dir": '/Documents/Huggin_Face/'},
       
    ) 
    output = summarizer(message, max_length=200, min_length=30, do_sample=False)
    summary = output[0]['summary_text']
    bullet_points = summary.split(". ")
    for point in bullet_points:
        result += f"{point}. "
    return result