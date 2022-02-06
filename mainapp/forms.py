from django import forms


class PrivacyRemoveForm(forms.Form):
    email = forms.EmailField(label='Электронная почта', required=True)
    message = forms.CharField(widget=forms.Textarea, label='Сообщение', required=True)

    def __init__(self, *args, **kwargs):
        super(PrivacyRemoveForm, self).__init__(*args, *kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
