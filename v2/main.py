import client, time, random, requests, sys


vocabClient = client.Client()

if __name__ == "__main__":
    
    # vocabClient.start_from_list(sat_lists[random.randint(0, len(sat_lists)-1)])
    # answer = vocabClient.askLLM()
    # vocabClient.answerQuestion(answer)
    
    total_sleep = 0
    sleep_limit = 7200 # 3600 = 1 hour, 7200 = 2 hours
    max_points = 300000
    started = False
    correct_answers = 0
    wrong_answers = 0
    
    while True and total_sleep < sleep_limit and vocabClient.total_points < max_points:
        print(f"Correct answers: {correct_answers} | Wrong answers: {wrong_answers} | Errors: {vocabClient.total_errors} | Points: {vocabClient.total_points} | Sleep time: {round(total_sleep, 0)}/{sleep_limit}", end="\r")
        if started:
            sleep_time = round(random.uniform(1, 5), 3)
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
        result = vocabClient.answerQuestion(answer)
        if result:
            correct_answers += 1
        else:
            wrong_answers += 1