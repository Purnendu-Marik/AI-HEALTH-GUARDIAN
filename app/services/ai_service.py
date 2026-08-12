import os

from dotenv import load_dotenv
# from xai_sdk import Client
# from xai_sdk.chat import user
from groq import Groq

load_dotenv()

def build_health_prompt(
    age,
    gender,
    symptoms,
    sleep,
    activity,
    additional_info
):
    """
    Build a professional and structured prompt
    for AI Health Guardian.
    """

    symptom_text = ", ".join(symptoms) if symptoms else "None reported"

    prompt = f"""
You are the AI analysis engine of AI Health Guardian.

Your task is to analyze the user's self-reported health
information and provide clear, educational, preventive
health guidance.

USER INFORMATION
----------------
Age: {age}
Gender: {gender}
Symptoms: {symptom_text}
Sleep: {sleep}
Physical Activity: {activity}
Additional Information: {additional_info}


IMPORTANT SAFETY RULES
----------------------
- Do NOT provide a medical diagnosis.
- Do NOT claim that the user has a specific disease.
- Do NOT use absolute or certain medical claims.
- Do NOT recommend prescription medicines or dosages.
- Use cautious language such as "may", "could", or
  "might".
- Encourage professional medical advice when appropriate.


RESPONSE FORMAT
---------------
Return the response using EXACTLY these four sections:

🧠 Overall Health Insight

Give a short 2-3 sentence summary of the user's
reported health information.

🔎 Key Insights

Provide 2-4 important observations based only on
the information provided.

💡 Lifestyle Suggestions

Provide 3-5 practical and general lifestyle suggestions
related to sleep, physical activity, hydration,
nutrition, stress management, or healthy habits.

⚠️ When to Seek Professional Help

Explain briefly when the user should consider speaking
with a qualified healthcare professional, especially if
symptoms are persistent, worsening, severe, or concerning.


STYLE
-----
- Keep the response concise.
- Use simple, easy-to-understand language.
- Use bullet points where appropriate.
- Avoid unnecessary technical medical terminology.
- Do not repeat the user's information unnecessarily.
- Be supportive and neutral.
- Never create information that was not provided by the user.
"""

    return prompt

#     import os

# from dotenv import load_dotenv
# from xai_sdk import Client
# from xai_sdk.chat import user


# load_dotenv()


# def test_grok_connection():

#     api_key = os.getenv("XAI_API_KEY")

#     if not api_key:
#         raise ValueError(
#             "XAI_API_KEY was not found in the .env file."
#         )

#     client = Client(api_key=api_key)

#     chat = client.chat.create(
#         model="grok-4.5"
#     )

#     chat.append(
#         user("Reply with exactly: Grok connection successful")
#     )

#     response = chat.sample()

#     return response.content

def test_groq_connection():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY was not found in the .env file."
        )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: Groq connection successful"
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content

def generate_health_insights(health_data):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY was not found in the .env file."
        )

    client = Groq(api_key=api_key)

    prompt = build_health_prompt(
        age=health_data["age"],
        gender=health_data["gender"],
        symptoms=health_data["symptoms"],
        sleep=health_data["sleep"],
        activity=health_data["activity"],
        additional_info=health_data["additional_info"]
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are AI Health Guardian, an educational health "
                    "assistant. Provide general health insights, not a "
                    "medical diagnosis. Encourage professional medical "
                    "help when symptoms may require it."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

def parse_ai_insights(ai_response):
    """
    Convert the structured AI response into separate sections.
    """

    sections = {
        "overall": "",
        "key_insights": [],
        "suggestions": [],
        "professional_help": ""
    }

    current_section = None

    for line in ai_response.splitlines():

        line = line.strip()

        if not line:
            continue

        # Section 1
        if "Overall Health Insight" in line:
            current_section = "overall"
            continue

        # Section 2
        elif "Key Insights" in line:
            current_section = "key_insights"
            continue

        # Section 3
        elif "Lifestyle Suggestions" in line:
            current_section = "suggestions"
            continue

        # Section 4
        elif "When to Seek Professional Help" in line:
            current_section = "professional_help"
            continue


        # Store content
        if current_section == "overall":

            sections["overall"] += " " + line


        elif current_section == "key_insights":

            if line.startswith("•"):
                line = line[1:].strip()

            if line.startswith("-"):
                line = line[1:].strip()

            sections["key_insights"].append(line)


        elif current_section == "suggestions":

            if line.startswith("•"):
                line = line[1:].strip()

            if line.startswith("-"):
                line = line[1:].strip()

            sections["suggestions"].append(line)


        elif current_section == "professional_help":

            sections["professional_help"] += " " + line


    # Clean extra spaces

    sections["overall"] = sections["overall"].strip()

    sections["professional_help"] = (
        sections["professional_help"].strip()
    )

    return sections