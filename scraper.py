from pytube import Playlist

def fetch_playlist_videos(playlist_url):
    playlist = Playlist(playlist_url)
    videos = []

    for video in playlist.videos:
        videos.append({"id":video.video_id, "title": video.title})

    return videos
