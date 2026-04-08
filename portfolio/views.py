from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Feedback, ChatMessage
import json, random

PORTFOLIO_DATA = {
    "name": "Karib Shams",
    "title": "Data Scientist & AI Developer",
    "email": "shams321karib@gmail.com",
    "phone": "01797470717",
    "whatsapp": "01797470717",
    "location": "93 South Bashabo, Dhaka-1214, Bangladesh",
    "github": "https://github.com/karibshams",
    "linkedin": "https://linkedin.com/in/karib-shams-007975305",
    "about": "Strong foundation in AI, machine learning, and deep learning with hands-on experience in computer vision, NLP, knowledge graphs, and explainable AI. Proven ability to solve complex problems through innovative technology solutions. Committed to continuous learning and development in cutting-edge AI methodologies.",
    "languages_spoken": [
        {"lang": "English", "level": "Advanced (C1)"},
        {"lang": "Bengali", "level": "Native"},
    ],
    "skills": {
        "Programming": ["Python", "JavaScript", "HTML/CSS", "SQL", "C/C++", "Java"],
        "AI & ML": ["Deep Learning", "Computer Vision", "NLP", "Explainable AI", "Knowledge Graphs", "Sentiment Analysis"],
        "Tools & Platforms": ["Jupyter Notebook", "Google Colab", "Roboflow", "Kaggle", "Oracle APEX", "Cisco Packet Tracer"],
        "Other": ["Linux Admin", "Neural Network Design", "Graph Theory", "Data Screening", "SQL Database Mgmt"],
    },
    "experience": [
        {
            "company": "Join Venture Ai (JVai), Betopia Group",
            "role": "Data Scientist | Team Leader",
            "period": "06/2025 – Present",
            "location": "Dhaka, Bangladesh",
            "desc": "Led R&D efforts and managed the night team while developing AI-driven solutions, such as chatbots and RAG-based NLP systems, and collaborating with sales to boost lead generation and overall performance.",
        },
        {
            "company": "East West University",
            "role": "Graduate Teaching Assistant (GTA)",
            "period": "10/2024 – 12/2025",
            "location": "Dhaka, Bangladesh",
            "desc": "Taught Statistics, AI, and Machine Learning while leading discussions and mentoring students in advanced ML and data analysis.",
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
        {"name": "EmoThrive – AI Therapy Assistant", "desc": "AI-powered therapeutic assistant offering warm, empathetic support through voice interaction, LLM-based therapy, and PDF-backed knowledge retrieval.", "link": "https://emothrive.net/", "tags": ["LLM", "Voice AI", "RAG"]},
        {"name": "OP Mental Performance AI Coach", "desc": "AI coaching platform for optimal mental performance and athletic excellence.", "link": "https://optimalperformanceai.com/", "tags": ["AI Coach", "NLP", "LLM"]},
        {"name": "VoiceMind AI Mental Wellness App", "desc": "Mental wellness application powered by voice AI and large language models.", "link": "https://lnkd.in/gFUFHn98", "tags": ["Voice AI", "Mental Health", "Mobile"]},
        {"name": "EduGPT – PDF Academic Chatbot", "desc": "PDF-powered academic chatbot for CSE and EEE students built with RAG architecture.", "link": "https://github.com/karibshams/cseeeegpt1.0.git", "tags": ["RAG", "Chatbot", "Education"]},
        {"name": "OCR Text Extraction System", "desc": "Robust OCR pipeline for extracting and processing text from scanned documents.", "link": "https://github.com/karibshams/simple_ocr.git", "tags": ["OCR", "Computer Vision", "Python"]},
        {"name": "MystudyBuddy App", "desc": "Smart study companion application to enhance student productivity and learning outcomes.", "link": "#", "tags": ["EdTech", "AI", "Productivity"]},
        {"name": "Vehicle Detection & Traffic Prediction", "desc": "Deep learning system for vehicle detection and real-time traffic flow prediction on Bangladeshi urban roads.", "link": "#", "tags": ["Computer Vision", "YOLO", "Traffic AI"]},
        {"name": "Sunflower & Rice Panicle Detection", "desc": "Self-supervised visual representation learning for agricultural applications using comparative ablation study.", "link": "#", "tags": ["Self-Supervised", "AgriAI", "Vision"]},
    ],
    "publications": [
        {"title": "CodeMixEcom-Emotion: A Large-Scale Bangla–English Review Corpus and Transformer-Based Benchmark for Fine-Grained Emotion Detection", "venue": "AII 2025, Springer-Nature CCIS", "award": "🏆 Best Paper Award – Washington D.C., USA"},
        {"title": "Towards Annotation-Efficient Kidney CT Scan Classification: Supervised and Semi-Supervised Swin Transformer Frameworks", "venue": "IEEE SPICSCON 2025", "award": ""},
        {"title": "Histopathology images-based deep learning prediction of prognosis and therapeutic response in small cell lung cancer", "venue": "ICDMIS 2024, Springer", "award": ""},
        {"title": "TFP-BD: An image dataset for Traffic Flow and Pedestrian movement analysis on Bangladeshi urban roads", "venue": "Data in Brief, Vol. 59 (2025)", "award": ""},
        {"title": "Tuberculosis Diagnosis from Chest X-Ray Image Using Deep Learning Techniques", "venue": "ICAECT 2025, IEEE", "award": ""},
        {"title": "Real-time monitoring of oyster mushroom cultivation using CCTV and attention-enhanced ShuffleNet-based explainable AI techniques", "venue": "Smart Agricultural Technology, Vol. 12 (2025)", "award": ""},
        {"title": "Interpretable Illness-Category Classification from Drug Attributes Using XGBoost with SHAP Explanations", "venue": "QPAIN 2025, IEEE", "award": ""},
    ],
    "education": [
        {"degree": "MSc. in CSE", "institution": "East West University", "period": "01/2025 – 12/2025", "detail": "CGPA: 3.91 | Major: Data Science"},
        {"degree": "B.Sc. in CSE", "institution": "East West University", "period": "01/2020 – 07/2024", "detail": "CGPA: 3.58"},
        {"degree": "HSC", "institution": "National Ideal College", "period": "2017 – 2019", "detail": "GPA: 4.67"},
        {"degree": "SSC", "institution": "Motijheel Model School And College", "period": "2016 – 2017", "detail": "GPA: 5.00"},
    ],
    "award": "🏆 Best Paper Award – AII 2025, Washington D.C., USA",
}

AI_REPLIES = [
    "That's a fascinating question! In AI, we often explore similar patterns through neural networks and probabilistic reasoning.",
    "Great point! Data-driven insights reveal that the answer lies in statistical modeling and deep pattern recognition.",
    "My training suggests this connects to explainable AI principles — transparency and interpretability matter most.",
    "Interesting! From a machine learning perspective, this is essentially an optimization problem worth exploring.",
    "As an AI assistant, I'd say the key is iterative learning — much like how transformer models refine embeddings.",
    "This reminds me of knowledge graph traversal — the connections between concepts reveal deeper meaning.",
    "From an NLP standpoint, context is everything. Your query has rich semantic potential!",
    "RAG-based systems would approach this by grounding the answer in retrieved, factual knowledge first.",
]

def index(request):
    feedbacks = Feedback.objects.order_by('-created_at')[:10]
    return render(request, 'portfolio/index.html', {'data': PORTFOLIO_DATA, 'feedbacks': feedbacks})

@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            Feedback.objects.create(
                name=body.get('name', ''),
                email=body.get('email', ''),
                message=body.get('message', ''),
            )
            return JsonResponse({'status': 'ok', 'msg': 'Thank you for your feedback!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_msg = body.get('message', '')
            reply = random.choice(AI_REPLIES)
            ChatMessage.objects.create(user_message=user_msg, bot_reply=reply)
            return JsonResponse({'reply': reply})
        except Exception as e:
            return JsonResponse({'reply': 'Neural network overloaded. Try again!'}, status=200)
    return JsonResponse({'status': 'error'}, status=405)
