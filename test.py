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
https://urldefense.com/v3/__https://9hdppg0c.r.ap-southeast-2.awstrack.me/L0/https:*2F*2Fdocs.google.com*2Fdocument*2Fd*2Fe*2F2PACX-1vTUHOdQy85pAXjTUGmDH4ae1YOatN-Mx_4mBx8zkkJbH8EvDpingnwwgu7wR9H_NKAWu_DjJKEwsdZq*2Fpub/1/0108018ec6f722d1-564aa71d-23a1-47ca-80c8-fe7f5eb0dd45-000000/VbdjsiUfqx58GhoPrDSjTTMFlkY=149__;JSUlJSUlJQ!!LSAcJDlP!26NMlSJChhrRCU97KGpovRRrXY5pIM8LT-e8yrDVTcM1b8lvM9ElTJFpiUcN9s-AumBDidxWKJE8x3qOsKYNatNdh9gvoppPl_fNxiY$
