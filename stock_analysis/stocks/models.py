from django.db import models

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    
    def __str__(self):
        return self.symbol

class StockData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.IntegerField()

    class Meta:
        unique_together = ('stock', 'date')

    def __str__(self):
        return f"{self.stock.symbol} data for {self.date}"
    
    def save(self, *args, **kwargs):
        # Clean and convert volume before saving
        if isinstance(self.volume, str):
            self.volume = int(self.volume.replace(',', ''))
        super().save(*args, **kwargs)