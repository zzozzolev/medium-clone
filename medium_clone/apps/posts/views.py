from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.common.permissions import IsOwnerOrReadOnly

from .serializers import PostSerializer


class PostViewSet(viewsets.ViewSet):
    # TODO: Add `slug` field as lookup.
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Post.objects.select_related("author", "author__user")
    serializer_class = PostSerializer

    def create(self, request):
        # TODO: Make test for this case.
        if "post" not in request.data:
            raise Response(request.data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(request.data["post"])
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
