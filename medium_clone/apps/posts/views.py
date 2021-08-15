from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.common.permissions import IsOwnerOrReadOnly

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ViewSet):
    # A lookup field except for pk has to be defined because router doesn't specify each url.
    lookup_field = "slug"
    permission_classes = (IsOwnerOrReadOnly, )
    # author is Profile model, so it requires User model for user info.
    queryset = Post.objects.select_related("author", "author__user")
    serializer_class = PostSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={
                                           "author": request.user.profile})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, slug):
        try:
            instance = self.queryset.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(f"slug `{slug}` doesn't exist.")

        serializer = self.serializer_class(instance=instance)

        return Response(serializer.data, status=status.HTTP_200_OK)
