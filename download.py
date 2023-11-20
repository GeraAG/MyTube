from pytube import YouTube

# URL of the video
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# https://www.youtube.com/watch?v=kXYiU_JCYtU

# Create a YouTube object
yt = YouTube(url)

# Get the highest resolution progressive stream
stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

# Download the stream
stream.download()
