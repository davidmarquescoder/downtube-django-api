from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from pytubefix import YouTube
import requests

class DowntubeController(APIView):
    def get(self, request):
        video_url = request.query_params.get('video_url')
        download_type = request.query_params.get('download_type', 'default')  #  "144p", "240p", "360p", "480p", "720p", "1080p", ou "audio"

        if not video_url:
            return Response({"error": "A URL do vídeo é obrigatória."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            video_info = self.get_video_info(video_url)

            if 'info' in request.query_params:
                return Response(video_info)

            video_stream, video_title, video_size = self.download(video_url, download_type)

            if not video_stream:
                return Response({"error": "Falha ao processar o vídeo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            response = StreamingHttpResponse(video_stream, content_type='video/mp4' if download_type != 'audio' else 'audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{video_title}.{"mp4" if download_type != "audio" else "mp3"}"'
            response['Content-Length'] = str(video_size)

            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_video_info(self, url):
        video = YouTube(url)
        video_streams = video.streams.filter(file_extension='mp4', resolution='1080p').first()

        resolutions = []

        for stream in video.streams.filter(file_extension='mp4').desc():
            if stream.resolution and stream.resolution not in resolutions:
                resolutions.append(stream.resolution)

        info = {
            "title": video.title,
            "duration": video.length,
            "views": video.views,
            "author": video.author,
            "description": video.description,
            "thumbnail_url": video.thumbnail_url,
            "publish_date": video.publish_date,
            "filesize_mb": video_streams.filesize_mb,
            "file_type": video_streams.mime_type,
            "resolution": video_streams.resolution,
            "resolutions": resolutions,
            "fps": video_streams.fps,
        }

        return info

    def download(self, url, download_type):
        video = YouTube(url)

        # VIDEO
        match(download_type):
            case '144p':
                stream = video.streams.filter(file_extension='mp4', resolution='144p').first()

            case '240p':
                stream = video.streams.filter(file_extension='mp4', resolution='240p').first()

            case '360p':
                stream = video.streams.filter(file_extension='mp4', resolution='360p').first()

            case '480p':
                stream = video.streams.filter(file_extension='mp4', resolution='480p').first()

            case '720p':
                stream = video.streams.filter(file_extension='mp4', resolution='720p').first()

            case '1080p':
                stream = video.streams.filter(file_extension='mp4', resolution='1080p').first()

            # AUDIO
            case 'audio':
                stream = video.streams.get_audio_only()
            
            # SE NÃO
            case _:
                stream = video.streams.get_highest_resolution()

        video_stream = requests.get(stream.url, stream=True)
        video_size = video_stream.headers.get('Content-Length', 0)

        return video_stream.iter_content(chunk_size=8192), video.title, video_size
