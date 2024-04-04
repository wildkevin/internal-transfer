load_dotenv()

MARKETS = "SG"
ifCompare = False
FIELD = "srr"
prompt_dict: dict = {}
COMPANIES = get_company_list(MARKETS)
url = os.getenv("ASK_URL")
# url = "http://localhost:8000/wsit-innovation-generativeAI-pa-chatgpt/v2/ask-question"
headers = {
    'Content-Type': 'application/json',
    'Cookie': os.getenv("ASK_COOKIE")
}

df = pd.DataFrame(columns=['company', 'stitt_output', 'api_return', 'response_time'])
https://urldefense.com/v3/__https://9hdppg0c.r.ap-southeast-2.awstrack.me/L0/https:*2F*2Fdocs.google.com*2Fdocument*2Fd*2Fe*2F2PACX-1vQ0yDBnu3pX60DW9yTftomGI_bvU4cLbF5bOnkM7LcD1thwlC14t5WHs58h80Gji6kbvpYjTV6oTGSp*2Fpub/1/0108018ea3c9ba05-cd46237d-9274-4fcf-ad37-5d2916522448-000000/4liNcBAcsR63fu6He21NOkazUgY=149__;JSUlJSUlJQ!!LSAcJDlP!3FmkF7K0RzO-IdxmwUDq2ZIMZe7hFQQEW0pW7vk_7fB5YjuxtI4C1RUPZ9Yq1K8Ob6x4kqsKXYMhf--q8faew_x8TMIr9BJtOjF6YsQ$
