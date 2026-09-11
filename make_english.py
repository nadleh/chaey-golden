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

def W(en, ko, emo):
    return {"en": en, "ko": ko, "emo": emo}

def A(en, ko, emo):
    return {"en": en, "ko": ko, "emo": emo}

def L(who, role, en, ko):
    return {"who": who, "role": role, "en": en, "ko": ko}

def Q(speak, answer, opts):
    return {"speak": speak, "answer": answer, "options": opts}

def O(i, emo, label):
    return {"id": i, "emo": emo, "label": label}

PACKS = [
    {
        "emoji": "\U0001f333", "title": "공원에서 놀자!", "subtitle": "미끄럼틀, 그네, 공.",
        "hint": "park slide swing ball run jump",
        "words": [W("park","공원","\U0001f333"),W("slide","미끄럼틀","\U0001f6dd"),W("swing","그네","\U0001f3a0"),W("ball","공","\u26bd"),W("run","달려","\U0001f3c3"),W("friend","친구","\U0001f467"),W("tree","나무","\U0001f333"),W("happy","기뻘","\U0001f604")],
        "dialogue": [
            L("별이","you","Let's go to the park!","공원에 가자!"),
            L(NAME,"me","Yay! I want to play.","예이! 나 놀고 싶어."),
            L("별이","you","Slide or swing?","미끄럼틀이야, 그네야?"),
            L(NAME,"me","The slide! It's so big!","미끄럼틀! 진짜 크다!"),
            L("별이","you","Come on. Let's run!","자, 달려가자!"),
            L(NAME,"me","I'm so happy!","나 너무 기뻘!"),
        ],
        "quizzes": [
            Q("slide","slide",[O("slide","\U0001f6dd","slide"),O("ball","\u26bd","ball"),O("tree","\U0001f333","tree")]),
            Q("ball","ball",[O("park","\U0001f333","park"),O("ball","\u26bd","ball"),O("swing","\U0001f3a0","swing")]),
            Q("I like the swing.","swing",[O("slide","\U0001f6dd","slide"),O("swing","\U0001f3a0","swing"),O("run","\U0001f3c3","run")]),
            Q("Let's run!","run",[O("sleep","\U0001f634","sleep"),O("run","\U0001f3c3","run"),O("eat","\U0001f36a","eat")]),
            Q("friend","friend",[O("friend","\U0001f467","friend"),O("ball","\u26bd","ball"),O("tree","\U0001f333","tree")]),
            Q("I'm so happy!","happy",[O("sad","\U0001f622","sad"),O("happy","\U0001f604","happy"),O("mad","\U0001f620","mad")]),
        ],
    },
    {
        "emoji": "\U0001f34e", "title": "맛있는 간식!", "subtitle": "사과, 주스, 쿠키.",
        "hint": "apple juice cookie eat drink yummy",
        "words": [W("apple","사과","\U0001f34e"),W("juice","주스","\U0001f964"),W("cookie","쿠키","\U0001f36a"),W("banana","바나나","\U0001f34c"),W("eat","먹어","\U0001f37d"),W("drink","마셔","\U0001f964"),W("yummy","맛있어","\U0001f60b"),W("please","좋아요","\U0001f64f")],
        "dialogue": [
            L("별이","you","Are you hungry?","배고파?"),
            L(NAME,"me","Yes! I want an apple.","응! 사과 먹고 싶어."),
            L("별이","you","Apple or cookie?","사과야, 쿠키야?"),
            L(NAME,"me","Cookie, please!","쿠키 주세요!"),
            L("별이","you","Here is juice.","주스 여기 있어."),
            L(NAME,"me","Yummy! Thank you.","맛있다! 고마워."),
        ],
        "quizzes": [
            Q("apple","apple",[O("apple","\U0001f34e","apple"),O("cookie","\U0001f36a","cookie"),O("juice","\U0001f964","juice")]),
            Q("cookie","cookie",[O("banana","\U0001f34c","banana"),O("cookie","\U0001f36a","cookie"),O("apple","\U0001f34e","apple")]),
            Q("I want juice.","juice",[O("juice","\U0001f964","juice"),O("eat","\U0001f37d","eat"),O("please","\U0001f64f","please")]),
            Q("banana","banana",[O("apple","\U0001f34e","apple"),O("banana","\U0001f34c","banana"),O("cookie","\U0001f36a","cookie")]),
            Q("Yummy!","yummy",[O("yummy","\U0001f60b","yummy"),O("sad","\U0001f622","sad"),O("sleep","\U0001f634","sleep")]),
            Q("Cookie, please!","please",[O("run","\U0001f3c3","run"),O("please","\U0001f64f","please"),O("jump","\U0001f998","jump")]),
        ],
    },
    {
        "emoji": "\U0001f9f8", "title": "장난감이랑 놀자!", "subtitle": "곰돌이, 블록, 차.",
        "hint": "teddy block car toy build share",
        "words": [W("teddy","곰돌이","\U0001f9f8"),W("block","블록","\U0001f9f1"),W("car","차","\U0001f697"),W("doll","인형","\U0001f9f8"),W("build","만들어","\U0001f528"),W("share","나눠 써","\U0001f91d"),W("toy","장난감","\U0001f3b2"),W("play","놀자","\U0001f3ae")],
        "dialogue": [
            L("별이","you","Let's play with toys!","장난감이랑 놀자!"),
            L(NAME,"me","My teddy!","내 곰돌이!"),
            L("별이","you","Can we share?","같이 놀아도 돼?"),
            L(NAME,"me","Yes. Build a car!","응. 차 만들자!"),
            L("별이","you","Wow, so cool!","우와, 멋지다!"),
            L(NAME,"me","I like my toys.","내 장난감 좋아."),
        ],
        "quizzes": [
            Q("teddy","teddy",[O("teddy","\U0001f9f8","teddy"),O("car","\U0001f697","car"),O("block","\U0001f9f1","block")]),
            Q("car","car",[O("doll","\U0001f9f8","doll"),O("car","\U0001f697","car"),O("toy","\U0001f3b2","toy")]),
            Q("Let's build.","build",[O("build","\U0001f528","build"),O("sleep","\U0001f634","sleep"),O("eat","\U0001f36a","eat")]),
            Q("block","block",[O("block","\U0001f9f1","block"),O("teddy","\U0001f9f8","teddy"),O("car","\U0001f697","car")]),
            Q("Share, please.","share",[O("share","\U0001f91d","share"),O("run","\U0001f3c3","run"),O("jump","\U0001f998","jump")]),
            Q("I like my toys.","toy",[O("toy","\U0001f3b2","toy"),O("apple","\U0001f34e","apple"),O("rain","\u2614","rain")]),
        ],
    },
    {
        "emoji": "\U0001f3e0", "title": "우리 집에서!", "subtitle": "엄마, 아빨, 문.",
        "hint": "mom dad door wash sleep love",
        "words": [W("mom","엄마","\U0001f469"),W("dad","아빨","\U0001f468"),W("home","집","\U0001f3e0"),W("door","문","\U0001f6aa"),W("wash","손 써","\U0001f9fc"),W("sleep","자","\U0001f634"),W("bed","침대","\U0001f6cf"),W("love","사랑","\u2764")],
        "dialogue": [
            L("별이","you","Welcome home!","집에 왔어!"),
            L(NAME,"me","Hi, Mom!","엄마, 안녕!"),
            L("별이","you","Wash your hands.","손 써자."),
            L(NAME,"me","Okay. Wash, wash!","응. 썩썩!"),
            L("별이","you","Time for bed.","자 시간이야."),
            L(NAME,"me","I love you.","사랑해."),
        ],
        "quizzes": [
            Q("mom","mom",[O("mom","\U0001f469","mom"),O("dad","\U0001f468","dad"),O("bed","\U0001f6cf","bed")]),
            Q("Wash your hands.","wash",[O("sleep","\U0001f634","sleep"),O("wash","\U0001f9fc","wash"),O("run","\U0001f3c3","run")]),
            Q("door","door",[O("door","\U0001f6aa","door"),O("home","\U0001f3e0","home"),O("bed","\U0001f6cf","bed")]),
            Q("I love you.","love",[O("love","\u2764","love"),O("sad","\U0001f622","sad"),O("car","\U0001f697","car")]),
            Q("bed","bed",[O("door","\U0001f6aa","door"),O("bed","\U0001f6cf","bed"),O("mom","\U0001f469","mom")]),
            Q("Time for bed.","sleep",[O("sleep","\U0001f634","sleep"),O("eat","\U0001f36a","eat"),O("play","\U0001f3ae","play")]),
        ],
    },
    {
        "emoji": "\U0001f436", "title": "동물 친구들!", "subtitle": "강아지, 고양이, 새.",
        "hint": "dog cat bird hop fly roar",
        "words": [W("dog","강아지","\U0001f436"),W("cat","고양이","\U0001f431"),W("bird","새","\U0001f426"),W("fish","물고기","\U0001f41f"),W("hop","휙휙","\U0001f430"),W("fly","날아","\U0001f985"),W("roar","어흥","\U0001f981"),W("cute","귀여워","\U0001f970")],
        "dialogue": [
            L("별이","you","Look at the dog!","강아지 봐!"),
            L(NAME,"me","Woof woof!","멍멍!"),
            L("별이","you","The cat is soft.","고양이는 부드러워."),
            L(NAME,"me","Meow. So cute!","야옹. 귀여워!"),
            L("별이","you","Can the bird fly?","새는 날 수 있어?"),
            L(NAME,"me","Yes! Fly, bird!","응! 새야, 날아!"),
        ],
        "quizzes": [
            Q("dog","dog",[O("dog","\U0001f436","dog"),O("cat","\U0001f431","cat"),O("bird","\U0001f426","bird")]),
            Q("Meow.","cat",[O("fish","\U0001f41f","fish"),O("cat","\U0001f431","cat"),O("dog","\U0001f436","dog")]),
            Q("The bird can fly.","fly",[O("hop","\U0001f430","hop"),O("fly","\U0001f985","fly"),O("sleep","\U0001f634","sleep")]),
            Q("fish","fish",[O("fish","\U0001f41f","fish"),O("bird","\U0001f426","bird"),O("cat","\U0001f431","cat")]),
            Q("Roar!","roar",[O("roar","\U0001f981","roar"),O("eat","\U0001f36a","eat"),O("wash","\U0001f9fc","wash")]),
            Q("So cute!","cute",[O("cute","\U0001f970","cute"),O("mad","\U0001f620","mad"),O("sad","\U0001f622","sad")]),
        ],
    },
    {
        "emoji": "\U0001f305", "title": "아침이에요!", "subtitle": "이 닥기, 옷 입기.",
        "hint": "morning teeth clothes shoes hello breakfast",
        "words": [W("morning","아침","\U0001f305"),W("teeth","이","\U0001f9b7"),W("clothes","옷","\U0001f455"),W("shoes","신발","\U0001f45f"),W("hello","안녕","\U0001f44b"),W("breakfast","아침밥","\U0001f33e"),W("ready","준비","\U0001f4aa"),W("go","가자","\U0001f6b6")],
        "dialogue": [
            L("별이","you","Good morning!","아침에 잘 자써!"),
            L(NAME,"me","Hello!","안녕!"),
            L("별이","you","Brush your teeth.","이 닥자."),
            L(NAME,"me","Okay. Brush, brush!","응. 쓰쓰!"),
            L("별이","you","Put on your shoes.","신발 신어."),
            L(NAME,"me","I'm ready. Let's go!","준비됐어. 가자!"),
        ],
        "quizzes": [
            Q("Good morning!","morning",[O("morning","\U0001f305","morning"),O("sleep","\U0001f634","sleep"),O("rain","\u2614","rain")]),
            Q("shoes","shoes",[O("teeth","\U0001f9b7","teeth"),O("shoes","\U0001f45f","shoes"),O("clothes","\U0001f455","clothes")]),
            Q("Brush your teeth.","teeth",[O("teeth","\U0001f9b7","teeth"),O("go","\U0001f6b6","go"),O("hello","\U0001f44b","hello")]),
            Q("hello","hello",[O("hello","\U0001f44b","hello"),O("ready","\U0001f4aa","ready"),O("shoes","\U0001f45f","shoes")]),
            Q("breakfast","breakfast",[O("breakfast","\U0001f33e","breakfast"),O("car","\U0001f697","car"),O("dog","\U0001f436","dog")]),
            Q("Let's go!","go",[O("sleep","\U0001f634","sleep"),O("go","\U0001f6b6","go"),O("sit","\U0001fa91","sit")]),
        ],
    },
    {
        "emoji": "\u2614", "title": "오늘 날씨는?", "subtitle": "비, 해, 바람.",
        "hint": "sun rain wind cold hot coat",
        "words": [W("sun","해","\u2600"),W("rain","비","\u2614"),W("wind","바람","\U0001f4a8"),W("cold","추워","\U0001f976"),W("hot","더워","\U0001f975"),W("coat","코트","\U0001f9e5"),W("hat","모자","\U0001f3a9"),W("wow","우와","\U0001f62e")],
        "dialogue": [
            L("별이","you","Look outside!","밖을 봐!"),
            L(NAME,"me","Oh! Rain!","어! 비야!"),
            L("별이","you","It's cold. Coat on.","추워. 코트 입자."),
            L(NAME,"me","My hat, too!","모자도!"),
            L("별이","you","The wind is whoosh!","바람이 후!"),
            L(NAME,"me","Wow! Let's run.","우와! 달려가자."),
        ],
        "quizzes": [
            Q("rain","rain",[O("sun","\u2600","sun"),O("rain","\u2614","rain"),O("hat","\U0001f3a9","hat")]),
            Q("It's cold.","cold",[O("hot","\U0001f975","hot"),O("cold","\U0001f976","cold"),O("wow","\U0001f62e","wow")]),
            Q("coat","coat",[O("coat","\U0001f9e5","coat"),O("hat","\U0001f3a9","hat"),O("sun","\u2600","sun")]),
            Q("The sun is hot.","hot",[O("cold","\U0001f976","cold"),O("hot","\U0001f975","hot"),O("rain","\u2614","rain")]),
            Q("hat","hat",[O("wind","\U0001f4a8","wind"),O("hat","\U0001f3a9","hat"),O("coat","\U0001f9e5","coat")]),
            Q("Wow!","wow",[O("wow","\U0001f62e","wow"),O("sad","\U0001f622","sad"),O("sleep","\U0001f634","sleep")]),
        ],
    },
    {
        "emoji": "\U0001f6bf", "title": "목욕 시간!", "subtitle": "물, 비누, 수건.",
        "hint": "bath water soap splash clean towel",
        "words": [W("bath","목욕","\U0001f6c1"),W("water","물","\U0001f4a7"),W("soap","비누","\U0001f9fc"),W("splash","참방","\U0001f92f"),W("clean","깨끗","\U0001f9fd"),W("towel","수건","\U0001f9f6"),W("duck","오리","\U0001f986"),W("warm","따뜻","\U0001f525")],
        "dialogue": [
            L("별이","you","Bath time!","목욕 시간이야!"),
            L(NAME,"me","Splash, splash!","참방, 참방!"),
            L("별이","you","Where is the duck?","오리 어디 있어?"),
            L(NAME,"me","Here! Quack quack!","여기! 꼭꼭!"),
            L("별이","you","All clean now.","이제 깨끗해."),
            L(NAME,"me","Warm towel, please.","따뜻한 수건 주세요."),
        ],
        "quizzes": [
            Q("bath","bath",[O("bath","\U0001f6c1","bath"),O("duck","\U0001f986","duck"),O("soap","\U0001f9fc","soap")]),
            Q("Splash!","splash",[O("sleep","\U0001f634","sleep"),O("splash","\U0001f92f","splash"),O("eat","\U0001f36a","eat")]),
            Q("duck","duck",[O("towel","\U0001f9f6","towel"),O("duck","\U0001f986","duck"),O("water","\U0001f4a7","water")]),
            Q("soap","soap",[O("soap","\U0001f9fc","soap"),O("warm","\U0001f525","warm"),O("bath","\U0001f6c1","bath")]),
            Q("All clean.","clean",[O("clean","\U0001f9fd","clean"),O("cold","\U0001f976","cold"),O("car","\U0001f697","car")]),
            Q("towel","towel",[O("duck","\U0001f986","duck"),O("towel","\U0001f9f6","towel"),O("soap","\U0001f9fc","soap")]),
        ],
    },
    {
        "emoji": "\U0001f3e2", "title": "밖에 나가자!", "subtitle": "버스, 가게, 안녕.",
        "hint": "bus shop hello walk stop bag",
        "words": [W("bus","버스","\U0001f68c"),W("shop","가게","\U0001f3ea"),W("walk","걸어","\U0001f6b6"),W("stop","먼춰","\U0001f6d1"),W("bag","가방","\U0001f45c"),W("hello","안녕","\U0001f44b"),W("big","탤","\U0001f4cf"),W("go","가자","\U0001f3c3")],
        "dialogue": [
            L("별이","you","Let's go out!","밖에 나가자!"),
            L(NAME,"me","The bus is big!","버스가 어마 크다!"),
            L("별이","you","Hold my hand.","손 잡자."),
            L(NAME,"me","Okay. Walk, walk.","응. 족족."),
            L("별이","you","Look, a shop!","봐, 가게야!"),
            L(NAME,"me","Hello!","안녕!"),
        ],
        "quizzes": [
            Q("bus","bus",[O("bus","\U0001f68c","bus"),O("bag","\U0001f45c","bag"),O("shop","\U0001f3ea","shop")]),
            Q("Let's walk.","walk",[O("stop","\U0001f6d1","stop"),O("walk","\U0001f6b6","walk"),O("sleep","\U0001f634","sleep")]),
            Q("shop","shop",[O("shop","\U0001f3ea","shop"),O("bus","\U0001f68c","bus"),O("bag","\U0001f45c","bag")]),
            Q("Stop!","stop",[O("go","\U0001f3c3","go"),O("stop","\U0001f6d1","stop"),O("hello","\U0001f44b","hello")]),
            Q("bag","bag",[O("big","\U0001f4cf","big"),O("bag","\U0001f45c","bag"),O("bus","\U0001f68c","bus")]),
            Q("Hello!","hello",[O("hello","\U0001f44b","hello"),O("stop","\U0001f6d1","stop"),O("walk","\U0001f6b6","walk")]),
        ],
    },
    {
        "emoji": "\U0001f3a8", "title": "그림 그리자!", "subtitle": "색, 연필, 동그란.",
        "hint": "draw color red blue paper crayon",
        "words": [W("draw","그려","\U0001f58d"),W("red","빨강","\U0001f534"),W("blue","파랑","\U0001f535"),W("paper","종이","\U0001f4c4"),W("crayon","크레용","\U0001f58d"),W("circle","동그란","\u2b55"),W("star","별","\u2b50"),W("pretty","예쁘","\U0001f338")],
        "dialogue": [
            L("별이","you","Let's draw!","그림 그리자!"),
            L(NAME,"me","I want red.","나 빨강색!"),
            L("별이","you","Draw a circle.","동그란 그려."),
            L(NAME,"me","A star, too!","별도!"),
            L("별이","you","Blue paper.","파란 종이."),
            L(NAME,"me","So pretty!","정말 예쁘!"),
        ],
        "quizzes": [
            Q("red","red",[O("red","\U0001f534","red"),O("blue","\U0001f535","blue"),O("star","\u2b50","star")]),
            Q("Draw a circle.","circle",[O("paper","\U0001f4c4","paper"),O("circle","\u2b55","circle"),O("crayon","\U0001f58d","crayon")]),
            Q("star","star",[O("star","\u2b50","star"),O("red","\U0001f534","red"),O("blue","\U0001f535","blue")]),
            Q("blue","blue",[O("red","\U0001f534","red"),O("blue","\U0001f535","blue"),O("pretty","\U0001f338","pretty")]),
            Q("crayon","crayon",[O("crayon","\U0001f58d","crayon"),O("paper","\U0001f4c4","paper"),O("star","\u2b50","star")]),
            Q("So pretty!","pretty",[O("pretty","\U0001f338","pretty"),O("sad","\U0001f622","sad"),O("cold","\U0001f976","cold")]),
        ],
    },
    {
        "emoji": "\U0001f3b5", "title": "노래 불러!", "subtitle": "노래, 박수, 추추.",
        "hint": "sing song clap dance loud quiet",
        "words": [W("sing","노래","\U0001f3a4"),W("song","노래","\U0001f3b5"),W("clap","손벽","\U0001f44f"),W("dance","추추","\U0001f483"),W("loud","케","\U0001f50a"),W("quiet","조용","\U0001f507"),W("happy","기뻘","\U0001f604"),W("again","다시","\U0001f504")],
        "dialogue": [
            L("별이","you","Let's sing a song!","노래 불러!"),
            L(NAME,"me","La la la!","라 라 라!"),
            L("별이","you","Clap your hands!","손벽 치자!"),
            L(NAME,"me","Clap, clap!","짝짝!"),
            L("별이","you","Now dance!","이제 추추!"),
            L(NAME,"me","Again, again!","또, 또!"),
        ],
        "quizzes": [
            Q("sing","sing",[O("sing","\U0001f3a4","sing"),O("quiet","\U0001f507","quiet"),O("dance","\U0001f483","dance")]),
            Q("Clap your hands!","clap",[O("sleep","\U0001f634","sleep"),O("clap","\U0001f44f","clap"),O("eat","\U0001f36a","eat")]),
            Q("dance","dance",[O("dance","\U0001f483","dance"),O("song","\U0001f3b5","song"),O("loud","\U0001f50a","loud")]),
            Q("quiet","quiet",[O("loud","\U0001f50a","loud"),O("quiet","\U0001f507","quiet"),O("again","\U0001f504","again")]),
            Q("song","song",[O("song","\U0001f3b5","song"),O("clap","\U0001f44f","clap"),O("happy","\U0001f604","happy")]),
            Q("Again!","again",[O("again","\U0001f504","again"),O("sad","\U0001f622","sad"),O("cold","\U0001f976","cold")]),
        ],
    },
    {
        "emoji": "\U0001f34e", "title": "주방 돔자!", "subtitle": "사과, 바나나, 돔도록.",
        "hint": "kitchen help mix bowl spoon banana",
        "words": [W("help","돔와","\U0001f91d"),W("mix","서어","\U0001f958"),W("bowl","그릇","\U0001f963"),W("spoon","숪가락","\U0001f944"),W("banana","바나나","\U0001f34c"),W("milk","우유","\U0001f95b"),W("stir","저어","\U0001f373"),W("done","다됐어","\u2705")],
        "dialogue": [
            L("별이","you","Can you help me?","돔와 줄래?"),
            L(NAME,"me","Yes! I can help.","응! 내가 돔솜게."),
            L("별이","you","Mix the banana.","바나나 서어."),
            L(NAME,"me","Stir, stir!","저어, 저어!"),
            L("별이","you","Milk in the bowl.","그릇에 우유."),
            L(NAME,"me","Done!","다 됐어!"),
        ],
        "quizzes": [
            Q("help","help",[O("help","\U0001f91d","help"),O("milk","\U0001f95b","milk"),O("bowl","\U0001f963","bowl")]),
            Q("Mix the banana.","mix",[O("sleep","\U0001f634","sleep"),O("mix","\U0001f958","mix"),O("run","\U0001f3c3","run")]),
            Q("spoon","spoon",[O("spoon","\U0001f944","spoon"),O("bowl","\U0001f963","bowl"),O("milk","\U0001f95b","milk")]),
            Q("banana","banana",[O("milk","\U0001f95b","milk"),O("banana","\U0001f34c","banana"),O("done","\u2705","done")]),
            Q("bowl","bowl",[O("bowl","\U0001f963","bowl"),O("help","\U0001f91d","help"),O("stir","\U0001f373","stir")]),
            Q("Done!","done",[O("done","\u2705","done"),O("sad","\U0001f622","sad"),O("cold","\U0001f976","cold")]),
        ],
    },
    {
        "emoji": "\U0001f31f", "title": "밤 인사!", "subtitle": "달, 별, 잠자.",
        "hint": "night moon star pajama hug sleep",
        "words": [W("night","밤","\U0001f319"),W("moon","달","\U0001f31d"),W("star","별","\u2b50"),W("pajama","잠옷","\U0001f9ba"),W("hug","안아","\U0001f917"),W("sleep","자","\U0001f634"),W("soft","부드러","\U0001f45a"),W("good night","잘 자","\U0001f31c")],
        "dialogue": [
            L("별이","you","It's night time.","밤이야."),
            L(NAME,"me","Look, the moon!","봐, 달!"),
            L("별이","you","Pajama on.","잠옷 입자."),
            L(NAME,"me","Soft pajama.","부드러워."),
            L("별이","you","Hug, then sleep.","안아 주고 자."),
            L(NAME,"me","Good night!","잘 자!"),
        ],
        "quizzes": [
            Q("moon","moon",[O("moon","\U0001f31d","moon"),O("star","\u2b50","star"),O("night","\U0001f319","night")]),
            Q("Good night!","good night",[O("good night","\U0001f31c","good night"),O("hug","\U0001f917","hug"),O("soft","\U0001f45a","soft")]),
            Q("star","star",[O("pajama","\U0001f9ba","pajama"),O("star","\u2b50","star"),O("moon","\U0001f31d","moon")]),
            Q("pajama","pajama",[O("pajama","\U0001f9ba","pajama"),O("sleep","\U0001f634","sleep"),O("hug","\U0001f917","hug")]),
            Q("Give me a hug.","hug",[O("hug","\U0001f917","hug"),O("run","\U0001f3c3","run"),O("eat","\U0001f36a","eat")]),
            Q("sleep","sleep",[O("sleep","\U0001f634","sleep"),O("star","\u2b50","star"),O("moon","\U0001f31d","moon")]),
        ],
    },
    {
        "emoji": "\U0001f455", "title": "옷 입자!", "subtitle": "싘츠, 바지, 양말.",
        "hint": "shirt pants socks hat on off",
        "words": [W("shirt","싘츠","\U0001f455"),W("pants","바지","\U0001f456"),W("socks","양말","\U0001f9e6"),W("hat","모자","\U0001f3a9"),W("on","입어","\U0001f446"),W("off","벗어","\U0001f447"),W("fast","빨리","\U0001f3c3"),W("yes","응","\U0001f44d")],
        "dialogue": [
            L("별이","you","Put your shirt on.","싘츠 입자."),
            L(NAME,"me","Shirt on!","싘츠 입었어!"),
            L("별이","you","Now socks.","이제 양말."),
            L(NAME,"me","One, two socks!","하나, 둘 양말!"),
            L("별이","you","Hat on?","모자 쓸까?"),
            L(NAME,"me","Yes! So fast.","응! 정말 빨라."),
        ],
        "quizzes": [
            Q("shirt","shirt",[O("shirt","\U0001f455","shirt"),O("pants","\U0001f456","pants"),O("hat","\U0001f3a9","hat")]),
            Q("Put it on.","on",[O("off","\U0001f447","off"),O("on","\U0001f446","on"),O("yes","\U0001f44d","yes")]),
            Q("socks","socks",[O("socks","\U0001f9e6","socks"),O("hat","\U0001f3a9","hat"),O("shirt","\U0001f455","shirt")]),
            Q("pants","pants",[O("pants","\U0001f456","pants"),O("shirt","\U0001f455","shirt"),O("fast","\U0001f3c3","fast")]),
            Q("Hat on?","hat",[O("hat","\U0001f3a9","hat"),O("socks","\U0001f9e6","socks"),O("off","\U0001f447","off")]),
            Q("Yes!","yes",[O("yes","\U0001f44d","yes"),O("off","\U0001f447","off"),O("pants","\U0001f456","pants")]),
        ],
    },
]

