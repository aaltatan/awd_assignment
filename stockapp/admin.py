from django.contrib import admin
from .models import StockData


@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
  list_display = ['ticker_symbol', 'date', 'open_price', 'close_price']
  list_filter = ['ticker_symbol']
  search_fields = ['ticker_symbol']
  ordering = ['-date']
  list_per_page = 10 