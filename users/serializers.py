from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


# class UserSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(
#         validators=[
#             UniqueValidator(
#                 queryset=User.objects.all(),
#                 message="A user with that username already exists.",
#             )
#         ],
#     )
#     email = serializers.EmailField(
#         validators=[UniqueValidator(queryset=User.objects.all())],
#     )
#     password = serializers.CharField(write_only=True)
#     first_name = serializers.CharField(max_length=50)
#     last_name = serializers.CharField(max_length=50)
#     is_superuser = serializers.BooleanField(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that username already exists.",
            )
        ],
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name", "is_superuser"]
        read_only_fields = ["id", "user_id"]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "username": {"required": True},
            "email": {"required": True},
        }

    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop("password", None)
        # a = instance.password
        # print(2, a)
        if password:
            instance.set_password(password)
            instance.save()
        #     print(6, instance.check_password(password))
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        # b = instance.password
        # print(3, b)
        # print(a == b)
        return instance
