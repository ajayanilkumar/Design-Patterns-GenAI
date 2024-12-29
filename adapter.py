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