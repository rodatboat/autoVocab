import client, time, random, requests


vocabClient = client.Client()

sat_lists = [148703, 151274, 148713, 148732, 148845, 149637, 149640, 149642, 149643, 151263, 151274, 151399, 151404, 151465, 151466, 156619, 156622, 158007, 158769, 158781, 158782, 161539]

if __name__ == "__main__":
    
    # vocabClient.start_from_list(151263)
    # answer = vocabClient.askLLM()
    # vocabClient.answerQuestion(answer)
    
    listCompleted = False
    while not listCompleted and not vocabClient.error:
        status = vocabClient.next_question()
        if status == -1:
            listCompleted = True
            break
        answer = vocabClient.askLLM()
        print(answer)
        vocabClient.answerQuestion(answer)
        
        sleep_time = round(random.uniform(5, 10), 3)
        print(f"Sleeping for {sleep_time}s")
        time.sleep(sleep_time)