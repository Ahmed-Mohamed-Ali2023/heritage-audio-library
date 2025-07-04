import streamlit as st
import pandas as pd
from gtts import gTTS
import os

# إعداد الصفحة
st.set_page_config(page_title="📚 مكتبة التراث الصوتية", layout="wide")

# تغيير لون خلفية الصفحة بالكامل إلى أسود داكن
st.markdown(
    """
    <style>
    body {
        background-color: #121212;  /* أسود داكن */
        color: #FFFFFF;             /* نص أبيض */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📚 مكتبة التراث الصوتية")
st.markdown("### استعرض الوثائق بسهولة واستمع للنص مباشرة.")

# ========= رابط الملف من GitHub بصيغة RAW ==========
csv_url = "https://raw.githubusercontent.com/Ahmed-Mohamed-Ali2023/heritage-audio-library/refs/heads/main/heritage_texts.csv"

# ========== قراءة الملف ==========
with st.spinner("📥 يتم تحميل البيانات من GitHub..."):
    try:
        data = pd.read_csv(csv_url)
        st.success("✅ تم تحميل البيانات بنجاح.")
    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء تحميل البيانات: {e}")
        st.stop()

# ========== إنشاء مجلد الملفات الصوتية ==========
if not os.path.exists('audio_files'):
    os.makedirs('audio_files')

# ========== توليد الملفات الصوتية إن لم تكن موجودة ==========
with st.spinner("📥 تجهيز الملفات الصوتية..."):
    for idx, row in data.iterrows():
        title = row['Title']
        text = str(row['Text'])[:3000]
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
        filename = f"audio_files/{safe_title}.mp3"
        if not os.path.exists(filename):
            tts = gTTS(text, lang='ar')
            tts.save(filename)
st.success("✅ الملفات الصوتية جاهزة.")

# ========== تقسيم الأعمدة ==========
col_content, col_select = st.columns([3, 1], gap="large")

with col_select:
    st.markdown("## 🔍 البحث والاختيار")

    search_col1, search_col2 = st.columns([3, 1])
    search_query = search_col1.text_input(
        "🔎 ابحث في العنوان أو المؤلف:",
        label_visibility="collapsed",
        placeholder="اكتب كلمة للبحث..."
    )
    search_button = search_col2.button("🔍 بحث")

    if "filtered_data" not in st.session_state:
        st.session_state.filtered_data = data

    if search_button:
        if search_query.strip():
            filtered_data = data[
                data['Title'].str.contains(search_query, case=False, na=False) |
                data['Author'].str.contains(search_query, case=False, na=False)
            ]
            st.session_state.filtered_data = filtered_data
            st.success(f"✅ تم العثور على {len(filtered_data)} وثيقة مطابقة.")
        else:
            st.session_state.filtered_data = data
            st.info("ℹ️ لم يتم إدخال كلمة بحث، يتم عرض جميع الوثائق.")

    filtered_data = st.session_state.filtered_data

    titles_list = filtered_data['Title'].tolist()
    selected_title = st.selectbox("📑 اختر الوثيقة:", ["-- اختر وثيقة --"] + titles_list)

# ========== عمود عرض النتائج مع خلفية رمادية داكنة ==========
with col_content:
    if selected_title != "-- اختر وثيقة --":
        row = filtered_data[filtered_data['Title'] == selected_title].iloc[0]

        st.markdown(
            f"""
            <div style='
                background-color: #333333;  /* رمادي داكن */
                color: #FFFFFF;              /* نص أبيض */
                padding: 20px;
                border-radius: 12px;
                border: 2px solid #555555;   /* لون إطار أفتح قليلاً */
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                text-align: right;
                direction: rtl;
                font-family: "Cairo", sans-serif;
            '>
                <img src="{row['Image']}" width="300" style="display: block; margin: auto; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); margin-bottom: 15px;">
                <h2 style="text-align: center;">📖 {row['Title']}</h2>
                <p><b>✍️ المؤلف:</b> {row['Author']}</p>
                <p><b>📅 سنة النشر:</b> {row['Year']}</p>
                <p><b>🏢 الناشر:</b> {row['Publisher']}</p>
                <p><b>🏷️ المجال:</b> {row['Field']}</p>
                <p><b>📄 عدد الصفحات:</b> {row['Pages']}</p>
                <h3>📜 النص:</h3>
                <p>{row['Text'][:1500] + "..." if len(row['Text']) > 1500 else row['Text']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        safe_title = "".join(c for c in row['Title'] if c.isalnum() or c in (' ', '_', '-')).rstrip()
        audio_file = f"audio_files/{safe_title}.mp3"
        if os.path.exists(audio_file):
            st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("⚠️ الملف الصوتي غير متوفر.")
    else:
        st.info("📑 اختر وثيقة من القائمة اليمنى للاطلاع على التفاصيل.")
