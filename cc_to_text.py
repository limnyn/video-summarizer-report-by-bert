import os, re

def cc_to_txt():
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

    # 출력 파일 이름 지정
    output_file = "output/cc_output.txt"


    if not os.path.exists('input'):
        os.makedirs('input')

    with open('input/input.txt', 'r', encoding='utf-8') as f:
        title = f.readline().strip()
        text = f.read().strip()

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
    return title, text

