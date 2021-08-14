from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.common.permissions import IsOwnerOrReadOnly

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ViewSet):
    # TODO: Add `slug` field as lookup.
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Post.objects.select_related("author", "author__user")
    serializer_class = PostSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={
                                           "author": request.user.profile})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
