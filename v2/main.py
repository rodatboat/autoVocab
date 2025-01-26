import client, time, random, requests


vocabClient = client.Client()

sat_lists = [148703, 151274, 148713, 148732, 148845, 149637, 149640, 149642, 149643, 151263, 151274, 151399, 151404, 151465, 151466, 156619, 156622, 158007, 158769, 158781, 158782, 161539]

if __name__ == "__main__":
    
    # vocabClient.start_from_list(sat_lists[random.randint(0, len(sat_lists)-1)])
    # answer = vocabClient.askLLM()
    # vocabClient.answerQuestion(answer)
    
    total_sleep = 0
    sleep_limit = 7200 # 3600 = 1 hour, 7200 = 2 hours
    max_points = 300000
    started = False
    while True and total_sleep < sleep_limit and vocabClient.total_points < max_points:
        if started:
            sleep_time = round(random.uniform(1, 5), 3)
            print(f"Sleeping for {sleep_time}s")
            time.sleep(sleep_time)
            total_sleep += sleep_time
        started = True
        
        fail_counter = 0
        fetch_success = vocabClient.fetched_question_success()
        if not fetch_success:
            if(fail_counter > 5):
                print("Failed to fetch question 5 times. Exiting...")
                exit()
            
            print("Failed to fetch question. Retrying...")
            fail_counter += 1
            time.sleep(5)
            fetch_success = vocabClient.fetched_question_success()
        
        answer = vocabClient.askLLM()
        print(answer)
        vocabClient.answerQuestion(answer)