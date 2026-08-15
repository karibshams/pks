/* ═══════════════════════════════════════════════
   KARIB SHAMS PORTFOLIO v2 — main.js
═══════════════════════════════════════════════ */

// ── CUSTOM CURSOR ──────────────────────────────
const dot  = document.getElementById('cursorDot');
const ring = document.getElementById('cursorRing');
let mx=0,my=0,rx=0,ry=0;
document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;dot.style.left=mx+'px';dot.style.top=my+'px'});
(function loop(){rx+=(mx-rx)*.1;ry+=(my-ry)*.1;ring.style.left=rx+'px';ring.style.top=ry+'px';requestAnimationFrame(loop)})();
document.querySelectorAll('a,button,.proj-card,.sk-tag,.pub-card').forEach(el=>{
  el.addEventListener('mouseenter',()=>{ring.style.width='46px';ring.style.height='46px';ring.style.background='rgba(0,255,194,.07)'});
  el.addEventListener('mouseleave',()=>{ring.style.width='30px';ring.style.height='30px';ring.style.background='transparent'});
});

// ── NEURAL CANVAS ──────────────────────────────
const canvas=document.getElementById('neural-bg');
const ctx=canvas.getContext('2d');
let W,H,nodes=[];
function resize(){W=canvas.width=window.innerWidth;H=canvas.height=window.innerHeight}
resize();window.addEventListener('resize',resize);

class Node{
  constructor(){this.x=Math.random()*W;this.y=Math.random()*H;this.vx=(Math.random()-.5)*.35;this.vy=(Math.random()-.5)*.35;this.r=Math.random()*1.8+.8;this.phase=Math.random()*Math.PI*2}
  update(){this.x+=this.vx;this.y+=this.vy;this.phase+=.018;if(this.x<0||this.x>W)this.vx*=-1;if(this.y<0||this.y>H)this.vy*=-1}
}
for(let i=0;i<75;i++)nodes.push(new Node());

(function drawLoop(){
  ctx.clearRect(0,0,W,H);
  nodes.forEach(n=>n.update());
  for(let i=0;i<nodes.length;i++){
    for(let j=i+1;j<nodes.length;j++){
      const dx=nodes[i].x-nodes[j].x,dy=nodes[i].y-nodes[j].y,d=Math.sqrt(dx*dx+dy*dy);
      if(d<130){const a=(1-d/130)*.25;ctx.beginPath();ctx.moveTo(nodes[i].x,nodes[i].y);ctx.lineTo(nodes[j].x,nodes[j].y);ctx.strokeStyle=`rgba(0,255,194,${a})`;ctx.lineWidth=.5;ctx.stroke()}
    }
    const p=Math.abs(Math.sin(nodes[i].phase));
    ctx.beginPath();ctx.arc(nodes[i].x,nodes[i].y,nodes[i].r+p*.6,0,Math.PI*2);
    ctx.fillStyle=`rgba(0,255,194,${.25+p*.35})`;ctx.fill();
  }
  requestAnimationFrame(drawLoop);
})();

// ── TYPING EFFECT ──────────────────────────────
const ROLES=['Data Scientist','AI Developer','Research Assistant','ML Engineer','NLP Specialist','Computer Vision Engineer','LLM Systems Builder'];
let ti=0,ci=0,del=false;
const tel=document.getElementById('typedText');
function typeLoop(){
  const cur=ROLES[ti];
  if(!del){tel.textContent=cur.slice(0,++ci);if(ci===cur.length){del=true;setTimeout(typeLoop,2200);return}}
  else{tel.textContent=cur.slice(0,--ci);if(ci===0){del=false;ti=(ti+1)%ROLES.length}}
  setTimeout(typeLoop,del?45:85);
}
typeLoop();

// ── COUNTERS ──────────────────────────────────
function runCounters(){
  document.querySelectorAll('.hs-n').forEach(el=>{
    const target=+el.dataset.count,step=target/45;let cur=0;
    const t=setInterval(()=>{cur+=step;if(cur>=target){el.textContent=target+(target>=10?'+':'');clearInterval(t)}else el.textContent=Math.floor(cur)},35);
  });
}

// ── SCROLL REVEAL ─────────────────────────────
const ro=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('vis');ro.unobserve(e.target)}});
},{threshold:.1});
document.querySelectorAll('.reveal').forEach(el=>ro.observe(el));

