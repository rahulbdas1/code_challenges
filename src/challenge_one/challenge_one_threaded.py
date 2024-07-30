import queue
import threading
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


'''
This class will handle hitting apis that have a rate limit of x requests every y seconds
'''
class ThreadedRateLimitApiRequestor:
    #Making last_request_time so that it doesnt get overwritten by another app calling this class
    last_request_time = time.time()
    request_queue = queue.Queue()
    #making the current_request_made static var in the class bc we want to multithread so we need to keep track current_request_made for all the conurrent threads in th class
    current_request_made = 0
    #making the initial_request_time static var in the class bc we want to multithread so we need to keep track current_request_made for all the conurrent threads in th class
    initial_request_time = time.time()

    #Ideally these maximum_requests and interval_seconds should come from a global file so we do not overwrite this from other instances of the methods
    #But for the purpose of the exercise, will allow the constructor set these values 
    #maximum_requests = MAXIMUM_REQUEST
    #interval_seconds = INTERVAL_SECONDS
    def __init__(self, maximum_requests, interval_seconds):
        self.maximum_requests = maximum_requests
        self.interval_seconds = interval_seconds
        self.lock = threading.Lock()
        self.request_queue = ThreadedRateLimitApiRequestor.request_queue
        self.last_request_time = ThreadedRateLimitApiRequestor.last_request_time
        self.current_request_made = ThreadedRateLimitApiRequestor.current_request_made
        self.initial_request_time = ThreadedRateLimitApiRequestor.initial_request_time
        
    '''
    This function will queue an incoming request
    '''
    def queue_request(self, request):
        self.request_queue.put(request)

    '''
    This Function takes care of making a request by considering last_request_time and current_request_made to ensure we do not go over the rate limit
    '''
    def process_request(self):
        current_time = time.time()
        time_since_last_request = 0
        while True:
            thread_name = threading.current_thread().name
            with self.lock:
                if not self.request_queue.empty():
                    url = self.request_queue.get()
                    if (self.current_request_made <= self.maximum_requests):
                        time_since_intitial_request = self.last_request_time - self.initial_request_time
                        #ensuring that if current_request_made + 1 is met or time taken is less than interval than we wait correct amount of time till next interval
                        #or if time_since_intitial_request is greater than interval meaning that there are too many request in a span
                        if ((time_since_intitial_request < self.interval_seconds and (self.current_request_made + 1) > self.maximum_requests) or (time_since_intitial_request > self.interval_seconds)):
                            time_sleep =  self.interval_seconds - (time_since_intitial_request) 
                            #to ensure that if time sleep < 0, we still sleep the correct amount depending on which condiditn above is met
                            if (time_sleep < 0):
                                time_sleep = time_sleep * -1
                            print(f"Sleep: {time_sleep} and Request made: {self.current_request_made}")
                            time.sleep(time_sleep)
                            self.current_request_made = 0
                            self.initial_request_time = time.time()
                        # Now execute the request and can hit post or get request 
                        response = self.make_request_with_retries(url) 
                        print(f"Request to {url} completed with status code {response.status_code} with time {self.last_request_time} and thread: {thread_name} and time since initial time {time_since_intitial_request}")
                        #update current request made to keep track of request availble to be made
                        self.current_request_made += 1
                        #updating last_request_time to current time
                        self.last_request_time = time.time()
                    #updating current timr
                    current_time = time.time()
                    self.request_queue.task_done()
                else: 
                    break

    def start(self, thread_count = 5):
        for _ in range(thread_count):
            thread = threading.Thread(target=self.process_request)
            thread.daemon = True  # Threads will exit when main program exits
            thread.start()
               
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

if __name__ == "__main__":
    rate_limited_api_requestor = ThreadedRateLimitApiRequestor(maximum_requests=51, interval_seconds=1)
    
    #Enqueue some requests
    #ideally this url will be put in a global config and we would have an independent APIrequestor for each url with its relevant
    #max request and interval...
    end_point = "https://www.example.com"
    queue_count = 52

    for i in range(queue_count):
        rate_limited_api_requestor.queue_request(end_point)

    # Start processing the requests
    rate_limited_api_requestor.start(10)

    rate_limited_api_requestor.request_queue.join()