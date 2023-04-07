import requests, json, base64
from bs4 import BeautifulSoup as soup

session_secret = ""
session_token = ""

next_question_endpoint = "https://www.vocabulary.com/challenge/nextquestion.json"
save_answer_endpoint = "https://www.vocabulary.com/challenge/saveanswer.json"
start_endpoint = "https://www.vocabulary.com/challenge/start.json"

r = requests.session()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0",
    "origin": "https://www.vocabulary.com",
}

cookies = {
    "JSESSIONID": session_token,
}

payload = {
    # "secret": session_secret,
    "v": 4,
    "activitytype": "p", # c = challenge, p = practice
    "wordlistid": "1815780" # wordlist
}

data = r.post(next_question_endpoint, cookies=cookies, data=payload, headers=headers)
print(data)

question_html = base64.b64decode(json.loads(data.text)["question"]["code"]).decode('utf-8')
question_html = soup(question_html, 'html.parser')

context = question_html.find("div", {"class": "questionContent"}).find("div", {"class": "sentence"})
question = question_html.find("div", {"class": "instructions"}).text.strip()

answers = question_html.find("div", {"class": "choices"}).find_all("a")
answers = [{"answer":a.text, "code":a["nonce"]} for a in answers]

print({
            "context":context,
            "question":question,
            "answers":answers
        })