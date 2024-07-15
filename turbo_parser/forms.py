from django import forms
from turbo_parser.models import Order

CHOICES= (
('USD','USD'),
('AZN','AZN'),
('EUR','EUR'),
)

class AddOrderForm(forms.ModelForm):
    threshold = forms.FloatField(widget=forms.NumberInput())
    currency = forms.CharField(widget=forms.Select(choices=CHOICES))
    ordered_link = forms.URLField(widget=forms.TextInput(attrs={'placeholder': '...'}))

    class Meta:
        model = Order
        fields = ('threshold', 'currency', 'ordered_link')

    def __init__(self,  *args, **kwargs):
        super(AddOrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['currency'].widget.attrs['class'] = 'form-select'