from rest_framework import serializers

from account.models import Rol
from account.serializers import UserDataSerializer
from analytics.models import Board, Comment, TypeBoard


class TypeBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeBoard
        fields = ['name', 'code']


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name']


class BoardSerializer(serializers.ModelSerializer):
    type = TypeBoardSerializer(many=False, read_only=True)

    class Meta:
        model = Board
        fields = ['name', 'description', 'type', 'status', 'created_at']


class BoardsByRolSerializer(serializers.ModelSerializer):
    boards = BoardListSerializer(many=True, read_only=False)

    class Meta:
        model = Rol
        fields = ['name', 'boards']


class CommentSerializer(serializers.ModelSerializer):
    user = UserDataSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['message', 'user', 'created_at']


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['message', 'user', 'board']
