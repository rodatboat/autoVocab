import requests, json, base64, random
from bs4 import BeautifulSoup as soup


class Client:
    next_question_endpoint = "https://www.vocabulary.com/challenge/nextquestion.json"
    save_answer_endpoint = "https://www.vocabulary.com/challenge/saveanswer.json"
    start_endpoint = "https://www.vocabulary.com/challenge/start.json"

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0",
        "origin": "https://www.vocabulary.com",
        "x-requested-with": "XMLHttpRequest",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    r_secret = ""
    current_question = {}
    question_type = ""

    points = 0
    listId = 0

    def __init__(self, session_token, vocab_aws, guid):
        self.session_token = session_token
        self.session = requests.Session()
        self.session.cookies.set(
            "JSESSIONID", self.session_token, domain="www.vocabulary.com")
        
        self.session.cookies.set(
            "AWSALB", vocab_aws, domain="www.vocabulary.com")
        self.session.cookies.set(
            "guid", guid, domain="www.vocabulary.com")
        
        
    def start_from_list(self, listId):
        self.listId = listId
        payload = {
            "secret": self.r_secret,
            "v": 3,
            "activitytype": "p",  # c = challenge, p = practice
            "wordlistid": self.listId # wordlist
        }

        data = self.session.post(self.next_question_endpoint,
                          data=payload, headers=self.headers)
        
        self.r_secret = json.loads(data.text)["secret"]

        if float(json.loads(data.text)["game"]["progress"]) == 1.0:
            return -1
        
        self.question_type = json.loads(data.text)["question"]["type"]
        
        data_cookies = data.cookies.get_dict()
        self.session.cookies.set(
            "AWSALB", data_cookies["AWSALB"], domain="www.vocabulary.com")
        self.session.cookies.set(
            "AWSALBCORS", data_cookies["AWSALBCORS"], domain="www.vocabulary.com", secure=True)

        question_html = base64.b64decode(json.loads(data.text)["question"]["code"]).decode('utf-8')
        self.current_question = self.parseQuestion(question_html)
        

    def parseQuestion(self, htmlData):
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
        answers = [{"answer":a.text, "code":a["nonce"]} for a in answers]

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

        # print(self.question_type)
        # print(self.current_question)

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
            "rt": int(round(random.uniform(1, 6), 3) * 1000),
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
