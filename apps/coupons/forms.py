from django import forms
from .models import Coupon


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_type', 'value', 'valid_to', 'valid_from', 'max_usage',
                  'active']


class ApplyCouponForm(forms.Form):
    code = forms.CharField()
