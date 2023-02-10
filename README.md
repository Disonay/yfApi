# Python API to get some information about companies traded on the exchange

## General

Run server: `uvicorn main:app --reload`. Examples of data obtained with yfinance can be found in the jupyter notebook

## Endpoints

Basic info about endpoint. You can find more specific information in the swagger documentation: `/docs`

### First Endpoint 

`POST /tickers/info`

Request body structure:
* tickers
* period 
* interval

Response body is a list of the following elements:
* ticker
* quotes
* institutional_holders

### Second Endpoint 

`GET /tickers/options/{ticker_name}`

Response is True if the stock has tradable options. Options are traded throughout the expiration time

## Performance

The main problem with performance is getting information about institutional investors. 
The notebook shows that if you only get information on quotes, the processing takes 3-4 seconds. 
If you also get information about investors, then the processing already takes 40 seconds. 
And this is without any data transformations, only what was received from yfinance in the original form. 
This is most likely due to the way the Holders scrapper works
