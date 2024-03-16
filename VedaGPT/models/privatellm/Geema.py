
import replicate
import os

# Set the Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "r8_UlQcSfz5ttfznmTwiH3R2B0gztZAzxv1fJOHb"

def reply(prompt):
    """
    Generate a reply using the Replicate API based on a given prompt.

    Args:
    - prompt (str): The user's input prompt.

    Returns:
    - str: The generated reply.
    """
    final = "This is Geema Reply:: <br>"
    pre_prompt = "you are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    prompt_input = prompt
    output = replicate.run(
        "google-deepmind/gemma-7b-it:2790a695e5dcae15506138cc4718d1106d0d475e6dca4b1d43f42414647993d5",
        input={
           "prompt": f'''
                        
                        [INST] <<SYS>>
                            you are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.
                            ,You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
                            ,If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
                                <</SYS>>

                            Question: {prompt}
                        [/INST]
                    
                    ''',
            "temperature": 0.1,
            "max_new_tokens": 512,
            "min_new_tokens": -1,
            "repetition_penalty": 1
        }
    )
    for item in output:
        # Output schema: https://replicate.com/meta/llama-2-70b-chat/api#output-schema
        final += item
    return final


def replyPdf(prompt, context):
    """
    Generate a reply using the Replicate API based on a given prompt and context.

    Args:
    - prompt (str): The user's input prompt.
    - context (str): The context provided for the question.

    Returns:
    - str: The generated reply.
    """
    final = "This is Geema Reply:: <br>-"
   
    output = replicate.run(
        "google-deepmind/gemma-7b-it:2790a695e5dcae15506138cc4718d1106d0d475e6dca4b1d43f42414647993d5",
        input={
            "prompt": f'''
                        [INST]
                        Give an answer for the question strictly based on the context provided.
                        you are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.
                        You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
                        If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
                        Question: {prompt}

                        Context : {context}
                        [/INST]
                    ''',
            "temperature": 0.7,
            "max_new_tokens": 512,
            "min_new_tokens": -1,
            "repetition_penalty": 1
        }
    )
    for item in output:
        # Output schema: https://replicate.com/meta/llama-2-70b-chat/api#output-schema
        final += item
    return final
