# Query Class
class Query:
    def __init__(self, prompt, temperature, max_tokens):
        self.prompt = prompt
        self.temperature = temperature
        self.max_tokens = max_tokens

    def __repr__(self):
        return f"Query(prompt={self.prompt!r}, temperature={self.temperature}, max_tokens={self.max_tokens})"

# Builder
class QueryBuilder:
    def __init__(self):
        self.prompt = ""
        self.temperature = 1.0
        self.max_tokens = 100
        self.examples = []  

    def set_prompt(self, prompt):
        self.prompt = prompt
        return self

    def set_temperature(self, temperature):
        self.temperature = temperature
        return self

    def set_max_tokens(self, max_tokens):
        self.max_tokens = max_tokens
        return self

    def add_example(self, example_input, example_output):
        self.examples.append({"input": example_input, "output": example_output})
        return self

    def build(self):
        """Construct and return the Query object."""
        if self.examples:
            # Combine few-shot examples into the prompt
            example_str = "\n\n".join(
                f"Input: {ex['input']}\nOutput: {ex['output']}" for ex in self.examples
            )
            full_prompt = f"{example_str}\n\nInput: {self.prompt}\nOutput:"
        else:
            # For no-shot prompt
            full_prompt = self.prompt

        # Return the fully built Query object
        return Query(full_prompt, self.temperature, self.max_tokens)

# Few-shot prompting
few_shot_query = (
    QueryBuilder()
    .add_example("What is Python?", "Python is a programming language.")
    .add_example("What is Java?", "Java is a programming language.")
    .set_prompt("What is C++?")
    .set_temperature(0.7)
    .set_max_tokens(50)
    .build()
)


# No-shot prompting
no_shot_query = (
    QueryBuilder()
    .set_prompt("What is the capital of France?")
    .set_max_tokens(20)
    .build()
)

print("Few-shot Query:", few_shot_query)
print("No-shot Query:", no_shot_query)