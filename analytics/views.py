from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from analytics.models import Board, Comment
from analytics.serializers import BoardSerializer, CommentSerializer, PostCommentSerializer


class BoardListCreate(ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope,)
    required_scopes = ['read']

    def get_queryset(self):
        values = Board.objects.filter(rol=self.kwargs["pk"])
        return get_object_or_404(values)


class BoardObject(RetrieveAPIView):
    serializer_class = BoardSerializer
    permission_classes = (IsAuthenticatedOrTokenHasScope,)
    required_scopes = ['read']

    def get_queryset(self):
        values = Board.objects.filter(pk=self.kwargs["pk"])
        return get_object_or_404(values)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CommentListCreate(ListCreateAPIView):
    parser_classes = [JSONParser]
    permission_classes = (IsAuthenticatedOrTokenHasScope,)
    required_scopes = ['read', 'write']

    def get_queryset(self):
        values = Comment.objects.filter(board=self.kwargs["pk"]).order_by('-created_at')
        return values

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = CommentSerializer(instance, many=True)
        data = serializer.data
        return response_data(message='success comments', extra_data={'comments': data})

    def post(self, request, format=None, **kwargs):
        posts = PostCommentSerializer(data=request.data, context={'request': request})
        if posts.is_valid():
            posts.save()
            return response_data("success", extra_data=None)
        else:
            return response_data("fail", status=400, extra_data=None)


def response_data(message, status=200, extra_data=None):
    data = {'coderesponse': 0, 'message': message, 'date': now().strftime("%Y/%m/%d %H:%M:%S")}
    if extra_data:
        data.update(extra_data)
    return Response(status=status, data=data)