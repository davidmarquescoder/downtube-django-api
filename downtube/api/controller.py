from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from pytubefix import YouTube
import requests

class DowntubeController(APIView):
    def get(self, request):
        video_url = request.query_params.get('video_url')

        if not video_url:
            return Response({"error": "A URL do vídeo é obrigatória."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            video_stream, video_title = self.download(video_url)
            
            if not video_stream:
                return Response({"error": "Falha ao processar o vídeo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            response = StreamingHttpResponse(video_stream, content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename="{video_title}.mp4"'

            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def download(self, url):
        video = YouTube(url).streams.get_highest_resolution()

        # Abre uma requisição para o URL de download do stream do vídeo
        video_stream = requests.get(video.url, stream=True)
        
        # Retorna o fluxo de bytes e o título do vídeo
        return video_stream.iter_content(chunk_size=8192), video.title
