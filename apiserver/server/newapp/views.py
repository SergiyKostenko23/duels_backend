from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import F, ExpressionWrapper, DurationField

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.pagination import LimitOffsetPagination

#from google.oauth2 import id_token
#from google.auth.transport import requests
#from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication

from .pagination import HeaderLimitOffsetPagination
from .models import User, Duel, Item, Result, Item, Result, Progress, Message
from .serializers import UserSerializer, DuelSerializer, ItemSerializer, ResultSerializer, PrintResultSerializer, ProgressSerializer, MessageSerializer
from .mixins import DynamicFieldsViewMixin
from .permissions import CreateUserPermssion

#View para contornar CSRF
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

#View de users
class UserViewSet(DynamicFieldsViewMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CreateUserPermssion,)
    parser_class = (FileUploadParser,)
    SAFE_METHODS = ['GET']

    def edit(self, request):
        user_to_update = get_object_or_404(User, id=request.data["id"])
        serializer = UserSerializer(user_to_update, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request):
        user_to_destroy = get_object_or_404(User, id=request.data["id"])
        user_to_destroy.delete()
        return Response(_("User Successfully Deleted."), status=status.HTTP_200_OK)

    def create(self, request):
        serializer = UserSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        if "id" in request.query_params:
            if User.objects.filter(id=request.query_params["id"]):
                queryset = User.objects.filter(id=request.query_params["id"])
            else:
                return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#View de registar utilizadores
class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,)
    
    def create(self, request):
        serializer = UserSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

#View de user profiles
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    SAFE_METHODS = ['GET']

    def list(self, request):
        token = request.headers['Authorization']
        token = token.strip("token ")
        user = Token.objects.get(key=token).user
        queryset = User.objects.filter(id=user.id)
        serializer = UserSerializer(queryset, many=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)

#View de autenticação a partir de Google
"""class GoogleAuthViewSet(viewsets.ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get_id_token(self, request):
        token = request.data["idtoken"]
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Erro ao fazer autenticação com o Google.')
        except ValueError:
            return Response("Token inválido", status=status.HTTP_400_BAD_REQUEST)
        data = {
            "email":idinfo['email'],
            "nome":idinfo['name']
        }
        photo = idinfo['picture']
        if User.objects.filter(email=data['email']).count()>0:
            token = Token.objects.get_or_create(user=User.objects.get(email=data['email']))
            t = {
                "token": Token.objects.get(user=User.objects.get(email=data['email'])).key
                }
            return Response(t, status.HTTP_200_OK)
        else:            
            serializer = UserSerializer(data=data, context={'photo':photo})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            uid = User.objects.get(email=data['email']).id
            Token.objects.get_or_create(user=User.objects.get(id=uid))
            t = {
                "token": Token.objects.get(user=uid).key
                }
            return Response(t, status=status.HTTP_200_OK)"""

class DuelViewSet(DynamicFieldsViewMixin, viewsets.ModelViewSet):
    queryset = Duel.objects.all()
    serializer_class = DuelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    SAFE_METHODS = "GET"

    def create(self, request):
        serializer = DuelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(criador=request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        if "id" in request.query_params:
            if Duel.objects.filter(id=request.query_params["id"]):
                queryset = Duel.objects.filter(id=request.query_params["id"])
        elif "criador" in request.query_params:
            if Duel.objects.filter(criador=request.query_params["criador"]):
                queryset = Duel.objects.filter(criador=request.query_params["criador"])
        elif "slug" in request.query_params:
            if Duel.objects.filter(slug=request.query_params["slug"]):
                queryset = Duel.objects.filter(slug=request.query_params["slug"])
        else:
            queryset = Duel.objects.all()
        serializer = DuelSerializer(queryset, many=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def edit(self, request):
        duel_to_update = get_object_or_404(Duel, id=request.data["id"])
        serializer = DuelSerializer(duel_to_update, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request):
        duel_to_destroy = get_object_or_404(Duel, id=request.data["id"])
        duel_to_destroy.delete()
        return Response(_("Duel Successfully Deleted."), status=status.HTTP_200_OK)  

class ItemViewSet(DynamicFieldsViewMixin, viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    SAFE_METHODS = "GET"

    def create(self, request):
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        if "id" in request.query_params:
            if Item.objects.filter(id=request.query_params["id"]):
                queryset = Item.objects.filter(id=request.query_params["id"])
            else:
                return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        elif "duel" in request.query_params:
            if Item.objects.filter(duel=request.query_params["duel"]):
                queryset = Item.objects.filter(duel=request.query_params["duel"])
            else:
                return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Item.objects.all()
        serializer = ItemSerializer(queryset, many=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def edit(self, request):
        if isinstance(request.data, list):
            for x in request.data:
                item_to_update = get_object_or_404(Item, id=x["id"])
                serializer = ItemSerializer(item_to_update, x, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        else:
            item_to_update = get_object_or_404(Item, id=request.data["id"])
            serializer = ItemSerializer(item_to_update, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)  

    def destroy(self, request):
        item_to_destroy = get_object_or_404(Item, id=request.data["id"])
        item_to_destroy.delete()
        return Response(_("Item Successfully Deleted."), status=status.HTTP_200_OK)  

class ResultViewSet(DynamicFieldsViewMixin, viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    SAFE_METHODS = "GET"

    def create(self, request):
        serializer = ResultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        #queryset = Result.objects.annotate(tempo=F('fim')-F('inicio'))
        queryset = Result.objects.annotate(tempo=ExpressionWrapper(F('fim') - F('inicio'), output_field=DurationField()))
        def switch(i):
            switcher={
                "true": "",
                "false": "-"
            }
            return switcher.get(i,"false")
        def switch2(j):
            switcher={
                "1": "duels",
                "2": "tempo",
                "3": "fim"
            }
            return switcher.get(j,"fim")
        queryset = queryset.filter(users=request.user).order_by(switch(request.query_params["ascdesc"])+switch2(request.query_params["filter"]))
        page = self.paginate_queryset(queryset)
        serializer = PrintResultSerializer(page, many=True)
        return Response({'total': queryset.count() , 'limit': request.query_params["limit"], 'data':serializer.data})

class PopularDuelsViewSet(DynamicFieldsViewMixin, viewsets.ModelViewSet):
    queryset = Duel.objects.all()
    serializer_class = DuelSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    SAFE_METHODS = "GET"

    def list(self, request):
        queryset = Duel.objects.all().order_by('-feito')[:4]
        serializer = DuelSerializer(queryset, many=True)
        return Response(serializer.data)

class ProgressViewSet(DynamicFieldsViewMixin, viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        try:
            serializer = ProgressSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Erro ao criar progresso.")

    def list(self, request):
        try:
            queryset = Progress.objects.filter(user=request.user, duel=request.query_params["duel"])
            serializer = ProgressSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response("Erro ao listar progresso.")

    def destroy(self, request):
        try:
            progress_to_destroy = Progress.objects.filter(id=request.data["id"])
            progress_to_destroy.delete()
            return Response("Progresso eliminado com sucesso.", status=status.HTTP_200_OK)
        except:
            return Response("Erro ao eliminar progresso.")

    def edit(self, request):
        try:
            item_to_update = Progress.objects.get(id=request.data["id"])
            serializer = ProgressSerializer(item_to_update, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Erro ao editar progresso.")

class MessageViewSet(DynamicFieldsViewMixin, viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def list(self, request):
        try:
            queryset = reversed(Message.objects.filter().order_by('-id')[:20])
            serializer = MessageSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response("Erro ao imprimir mensagens.")