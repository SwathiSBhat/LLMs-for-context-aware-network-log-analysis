def create_tree_of_thought_prompts():
    prompts = [
        "What are the main types of messages in these logs (e.g., errors, warnings, info)?",
        "For each type of message, what are the key details provided?",
        "Are there any recurring patterns or repeated messages?",
        "What are the potential causes of the errors or warnings?",
        "Summarize the overall health and status of the system based on these logs."
    ]
    return prompts
