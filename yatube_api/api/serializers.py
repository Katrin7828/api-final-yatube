from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Follow, Group

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор постов."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group',)
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'post', 'created',)
        read_only_fields = ('post',)
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = ('user', 'following',)
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны на этого пользователя!'
            )
        ]

    def validate_following(self, value):
        """Нельзя подписаться на себя самого."""
        request = self.context.get('request')
        if request and request.user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return value


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор сообществ."""

    class Meta:
        fields = ('id', 'title', 'slug', 'description',)
        model = Group
