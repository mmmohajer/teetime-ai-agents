getJsContext() {
    local compName=$1
    compName="$(tr '[:lower:]' '[:upper:]' <<< ${compName:0:1})${compName:1}"

    echo """import Div from \"@/baseComponents/reusableComponents/Div\";

const $compName = () => {
  return (
    <>
      <Div>$compName</Div>
    </>
  );
};

export default $compName;
"""
}

getJsPageContext() {
    local compName=$1
    compName="$(tr '[:lower:]' '[:upper:]' <<< ${compName:0:1})${compName:1}"

    echo """import Seo from '@/components/wrappers/Seo';
import PageContainer from '@/components/wrappers/PageContainer';

const Index = () => {
  return (
      <Seo>
        <PageContainer>
          Hello!!!
        </PageContainer>
      </Seo>
  );
};

export default Index;
"""
}

getAppsContext() {
local appName=$1

echo """from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '$appName'
"""
}

getUrlsContext() {
echo """from django.urls import path, include
from rest_framework import routers
"""
}

getDjangoModelContext() {
echo """from django.db import models

from core.models.base_model import TimeStampedUUIDModel


class ModelName(TimeStampedUUIDModel):
    # Add your fields here

    def __str__(self):
        return f\"String to return\"

    class Meta:
        verbose_name_plural = \"Plural Name\"
        ordering = ('id',)
"""
}

getDjangoSerializerContext() {
echo """from rest_framework import serializers

class SerializerNameSerializer(serializers.ModelSerializer):

    class Meta:
        # model = Your_ModelName
        fields = ['id', 'updated_at', 'created_at']
"""
}

getDjangoViewContext() {
echo """from rest_framework import views, permissions, response, status


class ViewNameViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        try:
            # Logic here
            return response.Response(status=status.HTTP_200_OK, data={})
        except Exception as e:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={\"message\": f\"{str(e)}\"})
"""
}

getDjangoAdminContext() {
echo """from django.contrib import admin

class ModelNameAdmin(admin.ModelAdmin):
    list_display = []
    list_per_page = 10
    search_fields = []
"""
}