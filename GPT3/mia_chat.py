import openai

"""
        Mia is Barry's personal chatbot

        What Mia Does:
            Answers questions with sarcastic responses
        """

class Mia:
    def __init__(self):
        # Set up the OpenAI API client
        openai.api_key = ""

        # Set up the model and prompt
        self.model_engine = ["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"]

        self.prompt = """
        Mia's characteristics are:
            Cute
            Sarcastic
            Funny
            Charming
        """

    def request_response(self, message):
        line = f"Barry: {message}\nMia:"
        self.prompt += "\n"+line

        # Generate a response
        completion = openai.Completion.create(
            engine=self.model_engine[0],
            prompt=self.prompt,
            max_tokens=256,
            n=1,
            stop=None,
            temperature=0.5,
        )

        response = completion.choices[0].text
        self.prompt += response

        print("=" * 20)
        print("Context:")
        print(self.prompt)
        print("=" * 20 + "\n\n")

        return response

    def request_response_simple(self, message):
        line = f"{message}\n"

        # Generate a response
        completion = openai.Completion.create(
            engine=self.model_engine[3],
            prompt=line,
            max_tokens=32,
            n=1,
            stop=None,
            temperature=0.5,
        )

        response = completion.choices[0].text
        return response

    def request_response_dummy(self, message):
        for i in range(2):
            message += " >>> " + message
        return message
