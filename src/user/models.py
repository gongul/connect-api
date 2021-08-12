from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.db.models.deletion import CASCADE
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
    email = models.EmailField('이메일', primary_key=True, unique=True,
                              max_length=255, error_messages=UserValidationMessage.EMAIL.to_dict())
    password = models.CharField('패스워드', max_length=128, error_messages=UserValidationMessage.PASSWORD.to_dict())
    name = models.CharField('이름', max_length=10, error_messages=UserValidationMessage.NAME.to_dict())
    verifying_number = models.CharField('인증번호', blank=True, null=True, max_length=6, error_messages=UserValidationMessage.VERIFYING_NUMBER.to_dict())
    registration_date = models.DateTimeField('회원가입 일시', auto_now_add=True, error_messages=UserValidationMessage.PASSWORD.to_dict())
    is_verified = models.BooleanField('인증 여부', default=False, error_messages=UserValidationMessage.IS_VERIFIED.to_dict())
    is_active = models.BooleanField('활성화 여부', default=False, error_messages=UserValidationMessage.IS_ACTIVE.to_dict())

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


class Friend(models.Model):
    user_id = models.ForeignKey(User, related_name='user_friends', on_delete=CASCADE)
    friend_user_id = models.ForeignKey(User, related_name='friend_user_friends', on_delete=CASCADE)
    is_frined = models.BooleanField('친구 여부')
    request_date = models.DateTimeField('친구 요청일', auto_now_add=True, error_messages=UserValidationMessage.PASSWORD.to_dict())
    accept_date = models.DateTimeField('친구 수락일', blank=True, null=True, error_messages=UserValidationMessage.PASSWORD.to_dict())
