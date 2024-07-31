import queue
import threading
import time
import requests
import sys
import random

#Making request_queue global var so that threads can update it
#request_queue = queue.Queue()

'''
This class will handle hitting apis that have a rate limit of x requests every y seconds
'''

class RateLimitApiRequestorArbitary:
    #Making last_request_time so that it doesnt get overwritten by another app calling this class
    #Ideally these maximum_requests and interval_seconds should come from a global file so we do not overwrite this from other instances of the methods
    #But for the purpose of the exercise, will allow the constructor set these values 
    request_queue = queue.Queue()
    last_request_time = time.time()
    keep_alive = True
    #maximum_requests = MAXIMUM_REQUEST
    #interval_seconds = INTERVAL_SECONDS
    def __init__(self, maximum_requests, interval_seconds):
        self.maximum_requests = maximum_requests
        self.interval_seconds = interval_seconds
        self.last_request_time = RateLimitApiRequestorArbitary.last_request_time
        self.request_queue = RateLimitApiRequestorArbitary.request_queue
        self.keep_alive = RateLimitApiRequestorArbitary.keep_alive


    '''
    This function will queue an incoming request
    '''
    def queue_request(self, request):
        self.request_queue.put(request)
        print(f"Added queue size: {self.request_queue.qsize()}, contents: {list(self.request_queue.queue)}")       

    def process_request(self):
        current_request_made = 0
        initial_request_time = time.time()
        while self.keep_alive:
            if not self.request_queue.empty():
                url = self.request_queue.get()
                if url == 'EXIT':
                    print(f"EXITING PROGRAM TY!")
                    self.keep_alive = False
                    #Terminate thread here
                    sys.exit()
                if (current_request_made <= self.maximum_requests):
                    time_since_intitial_request = self.last_request_time - initial_request_time
                    #ensuring that if current_request_made + 1 is met or time taken is less than interval than we wait correct amount of time till next interval
                    #or if time_since_intitial_request is greater than interval meaning that there are too many request in a span
                    if (((time_since_intitial_request < self.interval_seconds and (current_request_made + 1)) > self.maximum_requests) or (time_since_intitial_request > self.interval_seconds)):
                        time_sleep =  (time_since_intitial_request) - self.interval_seconds
                        #to ensure that if time sleep < 0, we still sleep the correct amount depending on which condiditn above is met
                        if (time_sleep < 0):
                            time_sleep = time_sleep * -1
                        print(f"Sleep: {time_sleep} and Request made: {current_request_made}")
                        time.sleep(time_sleep)
                        current_request_made = 0
                        initial_request_time = time.time()
                    # Now execute the request and can hit post or get request 
                    response = self.make_request_with_retries(url) 
                    #print(f"Removed queue size: {self.request_queue.qsize()} with reponse {response.status_code}")
                    print(f"Request to {url} completed with status code {response.status_code} with time {self.last_request_time} and time since initial time {time_since_intitial_request}")
                    #update current request made to keep track of request availble to be made
                    current_request_made += 1
                    #updating last_request_time to current time
                    self.last_request_time = time.time()
                #updating current time
    
    def make_request_with_retries(self,url,tries=5):
        for i in range(tries):
            try:
                return requests.get(url) 
            except KeyError as e:
                if i < tries- 1: # i is zero indexed
                    continue
                else:
                    raise
            break

'''Create request to queue at random times'''
def arbitary_requests(api, urls, total_request=5):
    for i in range(total_request):
        time.sleep(random.uniform(0.0, 3))  # Sleep for a random time between 0.0 and 3 seconds
        api.queue_request(urls)

if __name__ == "__main__":
    endpoint = "https://www.example.com"
    rate_limited_api_requestor = RateLimitApiRequestorArbitary(maximum_requests=5, interval_seconds=10)

    #added arbitary request #1
    request_thread = threading.Thread(target=arbitary_requests,args=(rate_limited_api_requestor, endpoint, 10))
    request_thread.start()

    process_thread = threading.Thread(target=rate_limited_api_requestor.process_request)
    process_thread.start()

    #added arbitary request #2
    request_thread2 = threading.Thread(target=arbitary_requests,args=(rate_limited_api_requestor, endpoint, 10))
    request_thread2.start()
    # Wait for the request thread to finish
    request_thread.join()
    request_thread2.join()
    
    #adding dummy value to exit out of request thread
    rate_limited_api_requestor.request_queue.put('EXIT') 
    process_thread.join()
