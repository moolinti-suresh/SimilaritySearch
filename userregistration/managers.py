from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(
        self,
        user_id,
        username,
        password=None,
        **extra_fields
    ):

        if not user_id:
            raise ValueError("User ID is required")

        if not username:
            raise ValueError("Username is required")

        user = self.model(
            user_id=user_id,
            username=username,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        user_id,
        username,
        password=None,
        **extra_fields
    ):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            user_id,
            username,
            password,
            **extra_fields
        )