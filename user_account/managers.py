from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, phone, password, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        
        if not phone:
            raise ValueError("The phone number must be set")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, phone, password, **extra_fields):
        user = self.create_user(email=email, phone=phone, password=password, **extra_fields)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user