from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from games.models import Game, GameCategory
from games.serializers import GameSerializer, GameCategorySerializer


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


# Using GenericView
class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'


class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-datail'


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer()
    name = 'game-list'


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'


