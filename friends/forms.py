from django import forms


class FriendshipRequestForm(forms.Form):
    user_to_add_id = forms.IntegerField(widget=forms.HiddenInput())
