import json, base64, random
from bs4 import BeautifulSoup as soup
from curl_cffi import requests


class Client:
    next_question_endpoint = "https://www.vocabulary.com/challenge/nextquestion.json"
    save_answer_endpoint = "https://www.vocabulary.com/challenge/saveanswer.json"
    start_endpoint = "https://www.vocabulary.com/challenge/start.json"

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0',
    'Origin': 'https://www.vocabulary.com',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '__cf_bm=nknMOlpgLxMNRpq0m7PpsljYOhAxMd8wo4hPMOWeuT4-1737804179-1.0.1.1-7rQ62hFn49EOGU6e0FL34kHSwRv.pdc5EDjnMZoMFA2h5caItc4_WWVf3ReumzZNkpHnskZk1QtqfbQkBkVVzw; _eu=0; autologin=1; cf_clearance=2EtlZh.920cJgguUigsYPVaIgjWgA05cmXkjR2rs47w-1737803137-1.2.1.1-SZ9m_OJzgnKWqHa5I8RGDJQKTVwBkngfTo.PYHma7RIeyMaUisHJYPM.niPbylwDMPOa46I.jFwuXEau3B0mXrc98HHX6UdS9QrdkMbkK3o.8xU7KzZkMFLHP8hS4jbxDixHRogXWe9SXbBS9_46jEiOTW9pCahhwTEPv.nxqyg2EIXVIeda8yLlhKZxjQUpiacLHJMQmeuR85Mz4qPQIDa1v6LwJ1DOdwV5LCWbJ_9QHrso.0tBt_hdDP2gFZJqlefxdf2BDgN8HqJAPSzdafu7BjR8JeXdywDEIL8ygLM; guid=9a897a5e2869a7aa4334ad4d7014a88f; AWSALB=PN8GEUyvUwwpH1C2anGPRdHHo2J9/LyIw76ZoArzgVtDFhKuSOVbSvxJDqVIllnQw2Nzw+1h9KvNIZT5LbxhQP3VEtZpax00vuonZQHuqRJswa07Twmfyxb1mG2I; AWSALBCORS=PN8GEUyvUwwpH1C2anGPRdHHo2J9/LyIw76ZoArzgVtDFhKuSOVbSvxJDqVIllnQw2Nzw+1h9KvNIZT5LbxhQP3VEtZpax00vuonZQHuqRJswa07Twmfyxb1mG2I; JSESSIONID=83A78EF7EC07B7475E7DAC0575792640; tz=America/Chicago'
    }


    r_secret = ""
    current_question = {}
    question_type = ""
    cookies = {}

    points = 0
    listId = 0

    def __init__(self):
        self.session = requests.Session()

        for cookie in self.headers['Cookie'].split('; '):
            key, value = cookie.split('=')
            self.cookies[key] = value
            
            self.session.cookies.set(
                key, value, domain="www.vocabulary.com")
        
        
    def start_from_list(self, listId):
        self.listId = listId
        payload = {
            "secret": self.r_secret,
            "v": 3,
            "activitytype": "p",  # c = challenge, p = practice
            "wordlistid": self.listId # wordlist
        }

        data = self.session.post(self.next_question_endpoint,
                          data=payload, headers=self.headers, cookies=self.cookies)
        
        self.r_secret = json.loads(data.text)["secret"]
        print(data.text)

        # if float(json.loads(data.text)["game"]["progress"]) == 1.0:
        #     return -1
        
        self.question_type = json.loads(data.text)["question"]["type"]
        
        data_cookies = data.cookies.get_dict()
        self.session.cookies.set(
            "AWSALB", data_cookies["AWSALB"], domain="www.vocabulary.com")
        self.session.cookies.set(
            "AWSALBCORS", data_cookies["AWSALBCORS"], domain="www.vocabulary.com", secure=True)

        question_html = base64.b64decode(json.loads(data.text)["question"]["code"]).decode('utf-8')
        self.current_question = self.parseQuestion(question_html)
        

    def parseQuestion(self, htmlData):
        print("Parsing question...")
        htmlData = soup(htmlData, 'html.parser')

        context = htmlData.find("div", {"class": "questionContent"})
        context = context.find_all("div", {"class": "sentence"}) if context != None else None
        if context != None:
            if len(context) > 0:
                if len(context) == 1:
                    context = context[0].text.strip().replace('\r', '').replace('\n', '').replace('\t', ' ')
                else:
                    context = context[1].find("strong").text.strip().replace('\r', '').replace('\n', '').replace('\t', ' ')

                    return {
                        "context":context,
                        "done":True
                    }

        question = htmlData.find("div", {"class": "instructions"}).text.strip().replace('\r', '').replace('\n', '').replace('\t', ' ')

        answers = htmlData.find("div", {"class": "choices"}).find_all("a")
        answers = [{"answer":a.text, "code":a["data-nonce"]} for a in answers]

        # if "choose the best picture" in question:
        #     return {
        #                 "context":answers[0],
        #                 "done":True
        #             }
        #     pass

        return {
            "context":context,
            "question":question,
            "answers":answers,
            "done":False
        }
    
    def formatQuestion(self):
        if self.current_question["done"]:
            return f'=+={self.current_question["context"]}'
        answers_string = ""
        for a in self.current_question["answers"]:
            answers_string += a["answer"]
            answers_string += "\n"

        if 1 == 0:
            return "=+="
        else:
            if self.current_question["context"] == None or not len(self.current_question["context"]) > 0:
                return f"{self.current_question['question']}\n(choose one of the following, only return the choice)\n{answers_string}"
            elif self.current_question["context"] != None:
                return f"'{self.current_question['context']}'\n{self.current_question['question']}\n(choose one of the following, only return the choice)\n{answers_string}"
            else:
                return f"{self.current_question['context']}\n(choose one of the following, only return the choice)\n{answers_string}"
    
    def answer_question(self, answer):
        if not self.current_question["done"]:
            for a in self.current_question["answers"]:
                if a["answer"].lower() == answer.lower():
                    answer = a["code"]
        payload = {
            "secret": self.r_secret,
            "v": 3,
            "rt": int(round(random.uniform(3, 7), 3) * 1000),
            "a": answer
        }

        data = self.session.post(self.save_answer_endpoint, data=payload, headers=self.headers)
        
        try:
            self.r_secret = json.loads(data.text)["secret"]
        except:
            print(data.text)

        data_cookies = data.cookies.get_dict()
        self.session.cookies.set(
            "AWSALB", data_cookies["AWSALB"], domain="www.vocabulary.com")
        self.session.cookies.set(
            "AWSALBCORS", data_cookies["AWSALBCORS"], domain="www.vocabulary.com", secure=True)

        answer_correct = json.loads(data.text)["answer"]["correct"]
        
        if not answer_correct:
            # print(data.question_type, answer)
            # print(self.current_question)
            # print(data.text)
            print("-")
            pass
        else:
            self.points += int(json.loads(data.text)["answer"]["points"])
            print(self.points)

    def next_question(self):
        payload = {
            "secret": self.r_secret,
            "v": 3,
        }

        data = self.session.post(self.next_question_endpoint, data=payload, headers=self.headers)

        self.r_secret = json.loads(data.text)["secret"]

        if float(json.loads(data.text)["game"]["progress"]) == 1.0:
            return -1
        else:
            self.question_type = json.loads(data.text)["question"]["type"]

            data_cookies = data.cookies.get_dict()
            self.session.cookies.set(
                "AWSALB", data_cookies["AWSALB"], domain="www.vocabulary.com")
            self.session.cookies.set(
                "AWSALBCORS", data_cookies["AWSALBCORS"], domain="www.vocabulary.com", secure=True)

            question_html = base64.b64decode(json.loads(data.text)["question"]["code"]).decode('utf-8')
            self.current_question = self.parseQuestion(question_html)

        # print(json.loads(data.text))
