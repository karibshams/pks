/* ===== KARIB SHAMS PORTFOLIO - main.js ===== */

// ---- CUSTOM CURSOR ----
const dot = document.getElementById('cursorDot');
const ring = document.getElementById('cursorRing');
let mx = 0, my = 0, rx = 0, ry = 0;

document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  dot.style.left = mx + 'px';
  dot.style.top = my + 'px';
});
(function animCursor() {
  rx += (mx - rx) * 0.1;
  ry += (my - ry) * 0.1;
  ring.style.left = rx + 'px';
  ring.style.top = ry + 'px';
  requestAnimationFrame(animCursor);
})();
document.querySelectorAll('a, button, .project-card, .skill-tag').forEach(el => {
  el.addEventListener('mouseenter', () => {
    ring.style.width = '48px'; ring.style.height = '48px';
    ring.style.background = 'rgba(0,255,194,0.08)';
  });
  el.addEventListener('mouseleave', () => {
    ring.style.width = '30px'; ring.style.height = '30px';
    ring.style.background = 'transparent';
  });
});

// ---- NEURAL NETWORK CANVAS ----
const canvas = document.getElementById('neural-bg');
const ctx = canvas.getContext('2d');
let W, H, nodes = [], frameId;

function resize() {
  W = canvas.width = window.innerWidth;
  H = canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

class Node {
  constructor() { this.reset(); }
  reset() {
    this.x = Math.random() * W;
    this.y = Math.random() * H;
    this.vx = (Math.random() - 0.5) * 0.4;
    this.vy = (Math.random() - 0.5) * 0.4;
    this.r = Math.random() * 2 + 1;
    this.pulse = Math.random() * Math.PI * 2;
  }
  update() {
    this.x += this.vx; this.y += this.vy;
    this.pulse += 0.02;
    if (this.x < 0 || this.x > W) this.vx *= -1;
    if (this.y < 0 || this.y > H) this.vy *= -1;
  }
}

for (let i = 0; i < 80; i++) nodes.push(new Node());

function drawNeural() {
  ctx.clearRect(0, 0, W, H);
  nodes.forEach(n => n.update());

  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const dx = nodes[i].x - nodes[j].x;
      const dy = nodes[i].y - nodes[j].y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 140) {
        const alpha = (1 - dist / 140) * 0.3;
        ctx.beginPath();
        ctx.moveTo(nodes[i].x, nodes[i].y);
        ctx.lineTo(nodes[j].x, nodes[j].y);
        ctx.strokeStyle = `rgba(0,255,194,${alpha})`;
        ctx.lineWidth = 0.6;
        ctx.stroke();
      }
    }
    const pulse = Math.abs(Math.sin(nodes[i].pulse));
    ctx.beginPath();
    ctx.arc(nodes[i].x, nodes[i].y, nodes[i].r + pulse, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(0,255,194,${0.3 + pulse * 0.4})`;
    ctx.fill();
  }
  frameId = requestAnimationFrame(drawNeural);
}
drawNeural();

// ---- TYPING EFFECT ----
const texts = [
  'Data Scientist',
  'AI Developer',
  'Research Assistant',
  'Machine Learning Engineer',
  'NLP Specialist',
  'Computer Vision Engineer',
];
let tIdx = 0, cIdx = 0, deleting = false;
const typedEl = document.getElementById('typedText');

function typeLoop() {
  const current = texts[tIdx];
  if (!deleting) {
    typedEl.textContent = current.slice(0, ++cIdx);
    if (cIdx === current.length) { deleting = true; setTimeout(typeLoop, 2000); return; }
  } else {
    typedEl.textContent = current.slice(0, --cIdx);
    if (cIdx === 0) { deleting = false; tIdx = (tIdx + 1) % texts.length; }
  }
  setTimeout(typeLoop, deleting ? 50 : 90);
}
typeLoop();

// ---- COUNTER ANIMATION ----
function animateCounters() {
  document.querySelectorAll('.stat-num').forEach(el => {
    const target = +el.dataset.count;
    let current = 0;
    const step = target / 40;
    const timer = setInterval(() => {
      current += step;
      if (current >= target) { el.textContent = target + (target > 1 ? '+' : ''); clearInterval(timer); }
      else el.textContent = Math.floor(current);
    }, 40);
  });
}

// ---- SCROLL REVEAL ----
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.section-header, .about-grid, .skill-group, .timeline-card, .project-card, .pub-card, .contact-item, .edu-card').forEach(el => {
  el.classList.add('fade-in');
  observer.observe(el);
});

// Counter trigger
const heroObserver = new IntersectionObserver(entries => {
  if (entries[0].isIntersecting) { animateCounters(); heroObserver.disconnect(); }
}, { threshold: 0.5 });
const heroStats = document.querySelector('.hero-stats');
if (heroStats) heroObserver.observe(heroStats);

// ---- NAVBAR ----
const navbar = document.getElementById('navbar');
const navToggle = document.getElementById('navToggle');
const navLinks = document.querySelector('.nav-links');
window.addEventListener('scroll', () => {
  navbar.style.background = window.scrollY > 20
    ? 'rgba(26,30,35,0.95)' : 'rgba(26,30,35,0.82)';
});
navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));

// ---- ACTIVE NAV ----
const sections = document.querySelectorAll('section[id]');
window.addEventListener('scroll', () => {
  let cur = '';
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 100) cur = s.id;
  });
  document.querySelectorAll('.nav-links a').forEach(a => {
    a.style.color = a.getAttribute('href') === '#' + cur ? 'var(--accent)' : '';
  });
});

// ---- AI QUIZ GAME ----
const quizData = [
  { q: "Which algorithm uses backpropagation for training?", opts: ["Decision Tree", "Neural Network", "K-Means", "SVM"], ans: 1 },
  { q: "What does RAG stand for in AI?", opts: ["Random Augmented Generation", "Retrieval Augmented Generation", "Rapid AI Graph", "Recursive Attention Gate"], ans: 1 },
  { q: "Which library is primarily used for deep learning in Python?", opts: ["Pandas", "Matplotlib", "PyTorch", "Seaborn"], ans: 2 },
  { q: "What is the purpose of a Transformer's attention mechanism?", opts: ["Data preprocessing", "Feature engineering", "Weigh input importance", "Normalize outputs"], ans: 2 },
  { q: "XGBoost is an optimized version of which technique?", opts: ["Random Forest", "Gradient Boosting", "Logistic Regression", "KNN"], ans: 1 },
  { q: "What does NLP stand for?", opts: ["Neural Learning Protocol", "Nonlinear Processing", "Natural Language Processing", "Normalized Layer Propagation"], ans: 2 },
  { q: "SHAP values are used for what purpose in ML?", opts: ["Model training", "Model explainability", "Data cleaning", "Hyperparameter tuning"], ans: 1 },
];

let qIdx = 0, score = 0;

function initQuiz() {
  qIdx = 0; score = 0;
  document.getElementById('quiz-start').style.display = 'none';
  document.getElementById('quiz-score').textContent = 'Score: 0/' + quizData.length;
  showQuestion();
}

function showQuestion() {
  if (qIdx >= quizData.length) {
    document.getElementById('quiz-question').textContent = '🎉 Quiz Complete!';
    document.getElementById('quiz-options').innerHTML = '';
    document.getElementById('quiz-score').textContent = `Final Score: ${score}/${quizData.length}`;
    document.getElementById('quiz-start').textContent = 'Play Again';
    document.getElementById('quiz-start').style.display = 'inline-flex';
    return;
  }
  const q = quizData[qIdx];
  document.getElementById('quiz-question').textContent = `Q${qIdx + 1}: ${q.q}`;
  const optsEl = document.getElementById('quiz-options');
  optsEl.innerHTML = '';
  q.opts.forEach((opt, i) => {
    const btn = document.createElement('button');
    btn.className = 'quiz-opt';
    btn.textContent = opt;
    btn.onclick = () => handleAnswer(i, btn, optsEl);
    optsEl.appendChild(btn);
  });
}

function handleAnswer(i, btn, optsEl) {
  const q = quizData[qIdx];
  Array.from(optsEl.children).forEach(b => b.disabled = true);
  if (i === q.ans) {
    btn.classList.add('correct'); score++;
  } else {
    btn.classList.add('wrong');
    optsEl.children[q.ans].classList.add('correct');
  }
  document.getElementById('quiz-score').textContent = `Score: ${score}/${quizData.length}`;
  qIdx++;
  setTimeout(showQuestion, 1200);
}

// ---- AI CHAT ----
async function sendChat() {
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';
  addChatMsg(msg, 'user');
  addChatMsg('...', 'bot', 'typing-msg');
  try {
    const res = await fetch('/api/chat/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg }),
    });
    const data = await res.json();
    const typing = document.querySelector('.typing-msg');
    if (typing) typing.querySelector('.msg-bubble').textContent = data.reply;
    if (typing) typing.classList.remove('typing-msg');
  } catch {
    document.querySelector('.typing-msg .msg-bubble').textContent = 'Signal lost. Try again!';
  }
}
document.getElementById('chatInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') sendChat();
});

function addChatMsg(text, role, extraClass = '') {
  const wrap = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = `chat-msg ${role} ${extraClass}`;
  div.innerHTML = role === 'bot'
    ? `<span class="bot-avatar">🤖</span><div class="msg-bubble">${text}</div>`
    : `<div class="msg-bubble">${text}</div>`;
  wrap.appendChild(div);
  wrap.scrollTop = wrap.scrollHeight;
}

// ---- FEEDBACK FORM ----
async function submitFeedback(e) {
  e.preventDefault();
  const name = document.getElementById('fb-name').value;
  const email = document.getElementById('fb-email').value;
  const message = document.getElementById('fb-msg').value;
  const result = document.getElementById('fb-result');

  try {
    const res = await fetch('/api/feedback/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, message }),
    });
    const data = await res.json();
    result.textContent = data.msg || 'Submitted!';
    document.getElementById('feedbackForm').reset();
    setTimeout(() => result.textContent = '', 3000);
  } catch {
    result.textContent = 'Error submitting. Please try again.';
  }
}

// ---- FILE UPLOAD SIMULATION ----
const fileInput = document.getElementById('fileInput');
const uploadZone = document.getElementById('uploadZone');
const uploadResult = document.getElementById('uploadResult');

uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.style.borderColor = 'var(--accent)'; });
uploadZone.addEventListener('dragleave', () => uploadZone.style.borderColor = '');
uploadZone.addEventListener('drop', e => {
  e.preventDefault(); uploadZone.style.borderColor = '';
  const file = e.dataTransfer.files[0];
  if (file) showUpload(file);
});
fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) showUpload(fileInput.files[0]);
});

function showUpload(file) {
  uploadResult.innerHTML = `✅ <strong>${file.name}</strong> (${(file.size / 1024).toFixed(1)} KB) — uploaded successfully!`;
  setTimeout(() => uploadResult.innerHTML = '', 5000);
}
