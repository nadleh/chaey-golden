#!/usr/bin/env python3
# 매일 GitHub Actions가 실행.
# Gemini는 JSON만 만들고, template.html 껍데기에 넣어 english.html을 덮어쓴다.
import json
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

SEOUL = ZoneInfo("Asia/Seoul")
NOW = datetime.now(SEOUL)
DATE_KR = NOW.strftime("%Y년 %m월 %d일")
DATE_KEY = NOW.strftime("%Y-%m-%d")

THEMES = [
    {"emoji": "\U0001f333", "title": "공원에서 놀자!", "subtitle": "미끄럼틀, 그네, 공. 밖에서 뛰어놀아요.", "hint": "park, slide, swing, ball, run, friend, outside, happy"},
    {"emoji": "\U0001f34e", "title": "맛있는 간식!", "subtitle": "배고파요. 사과, 주스, 쿠키를 먹어요.", "hint": "apple, juice, cookie, hungry, yummy, water, please, thank you"},
    {"emoji": "\U0001f9f8", "title": "장난감이랑 놀자!", "subtitle": "곰돌이, 블록, 차. 같이 만들어요.", "hint": "teddy, block, car, toy, share, build, mine, play"},
    {"emoji": "\U0001f3e0", "title": "우리 집에서!", "subtitle": "엄마, 아빨, 동생. 집에 있는 말이에요.", "hint": "mom, dad, baby, home, door, wash, sleep, love"},
    {"emoji": "\U0001f436", "title": "동물 친구들!", "subtitle": "강아지, 고양이, 새. 소리를 내봐요.", "hint": "dog, cat, bird, fish, hop, fly, soft, cute"},
    {"emoji": "\U0001f305", "title": "아침이에요!", "subtitle": "이 닥기, 옷 입기, 안녕. 하루를 시작해요.", "hint": "morning, teeth, clothes, shoes, hello, breakfast, ready, go"},
    {"emoji": "\u2614", "title": "오늘 날씨는?", "subtitle": "비, 해, 바람, 옷. 밖에 나가기 전에 봐요.", "hint": "sun, rain, wind, cold, hot, coat, hat, wow"},
]

THEME = THEMES[NOW.timetuple().tm_yday % len(THEMES)]

