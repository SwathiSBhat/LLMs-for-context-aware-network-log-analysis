import os

import google.generativeai as genai
from dotenv import load_dotenv

from log_extractor.elk import ELKLogExtractor
from thought.tree_of_thought import create_tree_of_thought_prompts

# Load the .env file
load_dotenv()

# Load the environment variable for the API key
api_key = os.environ.get("GOOGLE_API_KEY")

# Ensure the API key is set
if not api_key:
    raise ValueError("API key not found. Please set the 'OPENAI_API_KEY' environment variable.")

# Initialize the OpenAI client
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize the log extractor
log = ELKLogExtractor()


def get_recent_logs():
    print("Getting logs for the last 5 minutes...")
    _log = log.get_logs_for_last_5_minutes()
    print("Logs retrieved.")
    print(_log)
    return _log


def main():
    response = model.generate_content(str([
        {"role": "system", "content": "Analyze the following logs:"},
        {"role": "user", "content": '\n'.join(get_recent_logs())},
        {"role": "user", "content": '\n'.join(create_tree_of_thought_prompts())}
    ]))
    print(response)


if __name__ == "__main__":
    main()
