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
https://urldefense.com/v3/__http://meet.google.com/iir-fafh-voc__;!!LSAcJDlP!2ZEznN50F07Yw8xI_E64xeI5eEAjyBSbXtXaZqRT2VGFJybzJT_td_WtYaymbafRjX-LO4GhtDG21ABBgGP7S-Q$
