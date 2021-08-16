from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from apps.common.permissions import IsOwnerOrReadOnly

from .models import Post
from .pages import DefaultPagination
from .serializers import PostSerializer


class PostViewSet(viewsets.ViewSet):
    # A lookup field except for pk has to be defined because router doesn't specify each url.
    lookup_field = "slug"
    permission_classes = (IsOwnerOrReadOnly, )
    # author is Profile model, so it requires User model for user info.
    queryset = Post.objects.select_related("author", "author__user")
    serializer_class = PostSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = self.queryset

        author = self.request.query_params.get('author', None)
        if author is None:
            raise ValidationError(detail=f"`author` is not given.")
        queryset = queryset.filter(author__user__username=author)
        return queryset

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

    def list(self, request):
        pagination = self.pagination_class()
        page = pagination.paginate_queryset(self.get_queryset(), request)
        serializer = self.serializer_class(page, many=True)
        return pagination.get_paginated_response(serializer.data)
