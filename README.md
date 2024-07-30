For Challenge 1, I have created a threaded and non threaded version of the rateLimited api. 

challenge_one.py 
Architecture:
1) There is a single queue that we add request too
2) We process these records sequentially while saving our last_request_time and our current request made while we iterate through the queue to rate limit our calls
3) We did not multithread bc adding threading, especailly with a queue datastructure, complicates the code and especially with rate limit apis, things can get very messy with implementation, there are also other libraries that bridge this gap more effeciently than using a queue like using python ratelimit module with ThreadPoolExecutor
 
HOWEVER....
    it is more optimal to thread the code as it really helps when we have huge rates limits like 10000+ hits per min....

challenge_one_threaded.py 
Architecture:
1) There is a single queue that we add request too
2) We process these records concurrently while saving our last_request_time and our current request made while we iterate throught the queue
3) We are multi-threading based on using current_request_made as a static var that is shared across all the instances of the class, this makes sure that we do not pass the rate limit across all instances of the class...

***
challenge_one_arbitary.py

We can now run the script with arguments:

    code_challenges/src/challenge_one/challenge_one_arbitary.py "" 5 5


    maximum_requests = sys.argv[0] 
    interval_seconds = sys.argv[1]


Prompt to be able to add at arbitary times:
    Pls enter how many request you want to queue, if none pls enter negative value or 0:

Archeticture:
    ideally there will be 1 global function that can update the queue to add request, once the request is placed in the queue 
    than we can process these request asynch on concurrently on the seperate thread so we can keep processing on the main func....

    For this example, i did things VERY simply... we have 1 thread that is doing the processing from adding to the queue to sending the request.... both adding to the queue and sending the request is happening asynch. Ideally we can add to the queoe W/O having to wait for the api calls to complete...

    Program will ask Users input if they want to add to the queue or end the program, hopefully this is what works for adding to the queue at arbitray times. Other main threads will should be able to hit this global func at any time, in this case it is user response....

    Sample logs:
    Added queue size: 1
    Added queue size: 2
    Removed queue size: 1
    Added queue size: 2
    Removed queue size: 1
    Added queue size: 2
    Removed queue size: 1
    Added queue size: 2
    Removed queue size: 1
    Removed queue size: 0
    time taken: 0.33 s

    ^processing is happening concurrently...


***


Running Challenge 1
Challenge_one.py
1) We can simply run the module and get reponse: 
    Request to https://www.example.com completed with status code 200 with time 1721915730.533246
    Request to https://www.example.com completed with status code 200 with time 1721915730.584239
    Request to https://www.example.com completed with status code 200 with time 1721915730.637563
    Sleep: 9.999999046325684 and Request made: 4
    Request to https://www.example.com completed with status code 200 with time 1721915730.700114
    Request to https://www.example.com completed with status code 200 with time 1721915740.767566
    Request to https://www.example.com completed with status code 200 with time 1721915740.8256588
    Request to https://www.example.com completed with status code 200 with time 1721915740.880426
    Sleep: 9.999999046325684 and Request made: 4
    Request to https://www.example.com completed with status code 200 with time 1721915740.941678

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
    outgoing_dir and data dirs are already placed "src/resources/data/", "src/resources/outgoing_data/"


P.S.
    If had some more time, would have made some unit test! but mocking request and checking thread counts/rate limits can get a little tricky