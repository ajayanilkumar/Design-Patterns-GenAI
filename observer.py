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