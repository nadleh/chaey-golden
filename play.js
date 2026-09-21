const CONTENT = window.CONTENT || {words:[],quizzes:[],theme:{},dateKey:""};
const NAME = "채이";
const WORDS = (CONTENT.words || []).slice(0,15);
const QUIZZES = CONTENT.quizzes || [];
const STORE_KEY = "chaey-english-v1";
const STORE_BAK = "chaey-english-v1-bak";
const TODAY = CONTENT.dateKey || toKey(new Date());
const SEEDED = ["2026-09-10","2026-09-11","2026-09-12","2026-09-13","2026-09-14","2026-09-15","2026-09-16","2026-09-17","2026-09-18","2026-09-19","2026-09-20"];
let stars=0, audioUnlocked=false, justFinished=false, calCursor=parseKey(TODAY);
let heard=new Set(), popI=0, echoI=0, quizI=0, quizLock=false;
let matchDeck=[], matchOpen=[], matchGot=0, matchLock=false;
let curAudio=null;
function toKey(d){return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")}
function parseKey(key){const [y,m]=(key||TODAY).split("-").map(Number);return {y:y||2026,m:(m||1)-1}}
function cookieDays(){try{const m=document.cookie.match(/(?:^|; )chaey_days=([^;]*)/);if(!m)return [];return decodeURIComponent(m[1]).split(",").filter(Boolean)}catch(e){return []}}
function writeCookie(keys){const v=encodeURIComponent(keys.join(","));const max=";max-age=31536000;SameSite=Lax";try{document.cookie="chaey_days="+v+max+";path=/"}catch(e){}try{document.cookie="chaey_days="+v+max+";path=/chaey-golden"}catch(e){}}
function readJson(key){try{const d=JSON.parse(localStorage.getItem(key)||"null");if(d&&d.days&&typeof d.days==="object")return d}catch(e){}return null}
function loadStore(){const data={days:{}};
  [readJson(STORE_KEY),readJson(STORE_BAK)].forEach(d=>{if(!d)return;Object.keys(d.days).forEach(k=>{if(!data.days[k])data.days[k]=d.days[k]})});
  cookieDays().forEach(k=>{if(k&&!data.days[k])data.days[k]={theme:"영어 놀이",emoji:"⭐"}});
  SEEDED.forEach(k=>{if(!data.days[k])data.days[k]={theme:"영어 놀이",emoji:"⭐",seeded:true}});
  return data}
function saveStore(d){try{localStorage.setItem(STORE_KEY,JSON.stringify(d))}catch(e){}
  try{localStorage.setItem(STORE_BAK,JSON.stringify(d))}catch(e){}
  writeCookie(Object.keys(d.days||{}));
  try{if(navigator.storage&&navigator.storage.persist)navigator.storage.persist()}catch(e){}}
function doneDays(){return loadStore().days}
function isDone(k){return !!doneDays()[k]}
function countDays(){return Object.keys(doneDays()).length}
function streakCount(){const days=doneDays();let n=0;const d=new Date(TODAY+"T12:00:00");if(!days[toKey(d)])d.setDate(d.getDate()-1);while(days[toKey(d)]){n++;d.setDate(d.getDate()-1)}return n}
function markTodayDone(){const data=loadStore();const t=CONTENT.theme||{};data.days[TODAY]={theme:t.title||"영어 놀이",emoji:t.emoji||"⭐",stars:stars,doneAt:new Date().toISOString()};saveStore(data)}
saveStore(loadStore());
function unlockAudio(){audioUnlocked=true;if(!("speechSynthesis"in window))return;const u=new SpeechSynthesisUtterance(" ");u.volume=0;u.lang="en-US";speechSynthesis.speak(u)}
function ttsUrl(text){return "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q="+encodeURIComponent(text)}
function synthSpeak(text){
  if(!("speechSynthesis"in window))return;
  speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text);
  u.lang="en-US"; u.rate=0.96; u.pitch=1.18; u.volume=1;
  const vs=speechSynthesis.getVoices()||[];
  const pref=vs.find(x=>/en-US/i.test(x.lang)&&/samantha|karen|moira|google|enhanced|premium|nicky|siri/i.test(x.name))
    || vs.find(x=>/en-US/i.test(x.lang)&&!/compact|novelty/i.test(x.name))
    || vs.find(x=>/^en/i.test(x.lang));
  if(pref) u.voice=pref;
  speechSynthesis.speak(u);
}
function speak(text){
  unlockAudio();
  if(curAudio){try{curAudio.pause();curAudio.src=""}catch(e){}}
  const a=new Audio(ttsUrl(text));
  a.preload="auto";
  a.playbackRate=0.93;
  curAudio=a;
  const go=a.play();
  if(go&&go.catch) go.catch(()=>synthSpeak(text));
  a.onerror=()=>synthSpeak(text);
}
if(window.speechSynthesis){speechSynthesis.getVoices();speechSynthesis.onvoiceschanged=()=>speechSynthesis.getVoices()}
function addStars(n){stars+=n}
function setProgress(stage,detail){
  const map={cal:[0,"달력"],intro:[0,"시작"],words:[1,"단어 카드"],pop:[2,"풍선 놀이"],match:[3,"짝 맞추기"],echo:[4,"따라 말하기"],quiz:[5,"듣기 퀴즈"],finish:[6,"완료"]};
  const [n,name]=map[stage];
  document.getElementById("stage-name").textContent=name+(detail?" · "+detail:"");
  document.getElementById("stage-count").textContent=Math.min(n,5)+" / 5";
  document.getElementById("bar").style.width=((stage==="finish"?5:n)/5*100)+"%";
  document.getElementById("progress-wrap").classList.toggle("on",stage!=="cal");
  document.getElementById("star-chip").textContent=stage==="cal"?("⭐ "+countDays()+"일"):("⭐ "+stars);
}
function showScreen(id){["cal","intro","words","pop","match","echo","quiz","finish"].forEach(s=>document.getElementById("screen-"+s).classList.toggle("hidden",s!==id));document.getElementById("stage").scrollTop=0}
function setDock(buttons){const dock=document.getElementById("dock");dock.innerHTML="";buttons.forEach(b=>{const el=document.createElement("button");el.className="btn "+(b.cls||"btn-primary");el.textContent=b.label;if(b.disabled)el.disabled=true;el.onclick=()=>{unlockAudio();b.fn()};dock.appendChild(el)})}
function shuffle(a){return a.slice().sort(()=>Math.random()-0.5)}
function renderCalendar(){document.getElementById("cal-title").textContent=calCursor.y+"년 "+(calCursor.m+1)+"월";const grid=document.getElementById("cal-grid");grid.innerHTML="";const start=new Date(calCursor.y,calCursor.m,1).getDay();const last=new Date(calCursor.y,calCursor.m+1,0).getDate();const days=doneDays();for(let i=0;i<start;i++){const e=document.createElement("div");e.className="day empty";grid.appendChild(e)}for(let d=1;d<=last;d++){const key=calCursor.y+"-"+String(calCursor.m+1).padStart(2,"0")+"-"+String(d).padStart(2,"0");const rec=days[key];const btn=document.createElement("button");btn.type="button";btn.className="day";btn.dataset.day=key;if(key===TODAY)btn.classList.add("today");if(key>TODAY)btn.classList.add("future");if(rec)btn.classList.add("done");btn.innerHTML="<span class='n'>"+d+"</span><span class='mark'>"+(rec?"⭐":(key===TODAY?"·":""))+"</span>";btn.onclick=()=>{if(key===TODAY)go("intro")};grid.appendChild(btn)}document.getElementById("stat-days").textContent=countDays();document.getElementById("stat-streak").textContent=streakCount();const t=CONTENT.theme||{};document.getElementById("today-theme").textContent=(t.emoji||"⭐")+" "+(t.title||"오늘의 놀이");document.getElementById("today-sub").textContent=isDone(TODAY)?"오늘은 이미 별이 있어요. 또 해도 돼요.":(t.subtitle||"오늘 단어 15개!")}
function flyStarTo(dateKey){const cell=document.querySelector('[data-day="'+dateKey+'"]');if(!cell){renderCalendar();return}const flyer=document.createElement("div");flyer.className="flyer-star";flyer.textContent="⭐";flyer.style.transform="translate("+innerWidth/2+"px,"+(innerHeight*0.36)+"px) translate(-50%,-50%) scale(1)";document.body.appendChild(flyer);const r=cell.getBoundingClientRect();requestAnimationFrame(()=>{flyer.style.transform="translate("+(r.left+r.width/2)+"px,"+(r.top+r.height/2)+"px) translate(-50%,-50%) scale(.28)"});setTimeout(()=>{flyer.remove();renderCalendar()},950)}
function go(stage){setProgress(stage);showScreen(stage);if(stage==="cal"){renderCalendar();setDock([{label:isDone(TODAY)?"오늘 한 번 더 하기":"오늘 영어 놀이 시작!",cls:isDone(TODAY)?"btn-sun":"btn-primary",fn:()=>go("intro")}]);if(justFinished){justFinished=false;requestAnimationFrame(()=>flyStarTo(TODAY))}}if(stage==="intro"){const t=CONTENT.theme||{};document.getElementById("intro-emo").textContent=t.emoji||"⭐";document.getElementById("intro-title").textContent=t.title||"영어 놀이";document.getElementById("intro-sub").textContent=(t.subtitle||"")+" 오늘 단어 "+WORDS.length+"개.";setDock([{label:"단어부터 시작!",fn:()=>go("words")}])}if(stage==="words")loadWords();if(stage==="pop"){popI=0;loadPop()}if(stage==="match")loadMatch();if(stage==="echo"){echoI=0;loadEcho()}if(stage==="quiz"){quizI=0;loadQuiz()}if(stage==="finish"){markTodayDone();justFinished=true;setDock([{label:"달력에 별 붙이러 가기 ➜",cls:"btn-sun",fn:()=>go("cal")}]})}}
function loadWords(){
  heard=new Set();
  const box=document.getElementById("word-grid"); box.innerHTML="";
  WORDS.forEach(w=>{
    const b=document.createElement("button"); b.className="wcard";
    b.innerHTML="<span class='emo'>"+w.emo+"</span><span class='en'>"+w.en+"</span><span class='ko'>"+(w.ko||"")+"</span>";
    b.onclick=()=>{speak(w.en);heard.add(w.en);b.classList.add("heard");addStars(1);document.getElementById("word-sub").textContent="들은 단어 "+heard.size+" / "+WORDS.length;setDock([{label:heard.size>=WORDS.length?"풍선 놀이 ➜":"단어를 다 들어야 해요",cls:heard.size>=WORDS.length?"btn-primary":"btn-sun",disabled:heard.size<WORDS.length,fn:()=>go("pop")}])};
    box.appendChild(b);
  });
  document.getElementById("word-sub").textContent="그림을 눌러 소리를 들어요. 0 / "+WORDS.length;
  setDock([{label:"단어를 다 들어야 해요",cls:"btn-sun",disabled:true,fn:()=>{}}]);
}
function loadPop(){
  const ans=WORDS[popI % WORDS.length];
  document.getElementById("pop-count").textContent=(popI+1)+" / 10";
  const others=shuffle(WORDS.filter(w=>w.en!==ans.en)).slice(0,3);
  const opts=shuffle([ans].concat(others));
  const box=document.getElementById("pop-box"); box.innerHTML="";
  opts.forEach(w=>{
    const b=document.createElement("button"); b.className="balloon";
    b.innerHTML="<span class='emo'>"+w.emo+"</span><span class='en'>"+w.en+"</span>";
    b.onclick=()=>{if(w.en===ans.en){b.classList.add("good");addStars(1);setTimeout(()=>{if(popI<9){popI++;loadPop()}else go("match")},380)}else{b.classList.add("bad");speak(ans.en);setTimeout(()=>b.classList.remove("bad"),400)}};
    box.appendChild(b);
  });
  setProgress("pop",(popI+1)+"/10");
  setDock([{label:"🔊 다시 듣기",cls:"btn-teal",fn:()=>speak(ans.en)}]);
  setTimeout(()=>speak(ans.en),220);
}
function loadMatch(){
  const pairs=shuffle(WORDS).slice(0,6);
  matchDeck=shuffle(pairs.map(w=>({k:w.en,show:w.emo,kind:"emo"})).concat(pairs.map(w=>({k:w.en,show:w.en,kind:"en"}))));
  matchOpen=[]; matchGot=0; matchLock=false; drawMatch();
  setDock([{label:"카드 두 장을 눌러요",cls:"btn-teal",disabled:true,fn:()=>{}}]);
}
function drawMatch(){const box=document.getElementById("match-box");box.innerHTML="";matchDeck.forEach((c,i)=>{const b=document.createElement("button");const open=matchOpen.includes(i)||c.got;b.className="mem-card"+(c.got?" got":(open?" on":" back"));b.textContent=(c.got||open)?c.show:"?";b.onclick=()=>flipMatch(i);box.appendChild(b)})}
function flipMatch(i){if(matchLock||matchDeck[i].got||matchOpen.includes(i))return;matchOpen.push(i);drawMatch();if(matchOpen.length<2)return;matchLock=true;const a=matchDeck[matchOpen[0]],b=matchDeck[matchOpen[1]];if(a.k===b.k&&a.kind!==b.kind){a.got=b.got=true;matchGot++;addStars(2);speak(a.k);matchOpen=[];matchLock=false;drawMatch();if(matchGot>=6)setTimeout(()=>go("echo"),450)}else{setTimeout(()=>{matchOpen=[];matchLock=false;drawMatch()},700)}}
function loadEcho(){
  const w=WORDS[echoI];
  document.getElementById("echo-count").textContent=(echoI+1)+" / 8";
  document.getElementById("echo-emo").textContent=w.emo;
  document.getElementById("echo-en").textContent=w.en;
  document.getElementById("echo-ko").textContent=w.ko||"";
  setProgress("echo",(echoI+1)+"/8");
  setDock([
    {label:"🔊 다시 듣기",cls:"btn-teal",fn:()=>speak(w.en)},
    {label:"채이가 말했어요!",cls:"btn-sun",fn:()=>{addStars(1);if(echoI<7){echoI++;loadEcho()}else go("quiz")}}
  ]);
  setTimeout(()=>speak(w.en),240);
}
function loadQuiz(){
  quizLock=false;
  const q=QUIZZES[quizI] || {speak:WORDS[quizI].en,answer:WORDS[quizI].en,options:shuffle(WORDS).slice(0,3).map(w=>({id:w.en,emo:w.emo,label:w.en}))};
  if(!(q.options||[]).some(o=>o.id===q.answer)) q.options=[{id:q.answer,emo:(WORDS.find(w=>w.en===q.answer)||{}).emo||"⭐",label:q.answer}].concat(q.options||[]).slice(0,3);
  document.getElementById("quiz-count").textContent=(quizI+1)+" / "+Math.min(8,QUIZZES.length||8);
  const box=document.getElementById("quiz-box"); box.innerHTML="";
  q.options.forEach(opt=>{
    const b=document.createElement("button"); b.className="choice";
    b.innerHTML=opt.emo+"<span>"+opt.label+"</span>";
    b.onclick=()=>{if(quizLock)return;quizLock=true;const ok=opt.id===q.answer;b.classList.add(ok?"good":"bad");if(ok)addStars(2);else[...box.children].forEach((el,i)=>{if(q.options[i].id===q.answer)el.classList.add("good")});setDock([{label:"🔊 다시 듣기",cls:"btn-teal",fn:()=>speak(q.speak)},{label:quizI>=7?"끝! 잘했어요 ➜":"다음 ➜",fn:()=>{if(quizI<7){quizI++;loadQuiz()}else go("finish")}}])};
    box.appendChild(b);
  });
  setProgress("quiz",(quizI+1)+"/8");
  setDock([{label:"🔊 다시 듣기",cls:"btn-teal",fn:()=>speak(q.speak)}]);
  setTimeout(()=>speak(q.speak),240);
}
document.getElementById("cal-prev").onclick=()=>{calCursor.m--;if(calCursor.m<0){calCursor.m=11;calCursor.y--}renderCalendar()};
document.getElementById("cal-next").onclick=()=>{calCursor.m++;if(calCursor.m>11){calCursor.m=0;calCursor.y++}renderCalendar()};
go("cal");
