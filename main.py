import models
import yfinance as yf
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Stock


app = FastAPI()

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory = 'templates')


class StockRequest(BaseModel):
	symbol: str
def get_db():
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close()

def fetch_stock_data(id:int):
	db = SessionLocal()
	stock = db.query(Stock).filter(Stock.id ==id).first()

	yData = yf.Ticker(stock.symbol)

	stock.price = yData.info['previousClose']
	stock.forward_pe = yData.info['forwardPE']
	stock.forward_eps = yData.info['forwardEps']
	if yData.info['dividendYield'] != None:
		stock.dividend_yield = yData.info['dividendYield'] *100
	stock.ma50 = yData.info['fiftyDayAverage']
	stock.ma200 = yData.info['twoHundredDayAverage']

	db.add(stock)
	db.commit()
#home route
@app.get('/')
def home(request: Request, forward_pe = None, dividend_yield = None, ma50 = None, ma200 = None,db: Session = Depends(get_db)):
	stocks = db.query(Stock)
	
	if forward_pe:
		stocks = stocks.filter(Stock.forward_pe < forward_pe)
	if dividend_yield:
		stocks = stocks.filter(Stock.dividend_yield > dividend_yield)
	if ma50:
		stocks = stocks.filter(Stock.price > Stock.ma50)
	if ma200:
		stocks = stocks.filter(Stock.price > Stock.ma200)
	return templates.TemplateResponse('home.html',{
		'request': request,
		'stocks': stocks,
		'dividend_yield': dividend_yield,
		'ma50' : ma50,
		'ma200': ma200
		})


@app.post('/stock')
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
	stock = Stock()
	stock.symbol = stock_request.symbol

	db.add(stock)
	db.commit()

	background_tasks.add_task(fetch_stock_data, stock.id)

	return {
	'code':'success',
	'message':'stock created'
	}