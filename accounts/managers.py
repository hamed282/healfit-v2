from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, prefix_number=None,
                    phone_number=None, trn_number=None, company_name=None):
        if not email:
            raise ValueError('Email must be')

        user = self.model(first_name=first_name,
                          last_name=last_name,
                          email=self.normalize_email(email),
                          prefix_number=prefix_number,
                          phone_number=phone_number,
                          trn_number=trn_number,
                          company_name=company_name,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(first_name, last_name, email, password)
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
