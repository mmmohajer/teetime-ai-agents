from rest_framework import serializers

from core.models import UserModel
from core.models import ProfileModel

class UserForProfileSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField('get_groups')

    def get_groups(self, obj):
        user_groups_queryset = obj.groups.all()
        cur_user_groups = [group.name for group in list(user_groups_queryset)]
        return cur_user_groups

    class Meta:
        model = UserModel
        fields = ['id', 'uuid', 'first_name', 'last_name', 'email', 
                  'is_active', 'date_joined', 'groups', 'email', 'last_login']
        

class ProfileSerializer(serializers.ModelSerializer):
    user = UserForProfileSerializer(read_only=True)
    class Meta:
        model = ProfileModel
        fields = ['id', 'uuid', 'user', 'phone_number', 'birth_date', 
                  'mailing_city', 'mailing_province_state', 'mailing_country', 
                  'mailing_street_address', 'mailing_postal_code_zip', 'profile_photo',
                  'created_at', 'updated_at']
        