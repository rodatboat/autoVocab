import time, random
import autoVocab
import config
from curl_cffi import requests

listId = config.listId

vocabClient = autoVocab.Client()
listStatus = True

total_sleep = 0

if vocabClient.start_from_list(listId) == -1:
    listStatus = False

while listStatus:
    if total_sleep >= 3600: # 3600 = 1 hour
        break
    try:
        message = vocabClient.formatQuestion()
        if not message.startswith("=+="):
            # for ai_answer in client.send_message("chinchilla", message, with_chat_break=True):
            #     pass
            # text_answer = ai_answer["text"].replace(".", "")
            text_answer = "1234"
        else:
            text_answer = message.replace("=+=","")

        sleep_time = round(random.uniform(0, 4), 3)
        print(f"Sleeping for {sleep_time}s")
        time.sleep(sleep_time)
        total_sleep += sleep_time

        vocabClient.answer_question(text_answer)
        finished = vocabClient.next_question()

        if finished == -1:
            break
    except Exception as e:
        print(e)
        vocabClient.start_from_list(listId)
        pass

print("List finished!")