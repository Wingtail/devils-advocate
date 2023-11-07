from openai import OpenAI
from prompt_assistant import *

def init_context_memory(task_path="task.txt"):
    context_memory = {}
    context_memory["task"] = read_prompt_template(task_path)
    context_memory["memory"] = ""
    
    return context_memory

class Questioner:
    def __init__(self, api_key, model="gpt-4"):
        self.client = OpenAI(api_key=api_key)

        self.context_memory = init_context_memory()

        system_prompt = recursive_replace_tokens(read_prompt_template("questioner_prompt.txt"), self.context_memory)

        self.messages=[
            {"role": "system", "content": system_prompt},
        ]
        
        self.model = model
    
    def receive_persuasion(self, persuasion):
        self.messages.append({"role": "user", "content": persuasion})
    
    def make_summary(self):
        summary_prompt = read_prompt_template("summary_prompt.txt")
        self.messages.append({"role": "user", "content": summary_prompt})
    
    def provide_summary(self):
        summary_prompt = read_prompt_template("summary_prompt.txt")
        self.messages.append({"role": "user", "content": summary_prompt})

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=0.0,
            messages=self.messages
        )
        
        print("Questioner memory: ", completion.choices[0].message.content)
        
        self.context_memory["memory"] = completion.choices[0].message.content
    
    def provide_response(self):
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=self.messages
        )
        
        self.messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        
        print("Questioner: ", completion.choices[0].message.content)
        
        return completion.choices[0].message.content, "AGREE" in completion.choices[0].message.content

class Persuader:
    def __init__(self, api_key, model="gpt-4"):
        self.client = OpenAI(api_key=api_key)

        self.model = model
        self.context_memory = init_context_memory()

        system_prompt = recursive_replace_tokens(read_prompt_template("persuader_prompt.txt"), self.context_memory)

        self.messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": ""},
        ]
    
    def receive_questions(self, question):
        self.messages.append({"role": "user", "content": question})

    def provide_final_answer(self):
        final_answer_prompt = read_prompt_template("final_answer_prompt.txt")
        self.messages.append({"role": "user", "content": final_answer_prompt})
        
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=0.0,
            messages=self.messages
        )
        
        self.messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        
        print("Persuader Final Answer: ", completion.choices[0].message.content)
        
        return completion.choices[0].message.content, "AGREE" in completion.choices[0].message.content

    def provide_summary(self):
        summary_prompt = read_prompt_template("summary_prompt.txt")
        self.messages.append({"role": "user", "content": summary_prompt})
        
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=0.0,
            messages=self.messages
        )
        
        print("Persuader memory: ", completion.choices[0].message.content)
        
        self.context_memory["memory"] = completion.choices[0].message.content

    def provide_response(self):
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=0.4,
            messages=self.messages
        )
        
        self.messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        
        print("Persuader: ", completion.choices[0].message.content)
        
        return completion.choices[0].message.content, "AGREE" in completion.choices[0].message.content

if __name__ == "__main__":
    questioner = Questioner("<YOUR_OPENAI_API_KEY>")
    persuader = Persuader("<YOUR_OPENAI_API_KEY>")

    response, is_agree = persuader.provide_response()

    while True:
        questioner.receive_persuasion(response)
        response, is_agree = questioner.provide_response()
        
        if is_agree:
            break

        persuader.receive_questions(response)
        response, is_agree = persuader.provide_response()
    
    persuader.provide_final_answer()
    
    questioner.provide_summary()
    persuader.provide_summary()
