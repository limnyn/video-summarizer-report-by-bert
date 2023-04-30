# s/w 구조
# 	1. 자막 cc_input 전처리
	
# 	2. 전처리된 자막 cc_output
	
# 	3. cc_output을 bert에 삽입
	
# 	4 bert 결과 bert_output
	
# 	5 bert_output + 질문 -> gpt3.5터보에 삽입
	
# 	6 결과물 result.txt로 저장





import time, os, re, shutil
start_time = time.time()  # 시작 시간 저장

# 자막파일만 data폴더에 넣으면 제목을 추출하고 해당 자막 파일 이름을 cc_input.txt로 변환

# 현재 경로의 input 폴더를 지정합니다.
input_dir = "input"

# input 폴더 내의 모든 파일을 가져옵니다.
files = os.listdir(input_dir)

# txt 파일만 골라냅니다.
txt_files = [file for file in files if file.endswith(".txt")]

# txt 파일이 하나도 없으면 종료합니다.
if not txt_files:
    print("No txt files found in input folder.")
    exit()

# 첫 번째 txt 파일의 제목을 추출합니다.
txt_file = txt_files[0]
title = os.path.splitext(txt_file)[0]
title = re.sub(r"\[[^\]]*\]", "", title)
title = f'"{title}"'
print("title =", title)

# txt 파일을 복사하고 제목을 cc_input.txt로 지정해 input 폴더에 저장합니다.
shutil.copy(os.path.join(input_dir, txt_file), os.path.join(input_dir, "cc_input.txt"))
os.rename(os.path.join(input_dir, "cc_input.txt"), os.path.join(input_dir, f"cc_input.txt"))

# 입력 파일 이름과 출력 파일 이름을 지정합니다.
input_file = "input/cc_input.txt"
output_file = "output/cc_output.txt"

# 입력 파일을 엽니다.
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()
# 불필요한 줄바꿈을 제거합니다.
text = re.sub(r"\n+", " ", text)
# 문장 단위로 줄바꿈을 정리합니다.
text = re.sub(r"([^\n.!?]*(?:[.!?](?![']?\s|$)[^\n.!?]*)*[.!?]['\"]?(?=\s|$))", r"\1\n", text)
# 문장 시작 부분의 이상한 띄어쓰기를 제거합니다.
text = re.sub(r"\n\s+", r"\n", text)
# 대괄호와 대활호 사이의 문자열을 제거합니다.
text = re.sub(r"\[[^\]]*\]|\([^\)]*\)", "", text)
# 괄호 문자열을 제거합니다.
text = re.sub(r"[()\[\]]", "", text)

# 출력 파일을 엽니다.
with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)


from summarizer import Summarizer

body = text #cc_output.txt를 bert에 삽입
# 여기에 프로그램 코드를 작성합니다.
model = Summarizer()
result = model(body, min_length=60)
full = ''.join(result)

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)  # output 폴더가 없으면 생성합니다.
with open(os.path.join(output_dir, "bert_output.txt"), "w") as f:
    f.write(full)
    
end_time = time.time()  # 종료 시간 저장
elapsed_time = end_time - start_time  # 실행 시간 계산
print(f"bert종료 time: {elapsed_time:.4f} seconds")  # 실행 시간 출력

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
    

end_time = time.time()  # 종료 시간 저장
elapsed_time = end_time - start_time  # 실행 시간 계산
print(f"gpt종료 time: {elapsed_time:.4f} seconds")  # 실행 시간 출력



