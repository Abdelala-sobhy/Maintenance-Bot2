import streamlit as st
import google.generativeai as genai

# دي الطريقة الوحيدة الصحيحة عشان البوت يشتغل أونلاين
if "API_KEY" in st.secrets:
    api_key = st.secrets["API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("خطأ: مفتاح الـ API غير موجود في إعدادات Secrets")
    st.stop() # بيوقف الكود هنا عشان ميعملش العطل الأحمر اللي بتشوفه
# تعليمات النظام (قاعدة المعرفة للأعطال)
SYSTEM_PROMPT = """
أنت مساعد تعليمي متخصص في صيانة الحاسب والموبايل.
نطاق عملك هو شرح الأعطال التالية (10 أعطال لكل قسم كحد أدنى):
1. الماذربورد (مثل: انتفاخ المكثفات، أعطال الـ BIOS، قصر الدائرة).
2. المعالج (مثل: ارتفاع الحرارة، عدم توافق السوكت).
3. الأقراص الصلبة والمدمجة (مثل: Bad Sectors، عدم التعرف على القرص).
4. اللابتوب (مثل: أعطال الشحن، كسر الشاشة الداخلي).
5. الموبايل (مثل: أعطال التاتش، البطارية، السوفت وير).
6. السوفت وير والأمن السيبراني (مثل: الفيروسات، اختراق الصلاحيات).
7. الشاشات والطابعات (مثل: Dead Pixels، حشر الورق).

عند السؤال عن عطل، التزم بالرد في 3 نقاط:
- وصف العطل.
- طريقة التشخيص بدقة.
- طريقة الإصلاح.

إذا ذكر المستخدم اسمه، رحب به بـ "Hi [Name]" وابدأ المساعدة.
"""

model = genai.GenerativeModel(
   model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# تصميم واجهة المستخدم
st.set_page_config(page_title="Maintenance Chatbot", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 المساعد التعليمي للأعطال التقنية")

# التفاعل الأول: طلب الاسم
if "user_name" not in st.session_state:
    name = st.text_input("مرحباً بك! ما هو اسمك؟")
    if name:
        st.session_state.user_name = name
        st.success(f"Hi {name}! كيف يمكنني مساعدتك في دراسة الأعطال اليوم؟")

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال الأسئلة
if prompt := st.chat_input("اسأل عن عطل معين (مثلاً: أعطال الشاشة)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
