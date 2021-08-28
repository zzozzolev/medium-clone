from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from apps.common.permissions import IsOwnerOrReadOnly

from .exceptions import UserNoAccount
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
    # `to_internal_value` is called by `is_valid`
    # create and update should be distinguished for setting default values.
    update_context_key = "is_update"

    def get_queryset(self):
        queryset = self.queryset

        author = self.request.query_params.get('author', None)
        if author is None:
            raise ValidationError(detail=f"`author` is not given.")
        queryset = queryset.filter(author__user__username=author)

        if not queryset.exists():
            raise NotFound(f"author `{author}` doesn't exist.")

        return queryset

    def get_instance(self, slug):
        try:
            instance = self.queryset.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(f"slug `{slug}` doesn't exist.")

        return instance

    def create(self, request):
        # Anonymous user can't create a post.
        try:
            request.user.profile
        except AttributeError:
            raise UserNoAccount()

        serializer = self.serializer_class(data=request.data, context={
            "author": request.user.profile, self.update_context_key: False})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, slug):
        instance = self.get_instance(slug)
        serializer = self.serializer_class(instance=instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        pagination = self.pagination_class()
        page = pagination.paginate_queryset(self.get_queryset(), request)
        serializer = self.serializer_class(page, many=True)
        return pagination.get_paginated_response(serializer.data)

    def partial_update(self, request, slug):
        instance = self.get_instance(slug)
        self.check_object_permissions(request, instance.author)

        serializer = self.serializer_class(
            instance=instance, data=request.data, context={self.update_context_key: True})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def destroy(self, request, slug):
        instance = self.get_instance(slug)
        self.check_object_permissions(request, instance.author)

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