ACTIONS = [
    A("Jump!","점프!","\U0001f998"),
    A("Clap!","손벽!","\U0001f44f"),
    A("Run!","달려!","\U0001f3c3"),
    A("Wave!","손 흔들어!","\U0001f44b"),
    A("Spin!","빙글빙글!","\U0001f4ab"),
    A("Touch your nose!","코를 만져!","\U0001f443"),
    A("Sit down!","앉아!","\U0001fa91"),
    A("Stretch!","팔 쪽!","\U0001f646"),
]

THEME = PACKS[NOW.timetuple().tm_yday % len(PACKS)]

def pack_content(pack):
    data = {
        "date": DATE_KR,
        "dateKey": DATE_KEY,
        "theme": {"emoji": pack["emoji"], "title": pack["title"], "subtitle": pack["subtitle"]},
        "words": copy.deepcopy(pack["words"]),
        "actions": copy.deepcopy(ACTIONS),
        "dialogue": copy.deepcopy(pack["dialogue"]),
        "quizzes": copy.deepcopy(pack["quizzes"]),
    }
    return data

def validate(data):
    words = data.get("words") or []
    actions = data.get("actions") or []
    dialogue = data.get("dialogue") or []
    quizzes = data.get("quizzes") or []
    if len(words) < 8 or len(actions) < 6 or len(dialogue) < 6 or len(quizzes) < 6:
        raise ValueError("short content")
    for line in dialogue[:6]:
        line["who"] = line.get("who") or (NAME if line.get("role") == "me" else "별이")
        line["role"] = line.get("role") if line.get("role") in ("me", "you") else "you"
        if line["who"] in ("쳄이", "책이", "챙이"):
            line["who"] = NAME
    data["words"] = words[:8]
    data["actions"] = actions[:8]
    data["dialogue"] = dialogue[:6]
    data["quizzes"] = [{"speak": q["speak"], "answer": q["answer"], "options": (q.get("options") or [])[:3]} for q in quizzes[:6]]
    data["date"] = DATE_KR
    data["dateKey"] = DATE_KEY
    data["theme"] = {"emoji": THEME["emoji"], "title": THEME["title"], "subtitle": THEME["subtitle"]}
    return data

