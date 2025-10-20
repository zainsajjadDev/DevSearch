from django.core.exceptions import ValidationError
import re

class SymbolValidator:
    def validate(self, password, user=None):
        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError(
                "Your password must contain at least one symbol (e.g. !@#$%^&*).",
                code='password_no_symbol'
            )

        if len(password) < 8:
            raise ValidationError(
                "Your password must be at least 8 characters long.",
                code="minimum_length"
            )

    def get_help_text(self):
        return (
            "Your password must contain at least one symbol like !@#$%^&*() "
            "and must be at least 8 characters long."
        )

class NameVaidator:
    def validate(self,username):
        if not re.match( r'^[a-zA-Z]',username):
            raise ValidationError("Username must start with alphabet" , code = "namecheck")