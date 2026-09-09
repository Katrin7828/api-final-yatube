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
        read_only_fields = ('post', 'author')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = ('user', 'following',)
        model = Follow

    def validate(self, data):
        """Нельзя подписаться на себя самого."""
        request = self.context.get('request')
        following = data.get('following')
        if request and request.user == following:
            raise serializers.ValidationError(
                {'following': 'Нельзя подписаться на самого себя!'}
            )
        if Follow.objects.filter(user=request.user,
                                 following=following).exists():
            raise serializers.ValidationError(
                {'following': 'Вы уже подписаны на этого пользователя!'}
            )
        return data


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор сообществ."""

    class Meta:
        fields = ('id', 'title', 'slug', 'description',)
        model = Group
