from allauth.account.adapter import DefaultAccountAdapter
from django import forms


class AccountAdapter(DefaultAccountAdapter):
    
    def is_open_for_signup(self, request):
        return False
