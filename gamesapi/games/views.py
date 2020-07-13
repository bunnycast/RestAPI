from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse

from games.models import Game, GameCategory, Player, PlayerScore
from games.permissions import IsOwnerOrReadOnly
from games.serializers import GameSerializer, GameCategorySerializer, PlayerSerializer, PlayerScoreSerializer, \
    UserSerializer

from rest_framework.throttling import ScopedRateThrottle


## using JSONResponse HttpResponse Class
# class JSONResponse(HttpResponse):
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'applications/json'
#         super(JSONResponse, self).__init__(content, **kwargs)
#
#
# @csrf_exempt  # 사이트 간 요청 위조 쿠키(Cross-Site Request Forgery)
# def game_list(request):
#     if request.method == "GET":
#         games = Game.objects.all()
#         games_serializer = GameSerializer(games, many=True)
#         return JSONResponse(games_serializer.data)
#
#     elif request.method == "POST":
#         game_data = JSONParser().parse(request)
#         game_serializer = GameSerializer(data=game_data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             return JSONResponse(game_serializer.data, status=status.HTTP_201_CREATED)
#         return JSONResponse(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @csrf_exempt
# def game_detail(request, pk):
#     try:
#         game = Game.objects.get(pk=pk)
#     except Game.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         game_serializer = GameSerializer(game)
#         return JSONResponse(game_serializer.data)
#
#     elif request.method == "PUT":
#         game_data = JSONParser().parse(request)
#         game_serializer = GameSerializer(data=game_data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             return JSONResponse(game_serializer.data)
#         return JSONResponse(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == "DELETE":
#         game.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)  # json으로 반환할 필요가 없으므로 HttpResponse로 반환


# # using API_VIEW
# @api_view(['GET', 'POST'])
# def game_list(request):
#     if request.method == 'GET':
#         games = Game.objects.all()
#         games_serializer = GameSerializer(games, many=True)
#         return Response(games_serializer.data)
#
#     elif request.method == 'POST':
#         game_serializer = GameSerializer(data=request.data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             return Response(game_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def game_detail(request, pk):
#     try:
#         games = Game.objects.get(pk=pk)
#     except Game.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         game_serializer = GameSerializer(games)
#         return Response(game_serializer.data)
#
#     elif request.method == 'PUT':
#         game_serializer = GameSerializer(data=request.data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             return Response(game_serializer.data)
#         return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         Game.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


# Using GenericView
class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)


class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def perform_create(self, serializer):
        # 요청으로 받은 사용자로 소유자를 설정하기 위해
        # create 메서드에게 추가적인 owner 필드를 전달
        serializer.save(owner=self.request.user)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


class PlayerScoreList(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-list'


class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'


class ApiRoot(generics.GenericAPIView):  # api 경로를 보는 하이퍼링크 제공 P.144
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'players': reverse(PlayerList.name, request=request),
            'game-categories': reverse(GameCategoryList.name, request=request),
            'games': reverse(GameList.name, request=request),
            'scores': reverse(PlayerScoreList.name, request=request),
            'users': reverse(UserList.name, request=request),
        })
