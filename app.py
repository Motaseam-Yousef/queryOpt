import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI # Corrected the import statement for the OpenAI library

# Load environment variables from .env file
load_dotenv()

def generate_gpt_response(query_language, query):
    try:
        openai_api = os.getenv('OPENAI_API')
        openai_client = OpenAI(api_key=openai_api)
        MODEL = 'gpt-4o'

        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": '''You are a query optimizer. I will give you a query using {query_language} and the used query {query}. You will provide me with the optimal version of this query. Just give me the query without any explanation or anything else. If the input from the user is not a query, just return "I am here to optimize queries only."'''},
                {"role": "user", "content": f'''query language: {query_language}\nThe query: {query}'''}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content # Corrected the way to access the response content
    except Exception as e:
        st.error("Failed to generate GPT response: {}".format(e))
        return None

def main():
    st.title("Query Optimizer")
    
    query_language = st.text_input("Enter query language:")
    query = st.text_area("Enter your query:")
    
    if st.button("Optimize Query"):
        response = generate_gpt_response(query_language, query)
        if response:
            st.text_area("Optimized Query:", value=response, height=200)

if __name__ == "__main__":
    main()

