# Design Patterns for GenAI Applications

## Observer Pattern

The Observer Design Pattern is a behavioural pattern establishing a one-to-many dependency between objects. When the subject's state changes, it automatically notifies and updates its observers, enabling efficient interaction and communication among objects.

In an LLM application, the Observer Pattern can notify multiple observers of changes in the model's output. For example, when the LLM generates new output, observers like the UI update to display the response, the Logger records the interaction, and the Analytics system collects usage data, ensuring seamless decoupling between the LLM and its dependents.

```python
# Abstract Observer
class Observer:
    def update(self, llm_output):
        pass

# Concrete Observer: Logger
class Logger(Observer):
    def update(self, llm_output):
        print(f"Logger: Saving LLM output to logs: {llm_output}")

# Concrete Observer: UI Updater
class UIUpdater(Observer):
    def update(self, llm_output):
        print(f"UI: Displaying LLM output to the user: {llm_output}")

# Subject: LLM Output Generator
class LLMOutputNotifier:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify(self, llm_output):
        for observer in self.observers:
            observer.update(llm_output)

# Create the notifier (subject)
notifier = LLMOutputNotifier()

# Create observers
logger = Logger()
ui_updater = UIUpdater()

# Attach observers to the notifier
notifier.add_observer(logger)
notifier.add_observer(ui_updater)

# Simulate LLM generating an output and notify observers
llm_generated_output_1 = "The capital of France is Paris."
notifier.notify(llm_generated_output_1)

# Detach the logger observer
notifier.remove_observer(logger)

# Simulate LLM generating another output and notify observers
llm_generated_output_2 = "Python is a programming language known for its simplicity."
notifier.notify(llm_generated_output_2)
```


## Adapter Pattern

The adapter pattern helps two incompatible systems or classes work together by acting as a bridge. The adapter takes inputs from one system and converts them into a format the other system understands.

When we are working with multiple LLM API's and each one of them expect different input/output formats, this pattern can be used to standardize the way we call each model.

```python
# OpenAI Class
class OpenAIModel:
    def __init__(self, openai_model_name):
        self.openai_model_name = openai_model_name

    def query(self, prompt):
        return f"OpenAI response to: {prompt})"

# HuggingFace Class
class HuggingFaceModel:
    def __init__(self, model_name, quantization_method):
        self.model_name = model_name
        self.quantization_method = quantization_method

    def generate(self, prompt):
        return f"HuggingFace response to: {prompt})"

# Adapter
class ModelAdapter:
    def __init__(self, model, query_method):
        self.model = model
        self.query_method = query_method

    def query(self, text):
        return getattr(self.model, self.query_method)(text)

# Using the Adapter
openai_model = ModelAdapter(OpenAIModel(openai_model_name="gpt-4o"), "query")
huggingface_model = ModelAdapter(HuggingFaceModel(model_name="Mistral7b", quantization_method="bitsandbytes"), "generate")

# Standard interface usage
print(openai_model.query("What is Python?"))
print(huggingface_model.query("What is Python?"))

```

## Strategy Pattern

The Strategy Pattern is a behavioral design pattern that defines a family of algorithms or behaviors, encapsulates them in separate classes, and makes them interchangeable at runtime. It allows dynamic behavior changes without altering the class's code.

The Strategy Pattern in a RAG application can help in switching between different retrieval strategies dynamically, tailoring the retrieval process to user queries for flexible and adaptive responses.

```python
# Abstract Strategy
class RAGStrategy:
    def retrieve(self, query):
        pass

# Concrete Strategy: Naive RAG
class NaiveRAG(RAGStrategy):
    def retrieve(self, query):
        # Simulate naive retrieval
        return ["Document 1: Basics of Python.", "Document 2: OOP in Python."]

# Concrete Strategy: Advanced RAG
class AdvancedRAG(RAGStrategy):
    def retrieve(self, query):
        # Simulate advanced retrieval with filtering
        all_docs = [
            "Document 1: Basics of Python.",
            "Document 2: Advanced Python Design Patterns.",
            "Document 3: Strategy Pattern in Depth.",
        ]
        return [doc for doc in all_docs if "Design Patterns" in doc]

# Context Class: ChatBot
class ChatBot:
    def __init__(self, strategy: RAGStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: RAGStrategy):
        self.strategy = strategy

    def get_response(self, query):
        retrieved_docs = self.strategy.retrieve(query)
        return f"Generated response based on: {retrieved_docs}"


bot = ChatBot(NaiveRAG())

# Use NaiveRAG
print(bot.get_response("Explain Python design patterns."))

# Switch to AdvancedRAG
bot.set_strategy(AdvancedRAG())
print(bot.get_response("Explain Python design patterns."))

```

## Builder Pattern

The builder pattern is a creational pattern that helps create complex objects step by step. The construction process can change based on the type of product being built. This pattern separates the construction of a complex object from its representation, allowing the same construction process to create different representations.

We can use the builder pattern to construct complex prompts in our LLM applications. You can make use of this pattern for adding few-shot examples or more context while constructing your prompt.


```python
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

```
