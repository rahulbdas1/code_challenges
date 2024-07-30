import queue
import threading
import time
import requests
import sys
import asyncio
from concurrent.futures import ProcessPoolExecutor

'''
This class will handle hitting apis that have a rate limit of x requests every y seconds
'''
class RateLimitApiRequestorArbitary:
    #Making last_request_time so that it doesnt get overwritten by another app calling this class
    last_request_time = time.time()
    request_queue = queue.Queue()
    #Ideally these maximum_requests and interval_seconds should come from a global file so we do not overwrite this from other instances of the methods
    #But for the purpose of the exercise, will allow the constructor set these values 
    #maximum_requests = MAXIMUM_REQUEST
    #interval_seconds = INTERVAL_SECONDS
    def __init__(self, maximum_requests, interval_seconds):
        self.maximum_requests = maximum_requests
        self.interval_seconds = interval_seconds
        self.request_queue = RateLimitApiRequestorArbitary.request_queue
        self.last_request_time = RateLimitApiRequestorArbitary.last_request_time
        
    '''
    This function will queue an incoming request
    '''
    def queue_request(self, request):
        self.request_queue.put(request)
        print(f"Added queue size: {self.request_queue.qsize()}")

    '''
    This Function takes care of making a request by considering last_request_time and current_request_made to ensure we do not go over the rate limit
    '''
    async def queue_all_request(self,end_point,queue_count):
        for i in range(queue_count):
            rate_limited_api_requestor.queue_request(end_point)
            #asynch adding to queue
            await asyncio.sleep(0)           


    async def process_request(self):
        current_request_made = 0
        initial_request_time = time.time()
        while True:
            #asynch removing to queue
            await asyncio.sleep(0)           
            if not self.request_queue.empty():
                url = self.request_queue.get()
                print(f"Removed queue size: {self.request_queue.qsize()}")
                if (current_request_made <= self.maximum_requests):
                    time_since_intitial_request = self.last_request_time - initial_request_time
                    #ensuring that if current_request_made + 1 is met or time taken is less than interval than we wait correct amount of time till next interval
                    #or if time_since_intitial_request is greater than interval meaning that there are too many request in a span
                    if (((time_since_intitial_request < self.interval_seconds and (current_request_made + 1)) > self.maximum_requests) or (time_since_intitial_request > self.interval_seconds)):
                        time_sleep =  (time_since_intitial_request) - self.interval_seconds
                        #to ensure that if time sleep < 0, we still sleep the correct amount depending on which condiditn above is met
                        if (time_sleep < 0):
                            time_sleep = time_sleep * -1
                        #print(f"Sleep: {time_sleep} and Request made: {current_request_made}")
                        time.sleep(time_sleep)
                        current_request_made = 0
                        initial_request_time = time.time()
                    # Now execute the request and can hit post or get request 
                    response = self.make_request_with_retries(url) 
                    #print(f"Request to {url} completed with status code {response.status_code} with time {self.last_request_time} and time since initial time {time_since_intitial_request}")
                    #update current request made to keep track of request availble to be made
                    current_request_made += 1
                    #updating last_request_time to current time
                    self.last_request_time = time.time()
                #updating current time
            else: 
                break

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
async def main(rate_limited_api_requestor, end_point="https://www.example.com", queue_count=1):
    # Start processing the requests asyncc
    start_time = time.time()
    batch = asyncio.gather(rate_limited_api_requestor.queue_all_request(end_point,queue_count),rate_limited_api_requestor.process_request())
    result_request, reult_request = await batch

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"time taken: {elapsed_time:.2f} s")

if __name__ == "__main__":
    endpoint = "https://www.example.com"
    maximum_requests = sys.argv[0] 
    interval_seconds = sys.argv[1]
    rate_limited_api_requestor = RateLimitApiRequestorArbitary(maximum_requests=5, interval_seconds=5)
    keep_alive = True
    while keep_alive == True:
        val = int(input("Pls enter how many request you want to queue, if none pls enter negative value or 0: "))
        if val > 0: 
            #asynch process of adding and removing to queue so they can happen at similar times
            asyncio.run(main(rate_limited_api_requestor,"https://www.example.com",val))
        else: 
            keep_alive = False