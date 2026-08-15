import json
import urllib.request
import urllib.error
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Feedback, ChatLog

# ─── KARIB SHAMS — FULL PORTFOLIO DATA ───────────────────────────────────────
DATA = {
    "name": "Karib Shams",
    "title": "Data Scientist & AI Developer",
    "email": "shams321karib@gmail.com",
    "phone": "01797470717",
    "whatsapp": "01797470717",
    "location": "93 South Bashabo, Dhaka-1214, Bangladesh",
    "github": "https://github.com/karibshams",
    "linkedin": "https://linkedin.com/in/karib-shams-007975305",
    "scholar": "https://scholar.google.com/citations?user=C26dtwMAAAAJ&hl=en",
    "portfolio_url": "https://shams123.pythonanywhere.com",
    "citations": 9,
    "h_index": 2,
    "about": (
        "Strong foundation in AI, machine learning, and deep learning with hands-on experience "
        "in computer vision, NLP, knowledge graphs, and explainable AI. Experienced in building "
        "AI-powered automation systems using LLMs, RAG pipelines, and workflow orchestration "
        "tools like n8n. Proven ability to solve complex problems through innovative technology "
        "solutions, and committed to continuous learning in cutting-edge AI methodologies."
    ),
    "team": {
        "name": "AI Stream",
        "projects_count": "60+",
        "desc": (
            "I lead AI Stream — a dedicated AI & software team that has delivered 60+ web and "
            "mobile projects. Our work spans AI-powered web apps, automation pipelines, RAG "
            "systems, voice AI, and full-stack SaaS products across healthcare, education, "
            "agriculture, and business domains."
        ),
    },
    "skills": {
        "Programming": ["Python", "JavaScript", "HTML/CSS", "SQL", "C/C++", "Java", "Django"],
        "AI & ML": ["Deep Learning", "Computer Vision", "NLP", "Explainable AI (XAI)",
                    "Knowledge Graphs", "Sentiment Analysis", "Semi-Supervised Learning",
                    "Self-Supervised Learning", "RAG Pipelines", "LLM Chaining"],
        "Automation & Orchestration": ["n8n Workflows", "Webhook Systems", "API Orchestration",
                                        "AI Workflow Integration", "Prompt Engineering"],
        "Tools & Platforms": ["Jupyter Notebook", "Google Colab", "Roboflow", "Kaggle",
                               "Oracle APEX", "Cisco Packet Tracer", "Visual Studio Code",
                               "Linux Admin", "Windows PowerShell"],
    },
    "experience": [
        {
            "company": "Join Venture AI (JVai), Betopia Group",
            "role": "Senior Executive Data Scientist | Team Leader",
            "period": "06/2025 – Present",
            "location": "Dhaka, Bangladesh",
            "desc": ("Led R&D efforts and managed the night team while developing AI-driven "
                     "solutions — chatbots, RAG-based NLP systems, n8n automation workflows — "
                     "and collaborating with sales to boost lead generation."),
        },
        {
            "company": "East West University",
            "role": "Graduate Teaching Assistant (GTA)",
            "period": "10/2024 – 12/2025",
            "location": "Dhaka, Bangladesh",
            "desc": ("Taught Statistics, AI, and Machine Learning. Led discussions and mentored "
                     "students in advanced ML, data analysis, and research methodology."),
        },
        {
            "company": "East West University",
            "role": "Research Assistant",
            "period": "10/2024 – 12/2025",
            "location": "Dhaka, Bangladesh",
            "desc": "Contributing to academic research in Data Science, AI, and Machine Learning.",
        },
    ],
    "projects": [
        # Professional
        {"name": "EmoThrive – AI Therapy Assistant", "type": "Professional",
         "desc": "AI-powered therapeutic assistant with voice interaction, LLM-based therapy, and PDF-backed RAG knowledge retrieval.",
         "link": "https://emothrive.net/", "tags": ["LLM", "Voice AI", "RAG", "Healthcare"]},
        {"name": "OP Mental Performance AI Coach", "type": "Professional",
         "desc": "AI coaching platform for athletes and professionals targeting optimal mental performance.",
         "link": "https://optimalperformanceai.com/", "tags": ["AI Coach", "NLP", "LLM"]},
        {"name": "VoiceMind AI Mental Wellness App", "type": "Professional",
         "desc": "Mental wellness mobile app powered by voice AI and large language models.",
         "link": "https://lnkd.in/gFUFHn98", "tags": ["Voice AI", "Mental Health", "Mobile"]},
        {"name": "EduGPT – PDF Academic Chatbot", "type": "Professional",
         "desc": "PDF-powered RAG academic chatbot for CSE and EEE students at East West University.",
         "link": "https://github.com/karibshams/cseeeegpt1.0.git", "tags": ["RAG", "Chatbot", "Education"]},
        {"name": "OCR Text Extraction System", "type": "Professional",
         "desc": "Robust OCR pipeline for extracting and processing text from scanned documents and images.",
         "link": "https://github.com/karibshams/simple_ocr.git", "tags": ["OCR", "Computer Vision"]},
        {"name": "MystudyBuddy App", "type": "Professional",
         "desc": "Smart AI study companion to enhance student productivity and personalised learning outcomes.",
         "link": "#", "tags": ["EdTech", "AI", "Productivity"]},
        {"name": "n8n AI Video Generation Automation", "type": "Professional",
         "desc": "Automated pipelines for AI-based video creation using n8n, Runway ML, and external APIs.",
         "link": "#", "tags": ["n8n", "Automation", "Video AI"]},
        {"name": "RAG-Based AI System", "type": "Professional",
         "desc": "Context-aware RAG pipeline for enterprise knowledge retrieval using embeddings and LLMs.",
         "link": "#", "tags": ["RAG", "LLM", "Embeddings"]},
        # Academic
        {"name": "Vehicle Detection & Traffic Prediction", "type": "Academic",
         "desc": "Deep learning system for vehicle detection and real-time traffic flow prediction on Bangladeshi urban roads.",
         "link": "#", "tags": ["Computer Vision", "YOLO", "Traffic AI"]},
        {"name": "Sunflower & Rice Panicle Detection", "type": "Academic",
         "desc": "Self-supervised visual representation learning for precision agriculture — comparative ablation study.",
         "link": "#", "tags": ["Self-Supervised", "AgriAI", "Vision"]},
        {"name": "AI Stream — 60+ Team Projects", "type": "Team",
         "desc": "Led AI Stream team delivering 60+ web and mobile AI products spanning healthcare, education, e-commerce, and business automation.",
         "link": "https://docs.google.com/spreadsheets/d/1fthxg82tjNCc3PP6Ik9e2B1BkEmryOysXDD7Hh_XgoU/edit",
         "tags": ["Team Lead", "60+ Projects", "Full-Stack", "AI"]},
    ],
    "publications": [
        {
            "title": "CodeMixEcom-Emotion: A Large-Scale Bangla–English Review Corpus and Transformer-Based Benchmark for Fine-Grained Emotion Detection",
            "venue": "AII 2025, Springer-Nature CCIS (Washington D.C., USA)",
            "award": "🏆 Best Paper Award",
            "cited": 0,
            "doi": "",
        },
        {
            "title": "Towards Annotation-Efficient Kidney CT Scan Classification: Supervised and Semi-Supervised Swin Transformer Frameworks",
            "venue": "IEEE SPICSCON 2025",
            "award": "",
            "cited": 0,
            "doi": "",
        },
        {
            "title": "Histopathology Images-Based Deep Learning Prediction of Prognosis and Therapeutic Response in Small Cell Lung Cancer",
            "venue": "ICDMIS 2024, Springer (Data Mining and Information Security, Vol. 5)",
            "award": "",
            "cited": 0,
            "doi": "",
        },
        {
            "title": "TFP-BD: An Image Dataset for Traffic Flow and Pedestrian Movement Analysis on Bangladeshi Urban Roads",
            "venue": "Data in Brief, Vol. 59, 2025, p.111398",
            "award": "",
            "cited": 2,
            "doi": "",
        },
        {
            "title": "Tuberculosis Diagnosis from Chest X-Ray Image Using Deep Learning Techniques",
            "venue": "IEEE ICAECT 2025 — DOI: 10.1109/ICAECT63952.2025.10958925",
            "award": "",
            "cited": 1,
            "doi": "10.1109/ICAECT63952.2025.10958925",
        },
        {
            "title": "Real-Time Monitoring of Oyster Mushroom Cultivation Using CCTV and Attention-Enhanced ShuffleNet-Based Explainable AI Techniques",
            "venue": "Smart Agricultural Technology, Vol. 12, 2025, p.101571",
            "award": "",
            "cited": 1,
            "doi": "10.1016/j.atech.2025.101571",
        },
        {
            "title": "Interpretable Illness-Category Classification from Drug Attributes Using XGBoost with SHAP Explanations",
            "venue": "IEEE QPAIN 2025 — DOI: 10.1109/QPAIN66474.2025.11172160",
            "award": "",
            "cited": 1,
            "doi": "10.1109/QPAIN66474.2025.11172160",
        },
        {
            "title": "Real-Time Sunflower Detection Using Semi-Supervised and Self-Supervised Deep Learning for Precision Agriculture",
            "venue": "Smart Agricultural Technology, 2025, p.101684",
            "award": "",
            "cited": 2,
            "doi": "",
        },
        {
            "title": "BDFlower: Growth Stage Flower Image Dataset for Precision Agriculture and Floriculture",
            "venue": "Data in Brief, 2026, p.112745",
            "award": "",
            "cited": 1,
            "doi": "",
        },
        {
            "title": "Benchmarking Hybrid CNN and Transformer Backbones with Graph Convolution Networks (GCN) for Flower Growth-Stage Classification",
            "venue": "Scientific Reports, 2026",
            "award": "",
            "cited": 0,
            "doi": "",
        },
        {
            "title": "Semi-Supervised Deep Learning for Early Detection of Bone Metastases in Adult Breast Cancer Patients",
            "venue": "IEEE BIBE 2025",
            "award": "",
            "cited": 0,
            "doi": "",
        },
        {
            "title": "Maternal Health Risk Assessment with Interpretable Machine Learning: Evidence from Bangladesh",
            "venue": "IEEE SPICSCON 2025",
            "award": "",
            "cited": 0,
            "doi": "",
        },
        {
            "title": "Occlusion-Resilient Surgical Instrument Detection Using Self-Supervised Learning and YOLO Models",
            "venue": "IEEE BIBE 2025",
            "award": "",
            "cited": 0,
            "doi": "",
        },
        {
            "title": "Leveraging Semi-Supervised Learning for Multimodal Medical Image Classification with Paired CT and MRI",
            "venue": "ICCIT 2025",
            "award": "",
            "cited": 0,
            "doi": "",
        },
        {
            "title": "Explainable Random Forest Framework for Real-Time Indoor Air-Quality Prediction at Airports Using SCD30 Sensor Data",
            "venue": "IEEE QPAIN 2025",
            "award": "",
            "cited": 0,
            "doi": "",
        },
        {
            "title": "Smartphone-Based Multi-Criteria Vegetable Object Detection Dataset from Bangladesh",
            "venue": "Data in Brief, 2025, p.112281",
            "award": "",
            "cited": 1,
            "doi": "",
        },
    ],
    "education": [
        {"degree": "MSc. in CSE", "institution": "East West University", "period": "01/2025 – 12/2025", "detail": "CGPA: 3.91 | Major: Data Science"},
        {"degree": "B.Sc. in CSE", "institution": "East West University", "period": "01/2020 – 07/2024", "detail": "CGPA: 3.58"},
        {"degree": "HSC", "institution": "National Ideal College", "period": "2017 – 2019", "detail": "GPA: 4.67"},
        {"degree": "SSC", "institution": "Motijheel Model School And College", "period": "2016 – 2017", "detail": "GPA: 5.00"},
    ],
    "references": [
        {"name": "Mohammad Rifat Ahmmad Rashid", "title": "Associate Professor, East West University", "email": "rifat.rashid@ewubd.edu"},
        {"name": "Musharrat Khan", "title": "Senior Lecturer, East West University", "email": "musharrat.khan@ewubd.edu"},
    ],
}

