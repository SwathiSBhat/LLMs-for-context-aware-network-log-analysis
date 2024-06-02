import argparse
import json
import logging
import os
import uuid

import google.generativeai as genai
from dotenv import load_dotenv

from log_extractor.elk import ELKLogExtractor
from thought.tree_of_thought import create_tree_of_thought_prompts_prompts_suite_1

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the .env file
load_dotenv()

# Load the environment variable for the API key
api_key = os.environ.get("GOOGLE_API_KEY")

# Ensure the API key is set
if not api_key:
    raise ValueError("API key not found. Please set the 'GOOGLE_API_KEY' environment variable.")

# Initialize the generative AI client
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize the log extractor
log = ELKLogExtractor()


def get_recent_logs(time_range):
    logger.info("Getting logs for the last 5 minutes...")
    _log = log.get_logs(time_range=time_range)
    logger.info("Logs retrieved.")
    message = ELKLogExtractor.extract_message(json.loads(_log))
    paragraph = ELKLogExtractor.convert_to_paragraph(message)
    logger.info("Logs processed into paragraph.")
    return paragraph


def summarize_logs(logs, max_length=8000):
    total_length = 0
    summary = []
    for log in logs:
        log_length = len(log.split())
        if total_length + log_length <= max_length:
            summary.append(log)
            total_length += log_length
        else:
            break
    return summary


def write_to_file(unique_key, content, prefix="log"):
    filename = f"{prefix}_{unique_key}.txt"
    with open(filename, "w") as file:
        file.write(content)
    logger.info(f"{prefix.capitalize()} written to {filename}")


def main(time_range):
    # Generate a unique key for this session
    unique_key = str(uuid.uuid4())

    # Get and summarize logs
    logs = get_recent_logs(time_range)
    summarized_logs = summarize_logs(logs.split('\n'))

    # Write the original and summarized logs to files
    write_to_file(unique_key, logs, prefix="original_logs")
    write_to_file(unique_key, '\n'.join(summarized_logs), prefix="summarized_logs")

    # Prepare messages for the OpenAI API
    messages = [
        {"role": "system", "content": "Analyze the following logs:"},
        {"role": "user", "content": '\n'.join(logs)},
        {"role": "user", "content": '\n'.join(create_tree_of_thought_prompts_prompts_suite_1())}
    ]
    response = model.generate_content(str(messages))
    logger.info("Generated response from the model.")

    print(response)
    return unique_key


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--time-range', type=int, help='Time range of logs', required=True)
    print(main(time_range=parser.parse_args().time_range))
