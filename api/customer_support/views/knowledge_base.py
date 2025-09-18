from django.conf import settings
from rest_framework import views, permissions, response, status

from core.models import UserModel
from customer_support.models import CustomerSupportKnowledgeBaseModel, CustomerSupportKnowledgeBaseChunkModel
from customer_support.serializers import KnowledgeBaseSerializer
from ai.utils.open_ai_manager import OpenAIManager

class KnowledgeBaseViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cur_user = UserModel.objects.filter(email="mohammad@teetimegolfpass.com").first()
        self.open_ai_manager = OpenAIManager(model="gpt-4o", api_key=settings.OPEN_AI_SECRET_KEY, cur_users=[cur_user])

    def _rag_progress_callback(self, chunk=None, index=None, total=None, err_msg=None, **kwargs):
        if err_msg:
            print(f"Error on chunk {index}/{total}: {err_msg}")
        else:
            print(f"Processing chunk {index}/{total}...")
    
    def post(self, request, format=None):
        try:
            description = request.data.get("description")
            url = request.data.get("url")
            if url:
                if not description or description.strip() == "" or description.strip() == "null":
                    return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Description is required."})
                cur_knoledge_base = CustomerSupportKnowledgeBaseModel()
                cur_knoledge_base.url = url
                cur_knoledge_base.description = description
                cur_knoledge_base.save()
                chunks = self.open_ai_manager.build_materials_for_rag(text=description, progress_callback=self._rag_progress_callback)
                for index, chunk in enumerate(chunks):
                    print(f"Saving chunk {index+1}/{len(chunks)} to database...")
                    cur_text = chunk['text']
                    cur_embedding = chunk['vector']
                    cur_knoledge_base_chunk = CustomerSupportKnowledgeBaseChunkModel()
                    cur_knoledge_base_chunk.kb = cur_knoledge_base
                    cur_knoledge_base_chunk.chunk_text = cur_text
                    cur_knoledge_base_chunk.embedding = cur_embedding
                    cur_knoledge_base_chunk.save()
                return response.Response(status=status.HTTP_200_OK, data={"success": True})
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "URL is required."})
        except Exception as e:
            print(f"❌ Error occurred: {str(e)}")
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"{str(e)}"})