# ─── SYSTEM PROMPT FOR KARIB AI ───────────────────────────────────────────────
KARIB_SYSTEM_PROMPT = """You are Karib Shams's personal AI assistant embedded in his portfolio website.
You have two roles:
1. Answer questions ABOUT Karib Shams using the detailed biography below.
2. Answer general questions about AI, Machine Learning, Data Science, and Computer Science as a knowledgeable expert.

=== ABOUT KARIB SHAMS ===
Name: Karib Shams
Title: Data Scientist & AI Developer
Email: shams321karib@gmail.com | Phone: 01797470717
Location: Dhaka, Bangladesh
GitHub: https://github.com/karibshams
LinkedIn: https://linkedin.com/in/karib-shams-007975305
Google Scholar: https://scholar.google.com/citations?user=C26dtwMAAAAJ
Portfolio: https://shams123.pythonanywhere.com
Google Scholar Stats: 9 citations, h-index: 2

EDUCATION:
- MSc in CSE, East West University (2025), CGPA 3.91, Major: Data Science
- BSc in CSE, East West University (2020–2024), CGPA 3.58

EXPERIENCE:
- Senior Executive Data Scientist & Team Leader at JVai (Betopia Group), June 2025–Present
  → Builds chatbots, RAG NLP systems, n8n automation workflows
- Graduate Teaching Assistant at East West University (Oct 2024 – Dec 2025)
  → Taught Statistics, AI, Machine Learning
- Research Assistant at East West University (Oct 2024 – Dec 2025)

TEAM: Leads "AI Stream" — delivered 60+ web and mobile AI projects covering healthcare, education, e-commerce, and business automation.

SKILLS: Python, Django, JavaScript, SQL, Deep Learning, Computer Vision, NLP, RAG, LLMs, XAI (SHAP), n8n, Roboflow, Kaggle, Jupyter, Linux Admin

PUBLICATIONS (16 total, 9 citations, h-index 2):
- Best Paper Award: "CodeMixEcom-Emotion" — AII 2025, Washington D.C. (Springer)
- TB Diagnosis from Chest X-Ray — IEEE ICAECT 2025
- Kidney CT Scan Classification (Swin Transformer) — IEEE SPICSCON 2025
- Small Cell Lung Cancer Histopathology — ICDMIS 2024 Springer
- TFP-BD Traffic Dataset — Data in Brief 2025 (2 citations)
- Oyster Mushroom XAI Monitoring — Smart Agricultural Technology 2025
- XGBoost SHAP Drug Classification — IEEE QPAIN 2025
- Sunflower Detection Semi-Supervised — Smart Agricultural Technology 2025 (2 citations)
- BDFlower Dataset — Data in Brief 2026
- Benchmarking CNN+Transformer+GCN — Scientific Reports 2026
- Bone Metastases Detection — IEEE BIBE 2025
- Maternal Health Risk — IEEE SPICSCON 2025
- Surgical Instrument Detection (YOLO) — IEEE BIBE 2025
- Multimodal CT+MRI Classification — ICCIT 2025
- Air Quality XAI (Airport) — IEEE QPAIN 2025
- Vegetable Detection Dataset — Data in Brief 2025

PROFESSIONAL PROJECTS:
- EmoThrive (emothrive.net): AI therapy with voice + RAG
- OP Mental Performance AI Coach (optimalperformanceai.com)
- VoiceMind Mental Wellness App
- EduGPT: PDF academic chatbot for CSE/EEE students
- OCR Text Extraction System (GitHub)
- n8n AI Video Generation Automation
- RAG-Based Enterprise AI System

=== YOUR BEHAVIOR ===
- For personal questions about Karib → answer using above data, be specific and enthusiastic
- For AI/ML/Data Science questions → give expert, accurate, educational answers
- Keep answers concise but complete (2–5 sentences unless detail is needed)
- Be friendly, professional, and slightly futuristic in tone
- If asked something you don't know → say so honestly
- Never make up publications, projects, or facts about Karib
"""


