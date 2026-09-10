from rest_framework import viewsets, filters, permissions, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated)
from django.shortcuts import get_object_or_404

from posts.models import Post, Group, Comment
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления постами."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        """Автоматически подставляем автора."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для управления сообществами."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly,)

    def get_post(self):
        """Получаем пост по id из URL."""
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        """Получаем комментарии только для конкретного поста."""
        return Comment.objects.filter(post=self.get_post())

    def perform_create(self, serializer):
        """Автоматически подставляем автора и пост."""
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Вьюсет для упрваления подписками."""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('following__username',)

    def get_queryset(self):
        """Возвращаем подписки только текущего пользователя."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Автоматически подставляем пользователя."""
        serializer.save(user=self.request.user)
