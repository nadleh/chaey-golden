#!/usr/bin/env python3
import json, os, copy
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

SEOUL = ZoneInfo("Asia/Seoul")
NOW = datetime.now(SEOUL)
DATE_KR = NOW.strftime("%Y년 %m월 %d일")
DATE_KEY = NOW.strftime("%Y-%m-%d")
NAME = "채이"

PACKS = [
    {"emoji":"\U0001f333","title":"공원에서 놀자!","subtitle":"미끄럼틀, 그네, 공.","hint":"park slide swing",
     "words":[("park","공원","\U0001f333"),("slide","미끄럼틀","\U0001f6dd"),("swing","그네","\U0001f3a0"),("ball","공","\u26bd"),("tree","나무","\U0001f332"),("flower","꽃","\U0001f338"),("bench","벤치","\U0001fa91"),("sandbox","모래놀이","\U0001f3d6"),("friend","친구","\U0001f467"),("run","달려","\U0001f3c3"),("jump","점프","\U0001f998"),("play","놀자","\U0001f3b2"),("happy","기뻘","\U0001f604"),("water","물","\U0001f4a7"),("bird","새","\U0001f426")]},
    {"emoji":"\U0001f34e","title":"맛있는 간식!","subtitle":"사과, 주스, 쿠키.","hint":"apple juice cookie",
     "words":[("apple","사과","\U0001f34e"),("banana","바나나","\U0001f34c"),("cookie","쿠키","\U0001f36a"),("juice","주스","\U0001f9c3"),("milk","우유","\U0001f95b"),("bread","뻕","\U0001f35e"),("cake","케이크","\U0001f370"),("grape","포도","\U0001f347"),("eat","먹어","\U0001f37d"),("drink","마셔","\U0001f964"),("yummy","맛있어","\U0001f60b"),("please","주세요","\U0001f64f"),("thank you","고마워","\U0001f49d"),("hungry","배고파","\U0001f97a"),("more","더","\u2795")]},
    {"emoji":"\U0001f9f8","title":"장난감이랑 놀자!","subtitle":"곰돌이, 블록, 차.","hint":"teddy block car",
     "words":[("teddy","곰돌이","\U0001f9f8"),("block","블록","\U0001f9f1"),("car","차","\U0001f697"),("doll","인형","\U0001f38e"),("ball","공","\u26bd"),("train","기차","\U0001f682"),("plane","비행기","\u2708"),("robot","로봇","\U0001f916"),("toy","장난감","\U0001f3b2"),("build","만들어","\U0001f528"),("share","나눠 써","\U0001f91d"),("play","놀자","\U0001f3ae"),("mine","내 거야","\U0001f446"),("yours","네 거야","\U0001f448"),("fun","재미있어","\U0001f606")]},
    {"emoji":"\U0001f3e0","title":"우리 집에서!","subtitle":"엄마, 아빨, 문.","hint":"mom dad home",
     "words":[("mom","엄마","\U0001f469"),("dad","아빨","\U0001f468"),("baby","아기","\U0001f476"),("home","집","\U0001f3e0"),("door","문","\U0001f6aa"),("window","창문","\U0001fa9f"),("table","테이블","\U0001fab5"),("chair","의자","\U0001fa91"),("bed","침대","\U0001f6cf"),("wash","손 쌎어","\U0001f9fc"),("sleep","자자","\U0001f634"),("love","사랑해","\u2764"),("hug","안아줘","\U0001f917"),("light","불","\U0001f4a1"),("room","방","\U0001f3e1")]},
    {"emoji":"\U0001f436","title":"동물 친구들!","subtitle":"강아지, 고양이, 새.","hint":"dog cat bird",
     "words":[("dog","강아지","\U0001f436"),("cat","고양이","\U0001f431"),("bird","새","\U0001f426"),("fish","물고기","\U0001f41f"),("rabbit","토끼","\U0001f430"),("bear","곰","\U0001f43b"),("lion","사자","\U0001f981"),("duck","오리","\U0001f986"),("hop","폴짝","\U0001f430"),("fly","날아","\U0001f985"),("swim","헤엄","\U0001f3ca"),("roar","어흥","\U0001f981"),("cute","귀여워","\U0001f970"),("soft","부드러워","\U0001f9f6"),("pet","쓰담","\u270b")]},
    {"emoji":"\U0001f305","title":"아침이에요!","subtitle":"이 닥기, 옷 입기.","hint":"morning teeth shoes",
     "words":[("morning","아침","\U0001f305"),("hello","안녕","\U0001f44b"),("teeth","이","\U0001f9b7"),("brush","닥아","\U0001faa5"),("clothes","옷","\U0001f455"),("shirt","셔츠","\U0001f45a"),("pants","바지","\U0001f456"),("socks","양말","\U0001f9e6"),("shoes","신발","\U0001f45f"),("breakfast","아침밥","\U0001f35a"),("ready","준비","\U0001f4aa"),("go","가자","\U0001f6b6"),("bag","가방","\U0001f392"),("school","학교","\U0001f3eb"),("bye","잘 가","\U0001f44b")]},
    {"emoji":"\u2614","title":"오늘 날씨는?","subtitle":"비, 해, 바람.","hint":"sun rain wind",
     "words":[("sun","해","\u2600"),("rain","비","\u2614"),("wind","바람","\U0001f4a8"),("cloud","구름","\u2601"),("snow","눈","\u2744"),("hot","더워","\U0001f975"),("cold","추워","\U0001f976"),("coat","코트","\U0001f9e5"),("hat","모자","\U0001f3a9"),("umbrella","우산","\u2602"),("boots","장화","\U0001f97e"),("wow","우와","\U0001f62e"),("wet","축축","\U0001f4a6"),("dry","말라","\U0001f324"),("sky","하늘","\U0001f30c")]},
    {"emoji":"\U0001f6c1","title":"목욕 시간!","subtitle":"물, 비누, 수건.","hint":"bath soap towel",
     "words":[("bath","목욕","\U0001f6c1"),("water","물","\U0001f4a7"),("soap","비누","\U0001f9fc"),("towel","수건","\U0001f9fb"),("duck","오리","\U0001f986"),("splash","첨병","\U0001f92f"),("clean","깨끗","\U0001f9fd"),("warm","따뜻","\U0001f525"),("bubbles","거품","\U0001fae7"),("wash","쌎어","\U0001f64c"),("hair","머리","\U0001f487"),("face","얼굴","\U0001f60a"),("hands","손","\U0001f450"),("dry","닥아","\U0001f32c"),("done","다 했어","\u2705")]},
    {"emoji":"\U0001f68c","title":"밖에 나가자!","subtitle":"버스, 가게, 안녕.","hint":"bus shop walk",
     "words":[("bus","버스","\U0001f68c"),("car","차","\U0001f697"),("shop","가게","\U0001f3ea"),("walk","걸어","\U0001f6b6"),("stop","먼춰","\U0001f6d1"),("bag","가방","\U0001f45c"),("hello","안녕","\U0001f44b"),("big","커","\U0001f4cf"),("small","작아","\U0001f50e"),("go","가자","\U0001f3c3"),("wait","기다려","\u23f3"),("look","봐","\U0001f440"),("street","거리","\U0001f6e3"),("light","신호등","\U0001f6a6"),("home","집","\U0001f3e0")]},
    {"emoji":"\U0001f3a8","title":"그림 그리자!","subtitle":"색, 종이, 별.","hint":"draw red blue",
     "words":[("draw","그려","\u270f"),("crayon","크레용","\U0001f58d"),("paper","종이","\U0001f4c4"),("red","빨강","\U0001f534"),("blue","파랑","\U0001f535"),("yellow","노랑","\U0001f7e1"),("green","초록","\U0001f7e2"),("circle","동그라미","\u2b55"),("star","별","\u2b50"),("heart","하트","\U0001f497"),("pretty","예쁘","\U0001f338"),("color","색칠","\U0001f3a8"),("picture","그림","\U0001f5bc"),("big","크게","\u2b1b"),("small","작게","\u25ab")]},
    {"emoji":"\U0001f3b5","title":"노래 불러!","subtitle":"노래, 손벽, 춤.","hint":"sing clap dance",
     "words":[("sing","노래","\U0001f3a4"),("song","노래","\U0001f3b5"),("clap","손벽","\U0001f44f"),("dance","춤춰","\U0001f483"),("loud","크게","\U0001f50a"),("quiet","조용히","\U0001f507"),("happy","기뻘","\U0001f604"),("again","다시","\U0001f504"),("music","음악","\U0001f3b6"),("drum","북","\U0001f941"),("piano","피아노","\U0001f3b9"),("fast","빨리","\u26a1"),("slow","천천히","\U0001f422"),("smile","웃어","\U0001f601"),("fun","재미있어","\U0001f389")]},
    {"emoji":"\U0001f963","title":"주방 돕자!","subtitle":"사과, 바나나, 그릇.","hint":"help mix bowl",
     "words":[("help","돔와","\U0001f91d"),("mix","섞어","\U0001f958"),("bowl","그릇","\U0001f963"),("spoon","숭가락","\U0001f944"),("fork","포크","\U0001f374"),("plate","접시","\U0001f37d"),("banana","바나나","\U0001f34c"),("apple","사과","\U0001f34e"),("milk","우유","\U0001f95b"),("stir","저어","\U0001f373"),("wash","쌎어","\U0001f9fc"),("cut","잘라","\U0001f52a"),("yummy","맛있어","\U0001f60b"),("please","주세요","\U0001f64f"),("done","다 됐어","\u2705")]},
    {"emoji":"\U0001f319","title":"밤 인사!","subtitle":"달, 별, 잠자.","hint":"night moon star",
     "words":[("night","밤","\U0001f319"),("moon","달","\U0001f31d"),("star","별","\u2b50"),("pajama","잠옷","\U0001f9ba"),("bed","침대","\U0001f6cf"),("pillow","베개","\U0001f6cf"),("hug","안아","\U0001f917"),("sleep","자자","\U0001f634"),("soft","부드러워","\U0001f9f8"),("dark","어두워","\U0001f311"),("light","불","\U0001f4a1"),("story","이야기","\U0001f4d6"),("kiss","뽀뽀","\U0001f618"),("love","사랑해","\u2764"),("good night","잘 자","\U0001f31c")]},
    {"emoji":"\U0001f455","title":"옷 입자!","subtitle":"셔츠, 바지, 양말.","hint":"shirt pants socks",
     "words":[("shirt","셔츠","\U0001f455"),("pants","바지","\U0001f456"),("socks","양말","\U0001f9e6"),("shoes","신발","\U0001f45f"),("hat","모자","\U0001f3a9"),("coat","코트","\U0001f9e5"),("on","입어","\U0001f446"),("off","벗어","\U0001f447"),("fast","빨리","\U0001f3c3"),("slow","천천히","\U0001f422"),("yes","응","\U0001f44d"),("no","아니","\U0001f44e"),("blue","파랑","\U0001f535"),("red","빨강","\U0001f534"),("clean","깨끗","\u2728")]},
]

