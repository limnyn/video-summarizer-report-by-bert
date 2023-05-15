# s/w 구조
# 	1. 자막 cc_input 전처리
	
# 	2. 전처리된 자막 cc_output
	
# 	3. cc_output을 bert에 삽입
	
# 	4 bert 결과 bert_output
	
# 	5 bert_output + 질문 -> gpt3.5터보에 삽입
	
# 	6 결과물 result.txt로 저장





import time, os
import cc_to_text, youtubeCCextract
from summarizer import Summarizer


# 1- url을 받아서 영어 자막 다운로드, 제목추출
youtubeCCextract.caption_extract()
start_time = time.time()  # 시작 시간 저장

# 2- 영어 자막 파일 txt파일로 전처리
title, body = cc_to_text.cc_to_txt()

# 3- bert summarizer
model = Summarizer()
result = model(body, min_length=60)
full = ''.join(result)

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)  # output 폴더가 없으면 생성합니다.
with open(os.path.join(output_dir, "bert_output.txt"), "w", encoding='utf-8') as f:
    f.write(full)
end_time = time.time()  
elapsed_time = end_time - start_time  # 
print(f"bert종료 time: {elapsed_time:.4f} seconds")  



# 4- gpt3.5 turbo 사용 -> 한글 설명 생성
import apikey
import openai
openai.api_key = apikey.GPT_KEY

quest = f"User: {title}라는 제목을 가진 영상의 요약 내용인\n[{full}]\n를 읽고 이 영상에 대한 내용을 보고서 형식으로 한글로 써줘"
messages = [{"role":"user", "content": quest}]

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)


chat_response = completion.choices[0].message["content"].strip()
print(f'ChatGPT: {chat_response}')

result_file = os.path.join("output", "result.txt")
with open(result_file, "w", encoding="utf-8") as f:
    f.write(chat_response)
    

end_time = time.time() 
elapsed_time = end_time - start_time  
print(f"gpt종료 time: {elapsed_time:.4f} seconds")  # 실행 시간 출력


