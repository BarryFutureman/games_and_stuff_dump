import openai

# Set up the OpenAI API client
openai.api_key = ""

# Set up the model and prompt
model_engine = ["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"]

prompt = """
Mia is Barry's personal chatbot
Never describe herself unless directly asked to

What Mia Does:
Answers questions with sarcastic responses
"""

while True:
    input_user = input()
    if input_user == "end":
        break
    line = f"Barry: {input_user}\nMia:"
    prompt += "\n"+line

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine[0],
        prompt=prompt,
        max_tokens=256,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    print(response)
    prompt += response

    print("="*20)
    print("Context:")
    print(prompt)
    print("=" * 20+"\n\n")