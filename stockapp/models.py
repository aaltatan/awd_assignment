from django.db import models
from django.core.validators import MinValueValidator


price_validators = [
  MinValueValidator(0, 'Price must be greater than zero')
]

class StockData(models.Model):
  ticker_symbol = models.CharField(max_length=20)
  date = models.DateField()
  open_price = models.DecimalField(max_digits=10, 
                                   decimal_places=2,
                                   validators=price_validators)
  close_price = models.DecimalField(max_digits=10, 
                                    decimal_places=2,
                                    validators=price_validators)

  class Meta:
    verbose_name_plural = 'Stocks Data'

  def save(self, *args, **kwargs) -> None:
    self.ticker_symbol = self.ticker_symbol.upper()
    return super().save(*args, **kwargs)

  def __str__(self) -> str:
    attr: list[str] = [
      f'ticker_symbol={self.ticker_symbol}',
      f'date={self.date}',
      f'open_price={self.open_price}',
      f'close_price={self.close_price}',
    ]
    return f'Ticker({", ".join(attr)})'