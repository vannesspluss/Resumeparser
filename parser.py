import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

def ats_extractor(resume_data):
    prompt = '''
    You are an AI bot designed to act as a professional for parsing resumes. Extract the following info from the resume:
    1. full name
    2. email id
    3. github portfolio
    4. linkedin id
    5. employment details
    6. technical skills
    7. soft skills
    Provide the output ONLY in JSON format.
    '''

    openai_client = OpenAI(api_key=api_key)

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": resume_data}
    ]

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=1500
    )

    return response.choices[0].message.content