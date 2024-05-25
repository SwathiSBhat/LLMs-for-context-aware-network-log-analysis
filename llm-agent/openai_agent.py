import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from log_extractor.elk import ELKLogExtractor
from thought.tree_of_thought import create_tree_of_thought_prompts

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


def get_recent_logs():
    print("Getting logs for the last 5 minutes...")
    _log = log.get_logs_for_last_5_minutes()
    print("Logs retrieved.")
    print(_log)
    # return _log
    return [
        "2024-05-24 10:00:00 INFO Starting system check",
        "2024-05-24 10:01:00 WARN Disk space running low on /dev/sda1",
        "2024-05-24 10:02:00 ERROR Unable to reach database server",
        "2024-05-24 10:03:00 INFO User admin logged in",
        "2024-05-24 10:04:00 DEBUG Config file reloaded successfully",
        "2024-05-24 10:05:00 INFO System check complete"
    ]


async def main():
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Analyze the following logs:"},
            {"role": "user", "content": '\n'.join(get_recent_logs())},
            {"role": "user", "content": '\n'.join(create_tree_of_thought_prompts())}
        ],
        stream=True,
    )
    async for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")


if __name__ == "__main__":
    asyncio.run(main())
