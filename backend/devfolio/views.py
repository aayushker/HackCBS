# from .serializers import EncodeSerializers
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from process.scrapper import scrapper
from process.crux import crux
from process.vectorization import vectorization

# Heartbeat request
def Heartbeat(request):
    return JsonResponse({'status': 'Backend is active'})

class Devfolio(APIView):
    def post(self, request, *args, **kwargs):
        projectURL = request.data.get('projectURL') 
        # Call the scrapper function
        if projectURL and projectURL.startswith('https://devfolio.co/projects/'):
            try:
                scrapedData = scrapper(projectURL)
                cruxedData = crux(scrapedData)
                ps_crux_words = ["Self-Driving Software", "Android", "CAN BUS", "ADAS", "ACC", "FCW", "AEB", "LKA", "Neural Network", 
                                 "Cost-Effective", "Accessible", "Beta Testing", "Autonomous Driving", "Optimisation", "Mobile GPU"]
                result = vectorization(ps_crux_words)
                return Response({'status': 'success', 'data': result}, status=200)
            except Exception as e:
                import traceback
                traceback.print_exc()
                return Response({'status': 'error', 'message': f'Error: {e}'}, status=500)
        else:
            return Response({'status': 'error', 'message': 'Invalid URL'}, status=400)