FALLBACK = {
    "date": DATE_KR,
    "dateKey": DATE_KEY,
    "theme": {"emoji": "\U0001f333", "title": "공원에서 놀자!", "subtitle": "미끄럼틀, 그네, 공. 밖에서 뛰어놀아요."},
    "words": [
        {"en": "park", "ko": "공원", "emo": "\U0001f333"},
        {"en": "slide", "ko": "미끄럼틀", "emo": "\U0001f6dd"},
        {"en": "swing", "ko": "그네", "emo": "\U0001f3a0"},
        {"en": "ball", "ko": "공", "emo": "\u26bd"},
        {"en": "run", "ko": "달리다", "emo": "\U0001f3c3"},
        {"en": "friend", "ko": "친구", "emo": "\U0001f467"},
        {"en": "water", "ko": "물", "emo": "\U0001f4a7"},
        {"en": "happy", "ko": "기뻘요", "emo": "\U0001f604"},
    ],
    "sentences": [
        {"en": "Let's go to the park!", "ko": "공원에 가자!", "chunks": [["Let's go", "가자"], ["to the park!", "공원에!"]]},
        {"en": "I want to play outside.", "ko": "밖에서 놀고 싶어요.", "chunks": [["I want to", "나는 ~하고 싶어요"], ["play", "놀다"], ["outside.", "밖에서."]]},
        {"en": "Look at the big slide!", "ko": "큰 미끄럼틀 봐!", "chunks": [["Look at", "봐 봐"], ["the big slide!", "큰 미끄럼틀!"]]},
        {"en": "Can I go down?", "ko": "내려가도 돼요?", "chunks": [["Can I", "내가 ~해도 돼?"], ["go down?", "내려가다"]]},
        {"en": "I like the swing.", "ko": "나는 그네가 좋아요.", "chunks": [["I like", "나는 좋아해요"], ["the swing.", "그네를."]]},
        {"en": "Push me, please!", "ko": "밀어 주세요!", "chunks": [["Push me,", "나를 밀어 줘"], ["please!", "부탁해요!"]]},
        {"en": "Let's play with the ball.", "ko": "공으로 같이 놀자.", "chunks": [["Let's play", "같이 놀자"], ["with the ball.", "공으로."]]},
        {"en": "Throw the ball to me!", "ko": "나한테 공을 던져 줘!", "chunks": [["Throw the ball", "공을 던져 줘"], ["to me!", "나한테!"]]},
        {"en": "I can run so fast!", "ko": "나 진짜 빨리 달릴 수 있어요!", "chunks": [["I can run", "나는 달릴 수 있어요"], ["so fast!", "아주 빨리!"]]},
        {"en": "This is my friend.", "ko": "이 아이는 내 친구예요.", "chunks": [["This is", "이 아이는"], ["my friend.", "내 친구예요."]]},
        {"en": "I'm thirsty. I want water.", "ko": "목말라요. 물 먹고 싶어요.", "chunks": [["I'm thirsty.", "목말라요."], ["I want water.", "물 먹고 싶어요."]]},
        {"en": "I'm so happy today!", "ko": "오늘 정말 기뻘요!", "chunks": [["I'm so happy", "정말 기뻘요"], ["today!", "오늘!"]]},
    ],
    "dialogue": [
        {"who": "별이", "role": "you", "en": "Let's go to the park!", "ko": "공원에 가자!"},
        {"who": "쳄이", "role": "me", "en": "Yay! I want to play.", "ko": "예이! 나 놀고 싶어."},
        {"who": "별이", "role": "you", "en": "Slide or swing?", "ko": "미끄럼틀이야, 그네야?"},
        {"who": "쳄이", "role": "me", "en": "The slide! It's so big!", "ko": "미끄럼틀! 진짜 크다!"},
        {"who": "별이", "role": "you", "en": "Come on. Let's run!", "ko": "자, 달려가자!"},
        {"who": "쳄이", "role": "me", "en": "I'm so happy!", "ko": "나 너무 기뻘!"},
    ],
    "quizzes": [
        {"type": "listen-pick", "q": "이 단어는 무엇일까요?", "speak": "slide", "answer": "slide",
         "options": [{"id": "slide", "emo": "\U0001f6dd", "label": "slide"}, {"id": "ball", "emo": "\u26bd", "label": "ball"}, {"id": "water", "emo": "\U0001f4a7", "label": "water"}]},
        {"type": "listen-pick", "q": "지금 들린 말은 어떤 그림일까요?", "speak": "I like the swing.", "answer": "swing",
         "options": [{"id": "slide", "emo": "\U0001f6dd", "label": "slide"}, {"id": "swing", "emo": "\U0001f3a0", "label": "swing"}, {"id": "park", "emo": "\U0001f333", "label": "park"}]},
        {"type": "meaning", "q": "I'm thirsty. 는 무슨 뜻일까요?", "speak": "I'm thirsty.", "answer": "thirsty",
         "options": [{"id": "thirsty", "emo": "\U0001f4a7", "label": "목말라요"}, {"id": "sleepy", "emo": "\U0001f634", "label": "졸려요"}, {"id": "cold", "emo": "\U0001f976", "label": "추워요"}]},
        {"type": "listen-pick", "q": "공을 달라고 하는 말은?", "speak": "Throw the ball to me!", "answer": "ball",
         "options": [{"id": "friend", "emo": "\U0001f467", "label": "friend"}, {"id": "ball", "emo": "\u26bd", "label": "ball"}, {"id": "happy", "emo": "\U0001f604", "label": "happy"}]},
        {"type": "order", "q": "조각을 순서대로 눌러 문장을 만들어요.", "speak": "Let's go to the park!", "pieces": ["Let's go", "to the park!"]},
        {"type": "meaning", "q": "I'm so happy today! 는 무슨 느낌일까요?", "speak": "I'm so happy today!", "answer": "happy",
         "options": [{"id": "sad", "emo": "\U0001f622", "label": "슬퍼요"}, {"id": "happy", "emo": "\U0001f604", "label": "기뻘요"}, {"id": "mad", "emo": "\U0001f620", "label": "화나요"}]},
    ],
}