def index(request):
    feedbacks = Feedback.objects.order_by('-created_at')[:8]
    pub_count = len(DATA["publications"])
    proj_count = len([p for p in DATA["projects"] if p["type"] in ("Professional", "Academic")])
    return render(request, 'portfolio/index.html', {
        'data': DATA,
        'pub_count': pub_count,
        'proj_count': proj_count,
        'feedbacks': feedbacks,
    })


@csrf_exempt
def ai_chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    try:
        body = json.loads(request.body)
        user_msg = body.get('message', '').strip()
        history = body.get('history', [])  # list of {role, content}
        if not user_msg:
            return JsonResponse({'reply': 'Please type a message!'})

        # Build messages
        messages = []
        for h in history[-8:]:  # Keep last 8 exchanges for context
            if h.get('role') in ('user', 'assistant') and h.get('content'):
                messages.append({'role': h['role'], 'content': h['content']})
        messages.append({'role': 'user', 'content': user_msg})

        payload = json.dumps({
            'model': 'claude-sonnet-4-6',
            'max_tokens': 500,
            'system': KARIB_SYSTEM_PROMPT,
            'messages': messages,
        }).encode('utf-8')

        req = urllib.request.Request(
            'https://api.anthropic.com/v1/messages',
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'anthropic-version': '2023-06-01',
                # API key injected by PythonAnywhere / environment
                # For local dev: set ANTHROPIC_API_KEY in environment
                # The claude.ai artifact environment injects it automatically
            },
            method='POST'
        )

        # Try to get API key from environment
        import os
        api_key = os.environ.get('ANTHROPIC_API_KEY', '')
        if api_key:
            req.add_header('x-api-key', api_key)

        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            reply = data['content'][0]['text']

        ChatLog.objects.create(user_message=user_msg, ai_reply=reply)
        return JsonResponse({'reply': reply})

    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        # Fallback: smart rule-based reply
        reply = _smart_fallback(user_msg)
        return JsonResponse({'reply': reply})
    except Exception as e:
        reply = _smart_fallback(body.get('message', ''))
        return JsonResponse({'reply': reply})


