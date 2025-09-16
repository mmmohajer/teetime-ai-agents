from rest_framework import serializers

from core.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField('get_groups')

    def get_groups(self, obj):
        user_groups_queryset = obj.groups.all()
        cur_user_groups = [group.name for group in list(user_groups_queryset)]
        return cur_user_groups

    class Meta:
        model = UserModel
        fields = ['id', 'uuid', 'first_name', 'last_name', 'email', 
                  'is_active', 'date_joined', 'groups', 'email', 'last_login']
        