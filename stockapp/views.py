from django.shortcuts import render
from django.http.request import HttpRequest
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from . import forms
from datetime import datetime
from .controllers import history
from .models import StockData
from typing import Iterable


@login_required
def index(request: HttpRequest) -> HttpResponse:

  if request.method == 'POST':

    form = forms.StockForm(request.POST)

    if form.errors:
      errors = form.errors.as_json()
      return JsonResponse(data=errors, safe=False, status=400)

    if form.is_valid():

      start_date = form.cleaned_data.get('start_date')
      end_date = form.cleaned_data.get('end_date')

      if start_date:
        start_date = datetime.strftime(start_date, '%Y-%m-%d')
      if end_date:
        end_date = datetime.strftime(end_date, '%Y-%m-%d')

      data = {
        'ticker_symbol': form.cleaned_data.get('ticker_symbol'),
        'start_date': start_date,
        'end_date': end_date,
      }

      data = history(**data)
      status: int = 200 if data else 400

      if data:
        for row in data:
          row_data: dict = {
            'ticker_symbol': form.cleaned_data.get('ticker_symbol'),
            'date': datetime.strptime(row['Date'], '%Y-%m-%d'),
            'open_price': round(row['Open'], 2),
            'close_price': round(row['Close'], 2),
          }

          row_exists: StockData | None = (
            StockData
            .objects
            .filter(ticker_symbol=row_data['ticker_symbol'].upper(), date=row_data['date'])
            .first()
          )

          if not row_exists:
            StockData.objects.create(**row_data)


      return JsonResponse(data=data, safe=False, status=status)
    
  else:
    form = forms.StockForm()

  data: Iterable[StockData] = (
    StockData
    .objects
    .all()
    .order_by('-date')
  )

  return render(
    request=request,
    template_name='dashboard/index.html',
    context={
      'form': form,
      'data': data
    }
  ) 