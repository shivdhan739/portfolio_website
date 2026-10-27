from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=80)
    email = forms.EmailField(max_length=120)
    subject = forms.CharField(max_length=120, required=False)
    message = forms.CharField(max_length=2000)
    website = forms.CharField(required=False)  # honeypot: real users leave this empty

    def clean_name(self):
        return " ".join(self.cleaned_data["name"].split())

    def clean_subject(self):
        # collapse whitespace/newlines so the value is safe inside an email header
        return " ".join(self.cleaned_data.get("subject", "").split()) or "Portfolio contact"

    def clean_message(self):
        return self.cleaned_data["message"].strip()
