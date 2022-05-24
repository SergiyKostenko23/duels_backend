from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.transaction import atomic
from django.utils.text import slugify

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import User, Duel, Item, Result, Progress, Message
from .mixins import DynamicFieldsSerializerMixin

from urllib.request import urlopen
import itertools

#Serializer de users
class UserSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ('id', 'user', 'nome', 'email', 'data_registo', "password", 'tipo_user', 'criado_por', 'photo')
        fields = "__all__"

    @atomic
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if validated_data.get('photo', None) is not None:
            user.photo = user.photo.name[user.photo.name.find('/img'):]

        if validated_data.get('password', None) is not None:
            user.set_password(validated_data['password'])

        user.save()
        return user
  
    @atomic
    def create(self, validated_data):
        user = super().create(validated_data)
        if validated_data.get('photo', None) is not None:
            user.photo = user.photo.name[user.photo.name.find('/img'):]

        if validated_data.get('password', None) is not None:
            user.set_password(validated_data['password'])

        try:
            u = self.context['request'].user
            user.criado_por = User.objects.filter(email=u)[0].id
        except:
            pass

        #Download de imagem a partir do url
        try:
            image_url = self.context['photo']
            img_temp = NamedTemporaryFile("w+b")
            img_temp.write(urlopen(image_url).read())
            img_temp.flush()
            user.photo = File(img_temp)
            user.photo.name = f"image_{user.id}.PNG"
        except:
            pass

        user.save()
        return user

class DuelSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Duel
        fields = "__all__"

    @atomic
    def create(self, validated_data):
        value = validated_data.get('nome')
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Duel.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
        duel = super().create(validated_data)
        duel.slug = slug_candidate
        duel.save()
        return duel

class ItemSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

    def create(self, validated_data):
        item = super().create(validated_data)
        if "youtu" in item.url:
            s = item.url.replace("watch?v=","embed/")
            item.url = s
        item.save()
        return item

class ResultSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ("id", "users", "duels", "result", "inicio", "fim")

class PrintResultSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    users = serializers.SlugRelatedField(
        slug_field = "nome",
        queryset = User.objects.all(),
    )
    duels = serializers.SlugRelatedField(
        slug_field = "nome",
        queryset = Duel.objects.all(),
    )
    class Meta:
        model = Result
        fields = ("id", "users", "duels", "result", "inicio", "fim")

    def to_representation(self, instance):
        temp_dict = super().to_representation(instance)
        temp_dict["result"] = ItemSerializer(
             Item.objects.filter(id__in=temp_dict["result"].split(',')), 
             many=True).data
        return temp_dict

class ProgressSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ("id", "chosen", "not_chosen", "user", "duel", "iteration")

    def to_representation(self, instance):
        temp_dict = super().to_representation(instance)
        temp_dict["chosen"] = ItemSerializer(
            Item.objects.filter(id__in=temp_dict["chosen"].split(',')), 
            many=True).data
        temp_dict["not_chosen"] = ItemSerializer(
            Item.objects.filter(id__in=temp_dict["not_chosen"].split(',')), 
            many=True).data
        return temp_dict

class MessageSerializer(DynamicFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
    
    def to_representation(self, instance):
        temp_dict = super().to_representation(instance)
        temp_dict["user_id"] = User.objects.filter(id=temp_dict["user"])[0].id
        temp_dict["photo"] = 'http://127.0.0.1:8000' + User.objects.filter(id=temp_dict["user"])[0].photo.url
        temp_dict["user"] = User.objects.filter(id=temp_dict["user"])[0].nome[:20]
        return temp_dict