# movies-advisor
Ask movies advisor to find a movie for you at https://moviesadvisor.netlify.app/
This search engine utilizes movies DB adapted from kaggle movies dataset (5000 records). 

High level flow of this application:

frontend: moviesadvisor.netlify.app UI; \n
backend: AWS api Gateway -> AWS lambda -> AWS RDS postgreSQL -> AWS lambda -> AWS api Gateway \n
*possible cold starts for lambda, if not active long time
