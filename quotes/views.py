from django.shortcuts import render, redirect
import requests, json
from django.contrib import messages
from .forms import StockForm

from .models import Stock

# Create your views here.
def home(request):
	# pk_0b3c3d42d48d49aa912fc264edb38151
	template = 'home.html'
	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_0b3c3d42d48d49aa912fc264edb38151")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."
		return render(request, template, {'api': api})

	else:
		return render(request, template, {'ticker': 'Enter a ticker symbol above'})

def about(request):
	template = 'about.html'
	return render(request, template, {})

def base(request):
	template = 'base.html'
	return render(request, template, {})

def add_stock(request):
	template = 'add_stock.html'
	if request.method == 'POST':
		form = StockForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, "Stock has been added successfully")
			return redirect('add_stock')
	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_0b3c3d42d48d49aa912fc264edb38151")


			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."
	return render(request, template, {'ticker':ticker, 'output': output})


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock item has been deleted"))

	return redirect(delete_stock)

def delete_stock(request):
	template = 'delete_stock.html'
	ticker = Stock.objects.all()

	return render(request, template, {'ticker': ticker})