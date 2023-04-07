import poe, time, random
import autoVocab
import config

poe_session_token = config.poe_session_token
vocab_session_token = config.vocab_session_token
vocab_aws = config.vocab_aws
guid = config.guid
listId = config.listId

client = poe.Client(f"{poe_session_token}")
vocabClient = autoVocab.Client(vocab_session_token, vocab_aws, guid)
listStatus = True

if vocabClient.start_from_list(listId) == -1:
    listStatus = False

while listStatus:
    try:
        message = vocabClient.formatQuestion()
        if not message.startswith("=+="):
            for ai_answer in client.send_message("chinchilla", message, with_chat_break=True):
                pass
            text_answer = ai_answer["text"].replace(".", "")
        else:
            text_answer = message.replace("=+=","")

        sleep_time = round(random.uniform(0, 4), 3)
        print(f"Sleeping for {sleep_time}s")
        time.sleep(sleep_time)

        vocabClient.answer_question(text_answer)
        finished = vocabClient.next_question()

        if finished == -1:
            break
    except Exception as e:
        print(e)
        vocabClient.start_from_list(listId)
        pass

print("List finished!")