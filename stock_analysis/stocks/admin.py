from django.contrib import admin
from import_export import fields, resources, widgets
from import_export.admin import ImportExportModelAdmin
from stock_analysis.stocks.forms.import_form import StockDataImportForm, StockDataConfirmImportForm
from .models import Stock, StockData

# Register your models here.
class StockDataResource(resources.ModelResource):
    date = fields.Field(attribute='date', column_name='Date', widget=widgets.DateWidget(format='%m/%d/%Y'))
    open_price = fields.Field(attribute='open_price', column_name='Open')
    close_price = fields.Field(attribute='close_price', column_name='Close')
    high_price = fields.Field(attribute='high_price', column_name='High')
    low_price = fields.Field(attribute='low_price', column_name='Low')
    volume = fields.Field(attribute='volume', column_name='Volume')
    stock_id = fields.Field(attribute='stock_id', column_name='stock_id')
    """ stock = fields.Field(attribute='stock', column_name='stock', widget=widgets.ForeignKeyWidget(Stock, 'symbol')) """
    
    class Meta:
        model = StockData
        exclude = ('id',)

    def before_import_row(self, row, **kwargs):        
        selected_stock_symbol = kwargs.get("selected_stock")
    
        if selected_stock_symbol:
            try:
                # Retrieve the Stock instance by symbol
                stock_instance = Stock.objects.get(symbol=selected_stock_symbol)
                row['stock_id'] = stock_instance.id  # Set the stock_id in the row
            except Stock.DoesNotExist:
                raise ValueError(f"Stock with symbol '{selected_stock_symbol}' does not exist.")
        else:
            raise ValueError("Stock selection is required before import.")
        return row
    
    def get_instance(self, instance_loader, row):
        date = row.get("date")
        stock_id = row.get("stock_id")

        # Attempt to retrieve an existing instance based on date and stock_id
        if date and stock_id:
            try:
                return StockData.objects.get(date=date, stock_id=stock_id)
            except StockData.DoesNotExist:
                return None  # No existing instance, so a new one will be created
        return None
    """ def after_import_instance(self, instance, new, row_number=None, **kwargs):
        instance.stock = kwargs["stock"] """
                                 
class StockDataAdmin(ImportExportModelAdmin):  
    resource_class = StockDataResource
    list_display = ['stock', 'date', 'open_price', 'close_price', 'high_price', 'low_price', 'volume']
    search_fields = ['stock__symbol', 'date']
    list_filter = ['date', 'stock__symbol']
    ordering = ['date']
    exclude = ['id']
    
    import_form_class = StockDataImportForm
    confirm_form_class = StockDataConfirmImportForm
    
    def get_confirm_form_initial(self, request, import_form_class):
        initial = super().get_confirm_form_initial(request, import_form_class)

        # Pass on the `stock` value from the import form to
        # the confirm form (if provided)
        if import_form_class:
            initial['stock'] = import_form_class.cleaned_data['stock']
        return initial
    
    def get_import_data_kwargs(self, request, *args, **kwargs):
        form = kwargs.get('form')
        if form:
            return {"selected_stock": form.cleaned_data["stock"].symbol}
        return dict()
    
admin.site.register(Stock, ImportExportModelAdmin)     
admin.site.register(StockData, StockDataAdmin)