def to_words(pairs):
    return [{"en":e,"ko":k,"emo":m} for e,k,m in pairs]

def quizzes_from(words):
    out=[]
    for i,w in enumerate(words[:8]):
        others=[x for x in words if x["en"]!=w["en"]]
        opts=[{"id":w["en"],"emo":w["emo"],"label":w["en"]}]
        for x in others[i%max(1,len(others)):]+others:
            if x["en"]==w["en"]: continue
            opts.append({"id":x["en"],"emo":x["emo"],"label":x["en"]})
            if len(opts)==3: break
        out.append({"speak":w["en"],"answer":w["en"],"options":opts})
    return out

def dialogue_from(pack, words):
    a,b,c = words[0], words[1], words[2]
    return [
        {"who":"별이","role":"you","en":f"Look! A {a['en']}!","ko":f"{a['ko']} 봐!"},
        {"who":NAME,"role":"me","en":f"Wow, {a['en']}!","ko":f"우와, {a['ko']}!"},
        {"who":"별이","role":"you","en":f"{b['en']} or {c['en']}?","ko":f"{b['ko']}이야, {c['ko']}이야?"},
        {"who":NAME,"role":"me","en":f"The {b['en']}!","ko":f"{b['ko']}!"},
        {"who":"별이","role":"you","en":f"Say {c['en']}.","ko":f"{c['en']} 말해 봐."},
        {"who":NAME,"role":"me","en":f"{c['en']}!","ko":f"{c['ko']}!"},
    ]

