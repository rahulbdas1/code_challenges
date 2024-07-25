# For Challenge 1, I have created a threaded and non threaded version of the rateLimited api. 

challenge_one.py Architecture:
1) There is a single queue that we add request too
2) We process these records sequentially while saving our last_request_time and our current request made while we iterate throught the queue to rate limit our calls
3) We did not multithread bc adding threading, especailly with a queue datastructure, complicates the code and especially with rate limit apis, things can get very messy with implementation, there are also other libraries that bridge this gap more effeciently than using a queue like using python ratelimit module with ThreadPoolExecutor
 
however....
    it is more optimal to thread the code as it really helps when we have huge rates limits like 10000+ hits per min....
challenge_one_threaded.py Architecture:
1) There is a single queue that we add request too
2) We process these records concurrently while saving our last_request_time and our current request made while we iterate throught the queue
3) We are multi-threading based on using current_request_made as a static var that is shared across all the instances of the class, this makes sure that we do not pass the rate limit across all instances of the class...

Running Challenge 1
Challenge_one.py
1) We can simply run the files and get reponse: 
Request to https://www.example.com completed with status code 200 with time 1721873573.859222
Request to https://www.example.com completed with status code 200 with time 1721873573.859222
Sleep: 10.13070011138916 and Request made: 2
Request to https://www.example.com completed with status code 200 with time 1721873573.859222
Request to https://www.example.com completed with status code 200 with time 1721873573.859222
Sleep: 20.3896541595459 and Request made: 2
Request to https://www.example.com completed with status code 200 with time 1721873573.859222
Request to https://www.example.com completed with status code 200 with time 1721873573.859222

Logs show how long we are sleeping and the requests we make during that time...

Challenge_one.py
Request to https://www.example.com completed with status code 200 with time 1721913693.8270562 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913693.8903449 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913693.9413939 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913693.994364 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913694.060012 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913694.1207411 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913694.172917 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913694.244559 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913694.3069499 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913694.371514 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913694.425964 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913694.513015 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913694.570592 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913694.6283488 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913694.682166 and thread: Thread-1
Request to https://www.example.com completed with status code 200 with time 1721913694.757983 and thread: Thread-16
Request to https://www.example.com completed with status code 200 with time 1721913694.808588 and thread: Thread-16
Request to https://www.example.com completed with status code 200 with time 1721913694.862093 and thread: Thread-16
Request to https://www.example.com completed with status code 200 with time 1721913694.911006 and thread: Thread-16
Request to https://www.example.com completed with status code 200 with time 1721913694.961378 and thread: Thread-16
Request to https://www.example.com completed with status code 200 with time 1721913695.0124302 and thread: Thread-16
Request to https://www.example.com completed with status code 200 with time 1721913695.0658612 and thread: Thread-16
Request to https://www.example.com completed with status code 200 with time 1721913695.12122 and thread: Thread-16
Request to https://www.example.com completed with status code 200 with time 1721913695.178088 and thread: Thread-16
Request to https://www.example.com completed with status code 200 with time 1721913695.229294 and thread: Thread-16
Request to https://www.example.com completed with status code 200 with time 1721913695.2906969 and thread: Thread-16
Request to https://www.example.com completed with status code 200 with time 1721913695.347065 and thread: Thread-16
Request to https://www.example.com completed with status code 200 with time 1721913695.402016 and thread: Thread-28
Request to https://www.example.com completed with status code 200 with time 1721913695.457769 and thread: Thread-29
Sleep: 9.999999046325684 and Request made: 29
Request to https://www.example.com completed with status code 200 with time 1721913695.518969 and thread: Thread-29



Challenge Two:
    challenge_two.py:
    I took the simpler route here and processed evg in pandas from reading csv, transforming data, and writing to csv. As data size in in the many thousands, that is not too much data, so we can still use pandas even though its not optimized for processing big data... but pandas are very easy to read, so with smaller data sizes, its the ideal processing engine imo!

    challenge_two_threaded.py:
    I noticed that the request for each url was taking very long time since this was beng done sequentially in challenge_two so i decided to add mulitthreading to processing the request and calculating the redirect_url. We are still using pandas to process/store the data locally...

    Running challenge_two:
    We can simply run the modules and the main methods will process urls_big.csv or urls.csv using the func url_redirect_detector