// Counter trigger
const heroObs=new IntersectionObserver(e=>{if(e[0].isIntersecting){runCounters();heroObs.disconnect()}},{threshold:.4});
const hs=document.querySelector('.hero-stats');if(hs)heroObs.observe(hs);

// ── NAVBAR ────────────────────────────────────
const nb=document.getElementById('navbar');
const tog=document.getElementById('navToggle');
const nl=document.getElementById('navLinks');
window.addEventListener('scroll',()=>{
  nb.style.background=window.scrollY>20?'rgba(26,30,35,.96)':'rgba(26,30,35,.85)';
  let cur='';
  document.querySelectorAll('section[id]').forEach(s=>{if(window.scrollY>=s.offsetTop-90)cur=s.id});
  document.querySelectorAll('.nav-links a').forEach(a=>{a.classList.toggle('active',a.getAttribute('href')==='#'+cur)});
});
tog.addEventListener('click',()=>nl.classList.toggle('open'));
document.querySelectorAll('.nav-links a').forEach(a=>a.addEventListener('click',()=>nl.classList.remove('open')));

// ── PROJECT FILTER ─────────────────────────────
document.querySelectorAll('.ptab').forEach(btn=>{
  btn.addEventListener('click',()=>{
    document.querySelectorAll('.ptab').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    const f=btn.dataset.filter;
    document.querySelectorAll('.proj-card').forEach(c=>{
      c.classList.toggle('hidden',f!=='all'&&c.dataset.type!==f);
    });
  });
});

// ── QUIZ GAME ─────────────────────────────────
const QS=[
  {q:"What does RAG stand for in AI?",opts:["Random Augmented Generation","Retrieval Augmented Generation","Rapid AI Graph","Recursive Attention Gate"],a:1},
  {q:"Which algorithm does backpropagation train?",opts:["Decision Tree","Neural Network","K-Means","SVM"],a:1},
  {q:"What is the purpose of SHAP values?",opts:["Model training","Model explainability","Data cleaning","Hyperparameter tuning"],a:1},
  {q:"YOLO is primarily used for?",opts:["Text generation","Object detection","Data clustering","Speech recognition"],a:1},
  {q:"Which model architecture powers ChatGPT?",opts:["CNN","RNN","Transformer","KNN"],a:2},
  {q:"What does XAI stand for?",opts:["Extreme AI","Explainable AI","Extended AI","Expert AI"],a:1},
  {q:"n8n is primarily used for?",opts:["Deep learning","Workflow automation","Database management","Image processing"],a:1},
  {q:"Semi-supervised learning uses?",opts:["Only labeled data","Only unlabeled data","Both labeled & unlabeled","No training data"],a:2},
  {q:"Swin Transformer is primarily used for?",opts:["NLP tasks","Computer Vision","Audio processing","Tabular data"],a:1},
  {q:"Which library is used for SHAP analysis?",opts:["TensorFlow","SHAP (shapley)","Matplotlib","Scikit-plot"],a:1},
];
let qi=0,sc=0,quizActive=false;

function initQuiz(){
  qi=0;sc=0;quizActive=true;
  document.getElementById('quiz-start-btn').style.display='none';
  document.getElementById('quiz-score-top').textContent='Score: 0/'+QS.length;
  document.getElementById('quiz-body').innerHTML='<div id="quiz-q" class="quiz-q"></div><div id="quiz-opts" class="quiz-opts"></div>';
  showQ();
}
function showQ(){
  if(qi>=QS.length){
    document.getElementById('quiz-body').innerHTML=`
      <p class="quiz-q">🎉 Quiz Complete! Score: ${sc}/${QS.length}</p>
      <button class="btn-primary" onclick="initQuiz()" style="margin-top:1rem">Play Again</button>`;
    document.getElementById('quiz-score-top').textContent='Final: '+sc+'/'+QS.length;
    return;
  }
  const q=QS[qi];
  document.getElementById('quiz-q').textContent=`Q${qi+1}/${QS.length}: ${q.q}`;
  const oe=document.getElementById('quiz-opts');oe.innerHTML='';
  q.opts.forEach((o,i)=>{
    const b=document.createElement('button');b.className='q-opt';b.textContent=o;
    b.onclick=()=>{
      Array.from(oe.children).forEach(x=>x.disabled=true);
      if(i===q.a){b.classList.add('correct');sc++}
      else{b.classList.add('wrong');oe.children[q.a].classList.add('correct')}
      document.getElementById('quiz-score-top').textContent='Score: '+sc+'/'+QS.length;
      qi++;setTimeout(showQ,1100);
    };
    oe.appendChild(b);
  });
}

