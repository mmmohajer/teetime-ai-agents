from rest_framework import views, permissions, response, status

from core.models import ProfileModel
from core.serializers import ProfileSerializer


class ProfileViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try:
            profile = ProfileModel.objects.get(user_id=request.user.id)
            serializer = ProfileSerializer(profile)
            return response.Response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as e:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"{str(e)}"})