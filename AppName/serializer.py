from rest_framework.serializers import *

from .models import *

class SignUp(Serializer):
    first_name=CharField(max_length=20)
    last_name = CharField(max_length=20)
    password = CharField(max_length=20)
    email=EmailField(max_length=32)
    username = CharField(max_length=20)

    def validate(self, data):
        username=data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username exists')
        if User.objects.filter(email=email).exists():
            raise ValidationError('email exists')
        return data
    def create(self, validated_data):
        first_name=validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = validated_data.get('password')
        username = validated_data.get('username')
        user_type=validated_data.get('user_type')

        user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,user_type=1)
        user.set_password(password)
        user.save()
        return validated_data

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.email=validated_data.get('email')
        instance.save()
        return validated_data


class NoteSerializer(Serializer):
    name=CharField(max_length=30, error_messages={'required':"Name is required","blank":"name cannot be blank"})
    description=CharField(max_length=60, error_messages={'required':"desc is required","blank":"desc cannot be blank"})

    def create(self, data ):

        Notes.objects.create(user=self.context.get('user'), name=data.get('name'),description=data.get('description')).save()
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.description = validated_data.get('description')
        instance.save()
        return validated_data
