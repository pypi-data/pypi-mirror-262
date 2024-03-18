import sys
import cmd
from .generate import chat
from mlx_lm import load

class MlxCLI(cmd.Cmd):
    prompt = ">>> "

    def __init__(self):
        super().__init__()
        self.model, self.tokenizer = load("mistralai/Mistral-7B-Instruct-v0.2")
        self.verbose = False
        self.messages = []
    
    def default(self, line):
        if line == "/verbose": 
            self.run_verbose()
        elif line == "/exit": 
            self.run_exit()
        else:
            self.messages.append({
                'role': 'user', 
                'content': line
            })

            response = chat(self.messages, self.model, self.tokenizer, self.verbose)

            self.messages.append({
                'role': 'assistant', 
                'content': response
            })
            print()
    
    def run_verbose(self):
        if self.verbose:
            self.verbose = False 
            print("Verbose output disabled!")
        else: 
            self.verbose = True
            print("Verbose output enabled!")
        

    def run_exit(self):
        return True

def main():
    if len(sys.argv) > 1:
        print(sys.argv)

    MlxCLI().cmdloop()