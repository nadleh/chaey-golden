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
    {
        "emoji": "🌳",
        "title": "공원에서 놀자!",
        "subtitle": "미끄럼틀, 그네, 공. 밖에서 뛰어놀아요.",
        "hint": "park, slide, swing, ball, run, friend, outside, happy",
    },
    {
        "emoji": "🍎",
        "title": "맛있는 간식!",
        "subtitle": "배고파요. 사과, 주스, 쿠키를 먹어요.",
        "hint": "apple, juice, cookie, hungry, yummy, water, please, thank you",
    },
    {
        "emoji": "🧸",
        "title": "장난감이랑 놀자!",
        "subtitle": "곰돌이, 블록, 차. 같이 만들어요.",
        "hint": "teddy, block, car, toy, share, build, mine, play",
    },
    {
        "emoji": "🏠",
        "title": "우리 집에서!",
        "subtitle": "엄마, 아빠, 동생. 집에 있는 말이에요.",
        "hint": "mom, dad, baby, home, door, wash, sleep, love",
    },
    {
        "emoji": "🐶",
        "title": "동물 친구들!",
        "subtitle": "강아지, 고양이, 새. 소리를 내봐요.",
        "hint": "dog, cat, bird, fish, hop, fly, soft, cute",
    },
    {
        "emoji": "🌅",
        "title": "아침이에요!",
        "subtitle": "이 닮기, 옷 입기, 안녕. 하루를 시작해요.",
        "hint": "morning, teeth, clothes, shoes, hello, breakfast, ready, go",
    },
    {
        "emoji": "☔",
        "title": "오늘 날씨는?",
        "subtitle": "비, 해, 바람, 옷. 밖에 나가기 전에 봐요.",
        "hint": "sun, rain, wind, cold, hot, coat, hat, wow",
    },
]

THEME = THEMES[NOW.timetuple().tm_yday % len(THEMES)]