def ask_gemini(api_key):
    prompt = f"""오늘 {DATE_KR}
필수 테마: {THEME['emoji']} {THEME['title']} ({THEME['hint']})
6살 {NAME} 몸놀이 영어. JSON만.
공원 park/slide 금지. 오늘 테마 단어만.
words 8, actions 8, dialogue 6, quizzes 6 listen-pick.
"""
    last = "no model"
    for model in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-flash-latest"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            res = requests.post(
                url,
                json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.8, "responseMimeType": "application/json"}},
                timeout=90,
            )
            data = res.json()
            if "candidates" not in data:
                last = f"{model}: {res.text[:180]}"
                continue
            text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            return validate(json.loads(text))
        except Exception as e:
            last = f"{model}: {e}"
    raise RuntimeError(last)

def render(content):
    here = os.path.dirname(os.path.abspath(__file__))
    html = open(os.path.join(here, "template.html"), encoding="utf-8").read()
    html = html.replace("__CONTENT__", json.dumps(content, ensure_ascii=False))
    html = html.replace("쳄이", NAME).replace("책이", NAME).replace("챙이", NAME)
    open(os.path.join(here, "english.html"), "w", encoding="utf-8").write(html)
    print("wrote", content["theme"]["title"], content["words"][0]["en"], NAME)

def main():
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    content = None
    if api_key:
        try:
            content = ask_gemini(api_key)
            print("gemini ok")
        except Exception as e:
            print("gemini fallback:", e)
    if content is None:
        content = pack_content(THEME)
    render(content)

if __name__ == "__main__":
    main()
