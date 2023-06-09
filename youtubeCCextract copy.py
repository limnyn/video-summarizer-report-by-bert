# https://www.geeksforgeeks.org/python-downloading-captions-from-youtube/

# https://youtu.be/SW14tOda_kI
import re, os, requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
import codecs


# url = "https://www.youtube.com/watch?v=6_cFlt368XM"
def caption_extract():
    url = input("Enter the url of the video: ")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("meta", property="og:title")["content"]
    # print(title)
    # title 변수에 특수 문자가 있는지 확인합니다.
    # video_id = '6_cFlt368XM'
    video_id = re.search(r'(?<=v=)[\w-]+', url).group(0)

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # iterate over all available transcripts
    for transcript in transcript_list:
        # if transcript.language_code == 'ko':
        if transcript.language_code == 'en':
            text_list = [line['text'] for line in transcript.fetch()]
            # print(text_list)
        else:
            text_list = [line['text'] for line in transcript.translate('en').fetch()]
            # print(text_list)




    if not os.path.exists('input'):
        os.makedirs('input')

    with open('input/input.txt', 'w', encoding='utf-8') as f:
        f.write(f"{title}\n")
        f.write('\n'.join(text_list))
    