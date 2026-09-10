import os
import requests
import re
from datetime import datetime
import pytz

# 구글 패키지 충돌을 방지하기 위해 직접 API를 호출하는 튼튼한 방식입니다.
API_KEY = os.environ.get("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

kr_time = datetime.now(pytz.timezone('Asia/Seoul')).strftime("%Y년 %m월 %d일")

prompt = """
초등학생 아이가 영어 끊어 읽기를 연습하려고 합니다. 
매일 일상에서 자주 쓰는 새로운 영어 문장 1개를 만들어주고, 의미 단위로 3부분으로 끊어주세요.
반드시 아래와 같은 형식으로만 답변하세요. 다른 말은 절대 추가하지 마세요.

원본: I would like to go to the park.
조각1: I
조각2: would like to
조각3: go to the park.
"""

headers = {'Content-Type': 'application/json'}
data = {"contents": [{"parts": [{"text": prompt}]}]}

# API 호출
response = requests.post(url, headers=headers, json=data)
result_text = response.json()['candidates'][0]['content']['parts'][0]['text']

# 정규식으로 더 안전하게 텍스트 추출
original = re.search(r'원본:\s*(.*)', result_text).group(1).strip()
chunk1 = re.search(r'조각1:\s*(.*)', result_text).group(1).strip()
chunk2 = re.search(r'조각2:\s*(.*)', result_text).group(1).strip()
chunk3 = re.search(r'조각3:\s*(.*)', result_text).group(1).strip()

html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>오늘의 끊어 읽기 🌟</title>
    <style>
        body {{ font-family: 'Comic Sans MS', sans-serif; text-align: center; margin-top: 10vh; background-color: #f4f9f4; }}
        .card {{ background: white; padding: 50px; border-radius: 25px; display: inline-block; box-shadow: 0 10px 20px rgba(0,0,0,0.05); max-width: 90%; }}
        .sentence {{ font-size: 2.5em; margin: 30px 0; color: #34495e; font-weight: bold; }}
        .chunked {{ font-size: 2.5em; display: none; margin-top: 30px; font-weight: bold; }}
        .chunk-1 {{ color: #e74c3c; }} .chunk-2 {{ color: #2980b9; }} .chunk-3 {{ color: #27ae60; }}
        .slash {{ color: #bdc3c7; margin: 0 15px; }}
        button {{ font-size: 1.5em; padding: 15px 30px; background-color: #f39c12; color: white; border: none; border-radius: 15px; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>{kr_time} 오늘의 문장 🌟</h1>
        <div class="sentence" id="original">{original}</div>
        <button onclick="document.getElementById('original').style.display='none'; document.getElementById('chunked').style.display='block';">어떻게 끊어 읽을까?</button>
        <div class="chunked" id="chunked">
            <span class="chunk-1">{chunk1}</span> <span class="slash">/</span> 
            <span class="chunk-2">{chunk2}</span> <span class="slash">/</span> 
            <span class="chunk-3">{chunk3}</span>
        </div>
    </div>
</body>
</html>
"""

# HTML 파일 저장
with open("english.html", "w", encoding="utf-8") as file:
    file.write(html_content)
