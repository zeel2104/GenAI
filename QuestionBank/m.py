import openai
api_key = ''

# Set your OpenAI API key here
from openai import OpenAI
client = OpenAI(api_key=api_key)

# Function to generate questions with answers, difficulty, and options using OpenAI API
def generate_questions(prompt):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
    {"role": "system", "content": "You are a helpful assistant designed to answer users question based on the documents provided."},
    {"role": "user", "content": ""+prompt+""}
  ]
)
    return response.choices[0].message.content
