from rest_framework.serializers import *

from .models import *

from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler  = api_settings.JWT_ENCODE_HANDLER


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

        user=User.objects.create_user(user_type=user_type,first_name=first_name,last_name=last_name,email=email,username=username)
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

class LoginSerializer(Serializer):
    email=EmailField(error_messages={'required':'email key is required','blank':'email is required'})
    password=CharField(error_messages={'required':'password key is required','blank':'password is required'})
    token=CharField(read_only=True,required=False)

    def validate(self,data):
        qs=User.objects.filter(email=data.get('email'))
        if not qs.exists():
            raise ValidationError("No account with this email")

        user=qs.first()
        if user.check_password(data.get('password'))==False:
            raise ValidationError("Invalid Password")
        payload =  jwt_payload_handler(user)
        token   =  jwt_encode_handler(payload)
        data['token'] ='JWT '+str(token)
        return data

