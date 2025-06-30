import openai

# Set up the OpenAI API client
openai.api_key = ""

# Set up the model and prompt
model_engine = ["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"]


while True:
    prompt = f"{input()}"
    if prompt == "end":
        break
    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine[0],
        prompt=prompt,
        max_tokens=64,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices
    for i in range(len(response)):
        print(f">> {i} {response[i].text}")
    print("="*20)
    print()