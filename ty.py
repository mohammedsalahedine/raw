import streamlit as st
import pandas as pd
import openai

# Initialize the OpenAI client using st.secrets
client = openai.OpenAI(
    api_key= st.secrets['openai']["OPENAI_API_KEY"],
   # organization=st.secrets["openai"]["organization"]
)

def generate_AMDEC_info(element, detection, severity, occurrence, failure_mode=None):
    prompt = f"""
    ... Your task is to answer in a consistent style.
    ...
    you are a hse engenering working in rafinry manufacter ,which include these element {element}

    Failure Mode, Function ,Effects, Causes, Detection, Severity, Occurrence, Detection,
    Element: {element}
    Function:
    Failure Mode: {failure_mode}
    Effects:
    Causes:
    Detection : {detection}
    Severity: {severity}
    Occurrence: {occurrence}
    RPN:
    Recommendations :

    #and by /n i mean new line

    """
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo",
    )
    response = chat_completion.choices[0].message.content

    # Parse response to extract AMDEC-related information
    lines = response.split('\n')
    data = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()

    # Convert dictionary to DataFrame
    amdec_data = pd.DataFrame([data])
    return amdec_data

# Streamlit application code continues...
