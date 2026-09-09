from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Follow, Group

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор постов."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('user', 'following',)
        model = Follow

    def validate(self, data):
        """Нельзя подписаться на себя самого."""
        request = self.context.get('request')
        if request and request.user == data.get('following'):
            raise serializers.ValidationError(
                {'following': 'Нельзя подписаться на самого себя!'}
            )
        return data


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор сообществ."""

    class Meta:
        fields = ('title', 'slug', 'description',)
        model = Group
