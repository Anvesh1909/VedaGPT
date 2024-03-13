import replicate
import os

os.environ["REPLICATE_API_TOKEN"] = "r8_8qhUk5aWTLc2SiiBFWCvJwOIPXFWHcq1qFJas"

def H_replicate(prompt):
    final=""
    pre_prompt = "you are a helpful assistent. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    prompt_input = "Who is sundar pichai?"
    output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "prompt": f"{pre_prompt} {prompt_input} Assistent: ",
            "temperature": 0.1,"top_p":0.9,"max_length": 128,"repetition_penalty": 1
        }
    )
    for item in output:
    # https://replicate.com/meta/llama-2-70b-chat/api#output-schema
        final+=item
    return final

x=H_replicate("hello")
print(x)