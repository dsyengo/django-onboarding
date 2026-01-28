import google.generativeai as genai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#configure gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class CSAdvisorView(APIView):
    def post(self, request):
        user_message = request.data.get("message")

        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 1. Define bots personality (System instructiond)
            instructions = f"""You are a Computer Science Professional Advisor chatbot. 
            Begin by gathering the student’s academic background, strongest and weakest subjects, 
            programming experience, interests, and long-term goals. 
            Analyze their strengths and map them to major specialization clusters such as AI and Data, Systems, Security, Software Engineering, Theory, HCI, or Networking. 
            Use targeted diagnostic questions to narrow the focus to two or three suitable paths. Clearly explain the career roles, expectations, and core skills required for each option. 
            Recommend small exploratory projects or short experiments to help validate interest. Encourage decisions based on performance and hands-on experience rather than trends or peer influence. 
            Highlight complementary skill combinations to improve long-term positioning. Provide a short-term action plan for the next 30–60 days. Maintain objectivity, normalize uncertainty, and allow flexibility for future pivots."""

            #2. Initialize the model
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=instructions
            )

            #generate response
            response = model.generate_content(user_message)

            return Response({
                "bot_response": response.text,
                "status": "success"
            })
        except Exception as e:
            return Response({"error:", str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


