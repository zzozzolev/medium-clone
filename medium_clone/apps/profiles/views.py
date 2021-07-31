from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from apps.common.permissions import IsOwnerOrReadOnly

from .models import Profile
from .serializers import ProfileSerializer


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    # Allow only get and patch.
    # PUT is used when client wants to create or update object by given data.
    # But profile should be created only once when user is created.
    http_method_names = ["get", "patch"]

    def retrieve(self, request, username, *args, **kwargs):
        profile = self.queryset.get(user__username=username)
        serializer = self.serializer_class(profile)

        return Response(serializer.data)

    # PATCH
    def partial_update(self, request, username, *args, **kwargs):
        profile = self.queryset.get(user__username=username)
        self.check_object_permissions(request, profile)
        serializer = self.serializer_class(
            instance=profile, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)
