# cial-assignement


## Observations and disclaimers

### Tech Stack choices
I decided to go with scrapy and klein because I have worked with the two before and knew with could have a good performance.
Also, I haven't achieve good results using scrapy with FastAPI(my usual choice for api development) for realtime data scrapping
and decided to keep scrapy instead of FastAPI. Klein is a simple but function framework despite lacking some resources that FastAPI
has.

### Regarding database
I was planning to use MongoDB as the database, as it could be faster and more practical using a documented oriented approach.
However, close to the deadline I noticed that the database should be postgres (my bad, should have read more careful) and 
ended messing up a bit and storing only information regarding the purchase, instead of the whole information.

### Regarding docker
I wasn't able to make the docker compose work, I made some researches and found out some people were having issues with 
Mac M1 ship. This may be the reason, maybe not. I left the dockerfiles and docker-compose even I wasn't able to make it work.

### Regarding REST APIs
I noticed that the mentioned paths on the assignment didn't follow some REST guidelines, as using plural nouns and not sending
Post data in the urls, so I changed it a little.

### Final remarks
This wasn't my best performance on an assignment, but I'm glad that I tried. I was able to identify some things that I need to learn
more, and applying some knowledge.

### .env
As my docker-compose wasn't successful I left the `.env` file on github, but I know is not a good practice.

## Running the application

### Requirements:
- Python 3.12
- Poetry
- Docker

### setup
`$ cd cial`
`$ make setup_db`

### run
`$ cd cial`
`$ make run`

### test
`$ cd cial`
`$ make unit_tests`

### Request examples:

`http://localhost:8080/stocks/aapl`
`curl --location 'http://localhost:8080/stocks/' \
--header 'Content-Type: application/json' \
--data '{"amount":5, "stock_symbol":"aapl"}'`

