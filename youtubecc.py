
DEVELOPER_KEY = "AIzaSyBjqAlGFskJjlZsLwqWZDMln5JoZr09sZY"

import os
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Google Cloud Console에서 받은 API 키와 인증 정보를 사용하여 API에 연결
api_service_name = "youtube"
api_version = "v3"

youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)


# YouTube 동영상의 ID를 추출하는 함수
def extract_video_id(url):
    regex = r"^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.{11})"
    match = re.match(regex, url)
    if match is not None:
        return match.group(1)
    else:
        return None


# 동영상 ID를 가져와서 자막 ID를 가져오는 함수
def get_caption_id(video_id):
    captions = youtube.captions().list(
        part="id,snippet",
        videoId=video_id,
        fields="items(id,snippet(language,trackKind))"
    ).execute()

    for item in captions.get("items", []):
        try:
            if item["snippet"]["language"] == "en":  # 영어 자막이 있는 경우
                return item["id"]
        except KeyError:
            continue

    # 영어 자막이 없는 경우
    return None



# 자막 ID를 사용하여 자막 다운로드하는 함수
def download_caption(caption_id):
    try:
        caption_info = youtube.captions().download(id=caption_id).execute()
        caption = caption_info.decode("utf-8")  # 자막 파일을 문자열로 디코딩
        with open(os.path.join("input", "captions.txt"), "w") as f:  # 텍스트 파일로 저장
            f.write(caption)
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")


# 동영상 URL을 입력 받음
url = input("Enter the YouTube video URL: ")

# 동영상 URL에서 ID 추출
video_id = extract_video_id(url)
if video_id is None:
    print("Invalid YouTube video URL.")
    exit()

# "input" 폴더 생성 및 자막 다운로드
if not os.path.exists("input"):
    os.mkdir("input")
caption_id = get_caption_id(video_id)
if caption_id is None:
    print("There are no English captions available for this video.")
else:
    download_caption(caption_id)
    print("Captions have been downloaded.")
