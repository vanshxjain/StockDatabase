# StockDatabase

The purpose of this tool is to create a local database of various stocks to be used in analysis and filtering.

## Instructions

First install all the required libraries

Libraries Needed:
- fastapi
- uvicorn
- jinja2
- yfinance
- sqlalchemy
- lxml

Notation :

pip install **library** 

or

(If using Anaconda)
conda install **library**

conda install -c ranaroussi yfinance
***only for yfinance library***

After downloading the project files, open a terminal window in that folder. Then run the following command:

uvicorn main:app --reload

This should start a local host session on your machine 

Open up you favorite browser and navigate to **localhost:8000**

## Result

![Example](/Example.png)
