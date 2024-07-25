# For Challenge 1, I have created a threaded and non threaded version of the rateLimited api. 

Challenge 1 Architecture: 
1) There is a single queue that we add request too
2) We process these records sequentially while saving our last_request_time and our current request made while we iterate throught the queue
3) We did not multithread for one class bc adding threading substanitally complicates the code and especially with rate limit apis, things can get very messy with implementation
 
however....
    it is more optimal to thread the code as it really helps when we have huge rates like 10000+ hits per hour....

Running Challenge 1
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


Challenge Two: 
    I took the simpler route here and processed evg in pandas from reading csv, transforming data, and writing to csv in pandas. As data size in in the many thousands, that is not too much data, so we can still use pandas even though its not hyper optimized for processing big data... pandas are very easy to read, so with smaller data sizes, its the ideal processing engine imo!

    If we want we can optimize by multi-threading this process as well, so we can request mulitple URLs concurrently to speed up the process... or we can convert this whole process to using csv readers and using list as a datastructure. 