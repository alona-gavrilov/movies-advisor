# movies-advisor
Ask movies advisor to find a movie for you at https://moviesadvisor.netlify.app/
This search engine utilizes movies DB adapted from kaggle movies dataset (5000 records). 

High level flow of this application, using AWS resources:  

moviesadvisor.netlify.app Frontend → API Gateway → Lambda → RDS postgreSQL → Lambda → API Gateway → Frontend  

*possible cold starts for lambda, if not active long time