// ── AI CHAT ───────────────────────────────────
let chatHistory=[];

async function sendChat(){
  const inp=document.getElementById('chatInput');
  const msg=inp.value.trim();if(!msg)return;
  inp.value='';
  hideSuggested();
  addMsg(msg,'user');
  chatHistory.push({role:'user',content:msg});

  const typingId='typing-'+Date.now();
  addTyping(typingId);

  try{
    const res=await fetch('/api/chat/',{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':getCsrf()},
      body:JSON.stringify({message:msg,history:chatHistory.slice(-16)}),
    });
    const data=await res.json();
    removeTyping(typingId);
    const reply=data.reply||'No response received.';
    addMsg(reply,'bot');
    chatHistory.push({role:'assistant',content:reply});
  }catch(e){
    removeTyping(typingId);
    addMsg('Connection error. Please try again.','bot');
  }
}

function sendSuggested(btn){
  document.getElementById('chatInput').value=btn.textContent;
  sendChat();
}

function hideSuggested(){
  const s=document.getElementById('chatSuggested');
  if(s)s.style.display='none';
}

function addMsg(text,role){
  const wrap=document.getElementById('chatMsgs');
  const d=document.createElement('div');d.className='cm '+role;
  if(role==='bot')d.innerHTML=`<span class="bot-av-sm">🤖</span><div class="bubble">${escHtml(text)}</div>`;
  else d.innerHTML=`<div class="bubble">${escHtml(text)}</div>`;
  wrap.appendChild(d);wrap.scrollTop=wrap.scrollHeight;
}

function addTyping(id){
  const wrap=document.getElementById('chatMsgs');
  const d=document.createElement('div');d.className='cm bot';d.id=id;
  d.innerHTML='<span class="bot-av-sm">🤖</span><div class="bubble"><span class="typing-dots"><span>●</span><span>●</span><span>●</span></span></div>';
  wrap.appendChild(d);wrap.scrollTop=wrap.scrollHeight;
}
function removeTyping(id){const el=document.getElementById(id);if(el)el.remove()}

function clearChat(){
  chatHistory=[];
  document.getElementById('chatMsgs').innerHTML=`
    <div class="cm bot"><span class="bot-av-sm">🤖</span>
    <div class="bubble">Chat cleared! Ask me anything about Karib's research, projects, or any AI/ML topic.</div></div>`;
  const s=document.getElementById('chatSuggested');if(s)s.style.display='flex';
}

document.getElementById('chatInput').addEventListener('keydown',e=>{if(e.key==='Enter')sendChat()});

function escHtml(t){return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function getCsrf(){return document.querySelector('[name=csrfmiddlewaretoken]')?.value||''}

// ── FEEDBACK ──────────────────────────────────
async function submitFeedback(e){
  e.preventDefault();
  const res=document.getElementById('fb-res');
  try{
    const r=await fetch('/api/feedback/',{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':getCsrf()},
      body:JSON.stringify({name:document.getElementById('fb-name').value,email:document.getElementById('fb-email').value,message:document.getElementById('fb-msg').value}),
    });
    const d=await r.json();
    res.textContent=d.msg||'Submitted!';
    document.getElementById('fbForm').reset();
    setTimeout(()=>res.textContent='',4000);
  }catch{res.textContent='Error submitting. Try again.'}
}

// ── UPLOAD ZONE ───────────────────────────────
const uz=document.getElementById('uploadZone');
const fi=document.getElementById('fileInput');
const ur=document.getElementById('uploadResult');
uz.addEventListener('dragover',e=>{e.preventDefault();uz.style.borderColor='var(--acc)'});
uz.addEventListener('dragleave',()=>uz.style.borderColor='');
uz.addEventListener('drop',e=>{e.preventDefault();uz.style.borderColor='';if(e.dataTransfer.files[0])showUpload(e.dataTransfer.files[0])});
fi.addEventListener('change',()=>{if(fi.files[0])showUpload(fi.files[0])});
function showUpload(f){
  ur.innerHTML=`✅ <strong>${f.name}</strong> (${(f.size/1024).toFixed(1)} KB) — ready to showcase!`;
  setTimeout(()=>ur.innerHTML='',5000);
}
