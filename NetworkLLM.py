import torch
import transformers
import numpy as np

#from openai import OpenAI

#client = OpenAI()

class NetworkLLM:
    def __init__(self, historical_logs, chunk_size, embedding_model, LLM_type = "Hugging_Face", 
                 LLM_name = "unsloth/llama-3-8b-Instruct-bnb-4bit"):
        
        self.logs = self.process_logs(historical_logs, chunk_size)
        self.embedding_model = embedding_model
        self.embeddings = self.embed_logs(self.logs)
        self.LLM_type = LLM_type
        self.LLM_name = LLM_name
        

    #Functions for querying historical logs
    def process_logs(self, logs, chunk_size):
        #TODO: Need to see the logs in order to know how to process

        #Will probably involve aggregating and chunking the logs

        return "placeholder"

    def embed_logs(self, logs):
        #TODO: Create vector embeddings of processed logs

        #Either use pretrained model, if one exists that would work for this, or train one ourselves

        return "placeholder"

    def query_logs(self, query, num_logs_returned):
        #TODO: Use similarity search between query and log embeddings to retrieve relevant logs

        #Embed query

        #Compute dot product (or cosine similarity) between query and log embeddings

        #Sort, and return logs with highest similarity

        return "placeholder"
    
    
    
    #Example prompt generation
    def prompt_generation(self, current_logs, task):
        
        query = self.embed_logs(current_logs)
        relevant_logs = self.query_logs(query, num_logs_returned=5)

        network_details = "some string description/representation of network, maybe should be passed in as arg to the class."
        
        #An example task
        if(task == "Attack Detection"):
            
            prompt = ("Your task is to determine if an attack is occuring in a network. The network is " + network_details + 
                      "Here are the current logs " + current_logs + " and here are some relevant historical logs" + 
                      relevant_logs)
            
            return prompt

        elif(task == "Something Else"):
            return "placeholder"

        else:
            return "placeholder"
        
    
    #Main function called by user of class to query LLM
    def ask(self, current_logs, task="Attack Detection"):
        
        user_prompt = self.prompt_generation(current_logs, task)
        
        #May need changes
        messages = [
            {"role": "system", "content": "You are a network expert who can assist with any network issue"},
            {"role": "user", "content": user_prompt},
        ]
        
        if(self.LLM_type == "Hugging_Face"):
            model_id = self.LLM_name

            pipeline = transformers.pipeline(
                "text-generation",
                model=model_id,
                #model_kwargs={"torch_dtype": torch.bfloat16},
                device_map="auto",
            )

            prompt = pipeline.tokenizer.apply_chat_template(
                    messages, 
                    tokenize=False, 
                    add_generation_prompt=True
            )

            terminators = [
                pipeline.tokenizer.eos_token_id,
                pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]

            outputs = pipeline(
                prompt,
                max_new_tokens=256,
                eos_token_id=terminators,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
            )
            return outputs[0]["generated_text"][len(prompt):]
                   
        elif(self.LLM_type == "OpenAI"):
            completion = client.chat.completions.create(
              model="gpt-4-turbo",
              messages=messages
            )

            return completion.choices[0].message



#Test that this will succesfully run. No good output for now without any logs to test.
test = NetworkLLM(0, 0, 0)
print(test.ask('test'))

