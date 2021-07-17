from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer


class ProfileRetrieveView(RetrieveAPIView):
    permission_classes = (AllowAny, )
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        profile = self.queryset.get(user__username=username)
        serializer = self.serializer_class(profile)

        return Response(serializer.data)
