from openai import GPTAgent

if __name__ == "__main__":
    chatbot = GPTAgent()
    response = chatbot.ask_question("where did harrison work?")
    print(response)