def normalize_chunks(chunks):
    out = []
    for c in chunks:
        if isinstance(c, (list, tuple)) and len(c) >= 2:
            out.append([str(c[0]), str(c[1])])
        elif isinstance(c, dict):
            out.append([str(c.get("en") or c.get("text") or ""), str(c.get("ko") or c.get("meaning") or "")])
    return out


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("not an object")
    words = data.get("words") or []
    sentences = data.get("sentences") or []
    dialogue = data.get("dialogue") or []
    quizzes = data.get("quizzes") or []
    if len(words) < 8:
        raise ValueError("need 8 words")
    if len(sentences) < 12:
        raise ValueError("need 12 sentences")
    if len(dialogue) < 6:
        raise ValueError("need 6 dialogue lines")
    if len(quizzes) < 6:
        raise ValueError("need 6 quizzes")
    for w in words[:8]:
        if not w.get("en") or not w.get("emo"):
            raise ValueError("bad word")
    for s in sentences[:12]:
        chunks = normalize_chunks(s.get("chunks") or [])
        if not s.get("en") or len(chunks) < 2:
            raise ValueError("bad sentence")
        s["chunks"] = chunks
        s["ko"] = s.get("ko") or ""
    for line in dialogue[:6]:
        if not line.get("en"):
            raise ValueError("bad dialogue")
        line["who"] = line.get("who") or ("쳄이" if line.get("role") == "me" else "별이")
        line["role"] = line.get("role") if line.get("role") in ("me", "you") else "you"
        line["ko"] = line.get("ko") or ""
    data["words"] = words[:8]
    data["sentences"] = sentences[:12]
    data["dialogue"] = dialogue[:6]
    data["quizzes"] = quizzes[:6]
    data["date"] = DATE_KR
    data["dateKey"] = DATE_KEY
    data["theme"] = {
        "emoji": (data.get("theme") or {}).get("emoji") or THEME["emoji"],
        "title": (data.get("theme") or {}).get("title") or THEME["title"],
        "subtitle": (data.get("theme") or {}).get("subtitle") or THEME["subtitle"],
    }
    return data


def ask_gemini(api_key):
    prompt = f"""오늘 날짜: {DATE_KR}
테마: {THEME['emoji']} {THEME['title']}
키워드 힌트: {THEME['hint']}

한국 6살 아이(영어권 4~5살 말투)가 20~30분 영어 놀이할 콘텐츠를 만들어라.
짧고 입으로 나오는 말만. I would like, however, because 같은 긴 절 금지.
Let's / I want / Can I / Look / This is / I'm 위주.

반드시 JSON 객체만 출력. 마크다운 금지.
"""
    models = ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-2.0-flash"]
    last_err = None
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.9, "responseMimeType": "application/json"},
        }
        try:
            res = requests.post(url, json=body, timeout=90)
            data = res.json()
            if "candidates" not in data:
                last_err = f"{model}: {res.text[:400]}"
                print("모델 실패", last_err)
                continue
            text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            parsed = json.loads(text)
            return validate(parsed)
        except Exception as e:
            last_err = f"{model}: {e}"
            print("파싱/요청 실패", last_err)
    raise RuntimeError(last_err or "gemini failed")


def render(content):
    here = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(here, "template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
    if "__CONTENT__" not in html:
        raise RuntimeError("template.html missing __CONTENT__")
    payload = json.dumps(content, ensure_ascii=False)
    html = html.replace("__CONTENT__", payload)
    out = os.path.join(here, "english.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", out, "theme=", content["theme"]["title"])


def main():
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    content = None
    if api_key:
        try:
            content = ask_gemini(api_key)
            print("gemini ok")
        except Exception as e:
            print("gemini fallback:", e)
    else:
        print("no GEMINI_API_KEY, using fallback")
    if content is None:
        content = FALLBACK
        content["date"] = DATE_KR
        content["dateKey"] = DATE_KEY
    render(content)


if __name__ == "__main__":
    main()
