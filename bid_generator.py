# bid_generator.py
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MAX_PROPOSAL_LENGTH = 1500
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

router_client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)


# AlphaFusion Corporation profile
ALPHAFUSION_PROFILE = """
AlphaFusion Corporation is a next-generation technology company that bridges the power of Artificial Intelligence, Machine Learning, and Advanced Software Engineering to build intelligent solutions for the modern world. Our expertise spans finance, cybersecurity, automation, data analytics, cloud infrastructure, and full-stack development — empowering global businesses to innovate, scale, and lead with confidence.

We engineer intelligence into everything we build. Our teams combine deep technical expertise with a strong understanding of real-world business needs to deliver AI-powered software systems, custom applications, and next-generation digital platforms that drive measurable impact.

Core Domains:
1) AI & ML – Predictive modeling, NLP, computer vision, recommendation systems, autonomous decision engines.
2) Software & Web Development – Full-stack apps, APIs, enterprise-grade platforms (React, Next.js, Node.js, Python, etc.).
3) Fintech & Data Analytics – Advanced trading dashboards, AI-powered market forecasting (TradeShark engine), global data visualization.
4) Cybersecurity – Zero Trust architectures, threat detection, encryption, AI-driven security automation.
5) Automation & Cloud – Scalable cloud deployments (AWS, Azure, GCP), Kubernetes, DevOps, intelligent process automation.

Vision:
Redefine how businesses interact with technology — fusing AI, automation, and human creativity to empower innovation, trust, and transformation. Deliver intelligent systems that evolve with business needs.

Why Work With Us:
- Cross-disciplinary expertise across AI, enterprise platforms, and cloud systems.
- Custom-built solutions tailored to every business.
- End-to-end delivery from concept to deployment.
- Innovation-driven culture leveraging emerging technologies.
- Trusted by clients worldwide across finance, defense, healthcare, retail, and smart infrastructure.
"""

def generate_bid(project_title: str, project_desc: str, budget: str|None=None) -> str:
    try:
        prompt = f"""
You are an experienced corporate proposal writer representing **AlphaFusion Corporation**, a leader in AI, software engineering, automation, and cybersecurity.

Write a professional, institution-grade proposal for the following project:

Title: {project_title}
Description: {project_desc}
Budget: {budget or 'Not specified'}

Use this company profile for context:
{ALPHAFUSION_PROFILE}

Follow these rules strictly:
- Keep total length smaller than 1500 characters.
- Start with a short greeting: 'Hello,' (no client name).
- Maintain a confident, objective tone—no unnecessary gratitude (avoid phrases like "thank you for considering").
- Summarize AlphaFusion’s relevant expertise, past work, and credibility clearly.
- Include an **Approach** section in bullet points (4–5 points max).
- Mention budget/timeline only if relevant, but **never state or promise any hard deadlines**.
- End with a clear call-to-action (discussion, call, or demo).
- Close with:  
  `Best regards,`  
  `AlphaFusion Corporation`
- Do not include any extra commentary or explanation—return only the final polished proposal text.
- Avoid pleasantries like “thank you for considering” or “we appreciate your time.”
- Return only the final proposal text without extra commentary.
- Do NOT include any special tokens such as <begin_of_sentence>, <end_of_sentence>, or similar markers.
Return plain text only.

"""

        completion = router_client.chat.completions.create(model="deepseek/deepseek-chat-v3.1:free",messages=[
        {"role": "system", "content": "You are an experienced corporate proposal writer representing **AlphaFusion Corporation**, a leader in AI, software engineering, automation, and cybersecurity."},
        {"role": "user", "content": prompt}])

        response = completion.choices[0].message.content
        response = re.sub(r"<.*?>", "", response)
        response = response.strip()
        # Hard truncate if necessary
        if len(response) > MAX_PROPOSAL_LENGTH:
            response = response[:MAX_PROPOSAL_LENGTH].rsplit('.', 1)[0] + '.'
        return response
        # resp = client.chat.completions.create(
        #     model="gpt-5-mini",
        #     messages=[{"role":"user","content":prompt}],
        #     max_tokens=400,
        # )
        # return resp.choices[0].message.content.strip()

    except Exception as e:
        print(f"⚠️ AI proposal generation failed: {e}")
        # Fallback professional template
        fallback_proposal = f"""Hello,

I am pleased to submit my bid for '{project_title}'. At AlphaFusion Corporation, we specialize in developing intelligent and secure solutions across AI, machine learning, software engineering, cybersecurity, and automation. Our teams have successfully delivered enterprise-grade projects spanning fintech, defense, healthcare, smart infrastructure, and cloud platforms, consistently ensuring performance, scalability, and robust security.

Approach:
- Thoroughly analyze your project requirements to align with business objectives.
- Apply best practices and advanced technologies to execute tasks efficiently.
- Maintain proactive communication with regular updates and milestone reviews.
- Deliver a secure, scalable, and polished solution within the proposed timeline.
- Provide recommendations for next steps, implementation strategies, and risk mitigation.

We pride ourselves on engineering solutions that are not only technically sound but also tailored to the unique needs of our clients, ensuring measurable impact and long-term value. Our team leverages cutting-edge frameworks, automation, and AI-driven insights to optimize efficiency and innovation in every project. Budget: {budget or 'Negotiable'}

Best regards,
AlphaFusion Corporation
"""

        return fallback_proposal
