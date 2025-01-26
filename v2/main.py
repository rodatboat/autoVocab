import client, time, random, requests


vocabClient = client.Client()

if __name__ == "__main__":
    
    vocabClient.start_from_list(149644)
    answer = vocabClient.askLLM()
    vocabClient.answerQuestion(answer)
    
    listCompleted = False
    while not listCompleted and not vocabClient.error:
        status = vocabClient.next_question()
        if status == -1:
            listCompleted = True
            break
        answer = vocabClient.askLLM()
        print(answer)
        vocabClient.answerQuestion(answer)
        
        sleep_time = round(random.uniform(2, 6), 3)
        print(f"Sleeping for {sleep_time}s")
        time.sleep(sleep_time)