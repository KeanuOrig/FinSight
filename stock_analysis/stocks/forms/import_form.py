from django import forms
from ..models import Stock
from import_export.forms import ImportForm, ConfirmImportForm

# Custom import form with an additional field for selecting stock
class StockDataImportForm(ImportForm):
    stock = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        required=True,
        label="Select Stock"
    )
    
# Custom confirm import form with the same field
class StockDataConfirmImportForm(ConfirmImportForm):
    stock = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        required=True,
        label="Selected Stock",
        disabled=True
    )