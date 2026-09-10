#!/usr/bin/env python3
import json, os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
SEOUL = ZoneInfo("Asia/Seoul")
NOW = datetime.now(SEOUL)
DATE_KR = NOW.strftime("%Y년 %m월 %d일")
DATE_KEY = NOW.strftime("%Y-%m-%d")
NAME = "채이"
THEMES = [
    {"emoji": "\U0001f333", "title": "공원에서 놀자!", "subtitle": "미끄럼틀, 그네, 공.", "hint": "park, slide, swing, ball, run, jump, clap, friend"},
    {"emoji": "\U0001f34e", "title": "맛있는 간식!", "subtitle": "사과, 주스, 쿠키.", "hint": "apple, juice, cookie, eat, drink, yummy, please, thank you"},
    {"emoji": "\U0001f9f8", "title": "장난감이랑 놀자!", "subtitle": "곰돌이, 블록, 차.", "hint": "teddy, block, car, toy, build, share, play, clap"},
    {"emoji": "\U0001f3e0", "title": "우리 집에서!", "subtitle": "엄마, 아빨, 문.", "hint": "mom, dad, door, wash, sleep, wave, sit, love"},
    {"emoji": "\U0001f436", "title": "동물 친구들!", "subtitle": "강아지, 고양이, 새.", "hint": "dog, cat, bird, hop, fly, roar, swim, cute"},
    {"emoji": "\U0001f305", "title": "아침이에요!", "subtitle": "이 닥기, 옷 입기.", "hint": "morning, teeth, clothes, shoes, hello, wave, stretch, go"},
    {"emoji": "\u2614", "title": "오늘 날씨는?", "subtitle": "비, 해, 바람.", "hint": "sun, rain, wind, cold, hot, jump, run, coat"},
]
THEME = THEMES[NOW.timetuple().tm_yday % len(THEMES)]
FALLBACK = {
    "date": DATE_KR, "dateKey": DATE_KEY,
    "theme": {"emoji": "\U0001f333", "title": "공원에서 놀자!", "subtitle": "미끄럼틀, 그네, 공."},
    "words": [
        {"en":"park","ko":"공원","emo":"\U0001f333"},{"en":"slide","ko":"미끄럼틀","emo":"\U0001f6dd"},
        {"en":"swing","ko":"그네","emo":"\U0001f3a0"},{"en":"ball","ko":"공","emo":"\u26bd"},
        {"en":"run","ko":"달려","emo":"\U0001f3c3"},{"en":"friend","ko":"친구","emo":"\U0001f467"},
        {"en":"water","ko":"물","emo":"\U0001f4a7"},{"en":"happy","ko":"기뻘","emo":"\U0001f604"},
    ],
    "actions": [
        {"en":"Jump!","ko":"점프!","emo":"\U0001f998"},{"en":"Clap!","ko":"손벽!","emo":"\U0001f44f"},
        {"en":"Run!","ko":"달려!","emo":"\U0001f3c3"},{"en":"Wave!","ko":"손 흔들어!","emo":"\U0001f44b"},
        {"en":"Spin!","ko":"빙글빙글!","emo":"\U0001f4ab"},{"en":"Touch your nose!","ko":"코를 만져!","emo":"\U0001f443"},
        {"en":"Sit down!","ko":"앉아!","emo":"\U0001fa91"},{"en":"Stretch!","ko":"팔 쪽!","emo":"\U0001f646"},
    ],
    "dialogue": [
        {"who":"별이","role":"you","en":"Let's go to the park!","ko":"공원에 가자!"},
        {"who":NAME,"role":"me","en":"Yay! I want to play.","ko":"예이! 나 놀고 싶어."},
        {"who":"별이","role":"you","en":"Slide or swing?","ko":"미끄럼틀이야, 그네야?"},
        {"who":NAME,"role":"me","en":"The slide! It's so big!","ko":"미끄럼틀! 진짜 크다!"},
        {"who":"별이","role":"you","en":"Come on. Let's run!","ko":"자, 달려가자!"},
        {"who":NAME,"role":"me","en":"I'm so happy!","ko":"나 너무 기뻘!"},
    ],
    "quizzes": [
        {"speak":"slide","answer":"slide","options":[{"id":"slide","emo":"\U0001f6dd","label":"slide"},{"id":"ball","emo":"\u26bd","label":"ball"},{"id":"water","emo":"\U0001f4a7","label":"water"}]},
        {"speak":"ball","answer":"ball","options":[{"id":"park","emo":"\U0001f333","label":"park"},{"id":"ball","emo":"\u26bd","label":"ball"},{"id":"swing","emo":"\U0001f3a0","label":"swing"}]},
        {"speak":"I like the swing.","answer":"swing","options":[{"id":"slide","emo":"\U0001f6dd","label":"slide"},{"id":"swing","emo":"\U0001f3a0","label":"swing"},{"id":"run","emo":"\U0001f3c3","label":"run"}]},
        {"speak":"water","answer":"water","options":[{"id":"water","emo":"\U0001f4a7","label":"water"},{"id":"friend","emo":"\U0001f467","label":"friend"},{"id":"happy","emo":"\U0001f604","label":"happy"}]},
        {"speak":"Let's run!","answer":"run","options":[{"id":"sleep","emo":"\U0001f634","label":"sleep"},{"id":"run","emo":"\U0001f3c3","label":"run"},{"id":"eat","emo":"\U0001f36a","label":"eat"}]},
        {"speak":"I'm so happy!","answer":"happy","options":[{"id":"sad","emo":"\U0001f622","label":"sad"},{"id":"happy","emo":"\U0001f604","label":"happy"},{"id":"mad","emo":"\U0001f620","label":"mad"}]},
    ],
}
def validate(data):
    words = data.get("words") or []
    actions = data.get("actions") or []
    dialogue = data.get("dialogue") or []
    quizzes = data.get("quizzes") or []
    if len(words)<8 or len(actions)<6 or len(dialogue)<6 or len(quizzes)<6: raise ValueError("short content")
    for line in dialogue[:6]:
        line["who"] = line.get("who") or (NAME if line.get("role")=="me" else "별이")
        line["role"] = line.get("role") if line.get("role") in ("me","you") else "you"
        if line["who"] in ("쳄이","책이","챙이"): line["who"]=NAME
    data["words"]=words[:8]; data["actions"]=actions[:8]; data["dialogue"]=dialogue[:6]
    data["quizzes"]=[{ "speak":q["speak"], "answer":q["answer"], "options":(q.get("options") or [])[:3]} for q in quizzes[:6]]
    data["date"]=DATE_KR; data["dateKey"]=DATE_KEY
    th=data.get("theme") or {}
    data["theme"]={"emoji":th.get("emoji") or THEME["emoji"],"title":th.get("title") or THEME["title"],"subtitle":th.get("subtitle") or THEME["subtitle"]}
    return data