THEME = PACKS[NOW.timetuple().tm_yday % len(PACKS)]

def pack_content(pack):
    words=to_words(pack["words"])
    return {"date":DATE_KR,"dateKey":DATE_KEY,"theme":{"emoji":pack["emoji"],"title":pack["title"],"subtitle":pack["subtitle"]},"words":words,"dialogue":dialogue_from(pack, words),"quizzes":quizzes_from(words)}

def validate(data):
    words=data.get("words") or []
    quizzes=data.get("quizzes") or []
    dialogue=data.get("dialogue") or []
    if len(words)<15: raise ValueError("need 15 words")
    if len(quizzes)<8: quizzes=quizzes_from(words)
    if len(dialogue)<4: dialogue=dialogue_from(THEME, words)
    for line in dialogue[:6]:
        line["who"]=line.get("who") or (NAME if line.get("role")=="me" else "별이")
        line["role"]=line.get("role") if line.get("role") in ("me","you") else "you"
        if line["who"] in ("쳄이","책이","챙이"): line["who"]=NAME
    data["words"]=words[:15]
    data["quizzes"]=[{ "speak":q["speak"], "answer":q["answer"], "options":(q.get("options") or [])[:3]} for q in quizzes[:8]]
    data["dialogue"]=dialogue[:6]
    data["date"]=DATE_KR; data["dateKey"]=DATE_KEY
    data["theme"]={"emoji":THEME["emoji"],"title":THEME["title"],"subtitle":THEME["subtitle"]}
    return data

