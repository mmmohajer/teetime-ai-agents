from rest_framework import views, permissions, response, status
from rest_framework.parsers import JSONParser, FormParser

from customer_support.utils.teetime_agent_manager import TeeTimeSupportAgent

class CustomerSupportViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, FormParser]

    def post(self, request, format=None):
        try:
            session_id = (request.data.get("session_id") or "").strip()
            user_message = (request.data.get("user_message") or "").strip()
            if not session_id:
                return response.Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"bot_message": "Missing session_id."},
                )
            teetime_agent = TeeTimeSupportAgent(session_id=session_id)
            if user_message:
                teetime_agent._append_to_history({"role": "user", "content": user_message})
            result = teetime_agent.run_once()
            final = result.get("response", {})
            bot_message = final.get("message_to_user") or "Sorry—something went wrong."
            return response.Response(status=status.HTTP_200_OK, data={"bot_message": bot_message})
        except Exception as e:
            print(e)
            return response.Response(
                status=status.HTTP_200_OK,
                data={
                    "bot_message": (
                        "I’m sorry, I couldn’t process that just now. "
                        "Would you like me to try a different phrasing, or connect you with a human agent (Mon–Fri, 9am–5pm ET)?"
                    )
                },
            )
