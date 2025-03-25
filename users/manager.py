from typing import Any
from django.contrib.auth.models import BaseUserManager




class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, username: str, password=None, **extra_fields: Any) -> Any:
        if not username:
            raise ValueError("Username is required.")
        
        user = self.model(username = username, password=password,**extra_fields)
        user.set_password(password)
        user.save(using= self.db)
        return user
        
    def create_superuser(self, username: str, password=None, **extra_fields: Any) -> Any:
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(username, password, **extra_fields)