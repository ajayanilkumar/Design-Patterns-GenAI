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