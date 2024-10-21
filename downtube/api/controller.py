from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from pytubefix import YouTube
import requests

class DowntubeController(APIView):
    def get(self, request):
        video_url = request.query_params.get('video_url')
        download_type = request.query_params.get('download_type', 'high')  # 'high', 'low', ou 'audio'

        if not video_url:
            return Response({"error": "A URL do vídeo é obrigatória."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            video_info = self.get_video_info(video_url)
            
            if 'info' in request.query_params:
                return Response(video_info)

            video_stream, video_title = self.download(video_url, download_type)

            if not video_stream:
                return Response({"error": "Falha ao processar o vídeo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            response = StreamingHttpResponse(video_stream, content_type='video/mp4' if download_type != 'audio' else 'audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{video_title}.{"mp4" if download_type != "audio" else "mp3"}"'

            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_video_info(self, url):
        video = YouTube(url)

        info = {
            "title": video.title,
            "duration": video.length,
            "views": video.views,
            "author": video.author,
            "description": video.description,
            "thumbnail_url": video.thumbnail_url
        }

        return info

    def download(self, url, download_type):
        video = YouTube(url)

        if download_type == 'low':
            stream = video.streams.get_lowest_resolution()
        elif download_type == 'audio':
            stream = video.streams.get_audio_only()
        else:
            stream = video.streams.get_highest_resolution()

        video_stream = requests.get(stream.url, stream=True)

        return video_stream.iter_content(chunk_size=8192), video.title
