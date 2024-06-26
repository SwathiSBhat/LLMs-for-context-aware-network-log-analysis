import argparse
import asyncio
import json
import logging
import os
import uuid

from dotenv import load_dotenv
from openai import AsyncOpenAI

from log_extractor.elk import ELKLogExtractor
from thought.tree_of_thought import create_tree_of_thought_prompts_suite_1

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the .env file
load_dotenv()

# Load the environment variable for the API key
api_key = os.environ.get("OPENAI_API_KEY")

# Ensure the API key is set
if not api_key:
    raise ValueError("API key not found. Please set the 'OPENAI_API_KEY' environment variable.")

# Initialize the OpenAI client
client = AsyncOpenAI(api_key=api_key)

# Initialize the log extractor
log = ELKLogExtractor()


def get_recent_logs(time_range):
    _log = log.get_logs(time_range=time_range)
    logger.info("Logs retrieved.")
    message = ELKLogExtractor.extract_message(json.loads(_log))
    paragraph = ELKLogExtractor.convert_to_paragraph(message)
    logger.info("Logs processed into paragraph.")
    print(paragraph)
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


async def main(time_range):
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
        {"role": "user", "content": '\n'.join(summarized_logs)},
        {"role": "user", "content": '\n'.join(create_tree_of_thought_prompts_suite_1())}
    ]

    # Process the response from the OpenAI API
    response_content = []
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        stream=True,
    )
    async for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        print(content, end="")  # TODO: Remove this line get logged
        response_content.append(content)

    # Write the prompt output to a file
    write_to_file(unique_key, ''.join(response_content), prefix="prompt_output")
    return "\n" + unique_key


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--time-range', type=int, help='Time range of logs', required=True)
    print(asyncio.run(main(time_range=parser.parse_args().time_range)))