def ask_gemini(api_key):
    prompt=f"""오늘 {DATE_KR} 테마 {THEME['emoji']} {THEME['title']} 힌트 {THEME['hint']}
6살 {NAME} 몸놀이 영어 JSON만.
words 8, actions 8(Jump Clap Run Wave Spin Sit), dialogue 6, quizzes 6 listen-pick.
"""
    for model in ["gemini-3.5-flash","gemini-2.5-flash","gemini-2.0-flash"]:
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            res=requests.post(url,json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.9,"responseMimeType":"application/json"}},timeout=90)
            data=res.json()
            if "candidates" not in data: continue
            text=data["candidates"][0]["content"]["parts"][0]["text"].strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            return validate(json.loads(text))
        except Exception as e:
            last=str(e)
    raise RuntimeError("gemini failed")
def render(content):
    here=os.path.dirname(os.path.abspath(__file__))
    html=open(os.path.join(here,"template.html"),encoding="utf-8").read()
    html=html.replace("__CONTENT__", json.dumps(content, ensure_ascii=False))
    html=html.replace("쳄이", NAME).replace("책이", NAME).replace("챙이", NAME)
    open(os.path.join(here,"english.html"),"w",encoding="utf-8").write(html)
    print("wrote", content["theme"]["title"], NAME)
def main():
    api_key=os.environ.get("GEMINI_API_KEY","").strip(); content=None
    if api_key:
        try: content=ask_gemini(api_key); print("gemini ok")
        except Exception as e: print("fallback", e)
    if content is None:
        content=FALLBACK; content["date"]=DATE_KR; content["dateKey"]=DATE_KEY
    render(content)
if __name__=="__main__":
    main()
