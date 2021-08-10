from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone

from user.validator.message import UserValidationMessage


class UserManager(BaseUserManager):
    def create_user(self, email, name, password, is_active=False, is_verified=False):
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            is_active=is_active,
            is_verified=is_verified
        )

        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("이메일", primary_key=True, unique=True,
                              max_length=255, error_messages=UserValidationMessage.EMAIL.to_dict())
    password = models.CharField("패스워드", max_length=128, error_messages=UserValidationMessage.PASSWORD.to_dict())
    name = models.CharField("이름", max_length=10, error_messages=UserValidationMessage.NAME.to_dict())
    verifying_number = models.CharField("인증번호", blank=True, null=True, max_length=6, error_messages=UserValidationMessage.VERIFYING_NUMBER.to_dict())
    registration_date = models.DateTimeField("회원가입 일시", default=timezone.now, error_messages=UserValidationMessage.PASSWORD.to_dict())
    is_verified = models.BooleanField(default=False, error_messages=UserValidationMessage.IS_VERIFIED.to_dict())
    is_active = models.BooleanField(default=False, error_messages=UserValidationMessage.IS_ACTIVE.to_dict())

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'user'

    @property
    def is_staff(self):
        "관리자 사이트에 엑세스 할 수 있는지 여부"
        return self.is_superuser
