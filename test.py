import openai

openai.api_key = "sk-YoHbhlK3USBd6fG0586413B3E6A84100B9C527A9201f34E8"
openai.base_url = "http://localhost/v1/"
response = openai.ChatCompletion.create(
    model="DeepSeek-R1",  # DeepSeekV3
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "hello"}
    ],
    temperature=0.7,
)

print(response.choices[0].message.content)