def _smart_fallback(msg):
    """Smart fallback replies when API key is not configured."""
    msg = msg.lower()
    if any(w in msg for w in ['publication', 'paper', 'research', 'cited', 'scholar']):
        return ("Karib has 16 publications across IEEE, Springer, Elsevier, and Nature Portfolio, "
                "with 9 citations and an h-index of 2. His Best Paper Award was at AII 2025 in Washington D.C. "
                "for CodeMixEcom-Emotion — a Bangla-English emotion detection benchmark.")
    if any(w in msg for w in ['project', 'team', 'ai stream', 'built', 'work']):
        return ("Karib leads AI Stream — a team that has delivered 60+ web and mobile AI projects. "
                "Notable work includes EmoThrive (AI therapy), EduGPT (RAG chatbot), and multiple n8n automation pipelines.")
    if any(w in msg for w in ['skill', 'language', 'tech', 'stack', 'python', 'django']):
        return ("Karib is proficient in Python, Django, JavaScript, SQL, and various AI frameworks. "
                "He specialises in RAG pipelines, LLM chaining, XAI (SHAP), Computer Vision, and n8n workflow automation.")
    if any(w in msg for w in ['rag', 'retrieval', 'augmented', 'generation']):
        return ("RAG (Retrieval-Augmented Generation) grounds LLM outputs in retrieved factual documents, "
                "dramatically reducing hallucinations. Karib has built multiple RAG systems including EduGPT and EmoThrive.")
    if any(w in msg for w in ['llm', 'large language', 'gpt', 'transformer', 'bert']):
        return ("Large Language Models like GPT-4 and Claude are trained on vast text corpora using the Transformer "
                "architecture with self-attention. Karib uses LLMs extensively in his RAG systems and AI products.")
    if any(w in msg for w in ['contact', 'hire', 'email', 'whatsapp', 'reach']):
        return ("You can reach Karib at shams321karib@gmail.com or WhatsApp: 01797470717. "
                "He's open to AI development, research collaborations, and freelance projects.")
    if any(w in msg for w in ['education', 'university', 'degree', 'cgpa', 'gpa']):
        return ("Karib holds a BSc in CSE (CGPA 3.58) and an MSc in CSE specialising in Data Science (CGPA 3.91), "
                "both from East West University, Dhaka, Bangladesh.")
    if any(w in msg for w in ['xai', 'explainable', 'shap', 'interpret']):
        return ("Explainable AI (XAI) makes ML models interpretable. SHAP (SHapley Additive exPlanations) assigns "
                "feature importance values. Karib has published on XAI for drug classification and agricultural monitoring.")
    return ("I'm Karib's AI assistant! I can answer questions about his research, projects, skills, "
            "or any AI/ML topic. Note: full AI mode requires an API key configured in the Django settings.")


@csrf_exempt
def submit_feedback(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)
    try:
        body = json.loads(request.body)
        Feedback.objects.create(
            name=body.get('name', ''),
            email=body.get('email', ''),
            message=body.get('message', ''),
        )
        return JsonResponse({'status': 'ok', 'msg': '✅ Thank you! Your feedback has been saved.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)