def ask_gemini(api_key):
    hint=", ".join(e for e,_,_ in THEME["words"])
    prompt=f"""오늘 {DATE_KR}
테마 {THEME['emoji']} {THEME['title']}
단어 힌트: {hint}
6살 {NAME} 영어 JSON만. 단어 15개. Stretch/Jump/Clap 몸명령 금지.
"""
    last="no"
    for model in ["gemini-2.5-flash","gemini-2.0-flash","gemini-flash-latest"]:
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            res=requests.post(url,json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.7,"responseMimeType":"application/json"}},timeout=90)
            data=res.json()
            if "candidates" not in data:
                last=f"{model}:{res.text[:160]}"; continue
            text=data["candidates"][0]["content"]["parts"][0]["text"].strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            return validate(json.loads(text))
        except Exception as e:
            last=f"{model}:{e}"
    raise RuntimeError(last)

def render(content):
    here=os.path.dirname(os.path.abspath(__file__))
    html=open(os.path.join(here,"template.html"),encoding="utf-8").read()
    html=html.replace("__CONTENT__", json.dumps(content, ensure_ascii=False))
    html=html.replace("쳄이",NAME).replace("책이",NAME).replace("챙이",NAME)
    open(os.path.join(here,"english.html"),"w",encoding="utf-8").write(html)
    print("wrote", content["theme"]["title"], len(content["words"]), content["words"][0]["en"], NAME)

def main():
    api_key=os.environ.get("GEMINI_API_KEY","").strip(); content=None
    if api_key:
        try:
            content=ask_gemini(api_key); print("gemini ok")
        except Exception as e:
            print("gemini fallback:", e)
    if content is None:
        content=pack_content(THEME)
    render(content)

if __name__=="__main__":
    main()
