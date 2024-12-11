from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.users.serializers import UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
