import streamlit as st
import pandas as pd
from gtts import gTTS
import os

# إعداد الصفحة
st.set_page_config(page_title="📚 مكتبة التراث الصوتية", layout="wide")

# إعداد الخطوط والألوان
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .title {
        color: #1565C0;
        font-size: 32px;
        font-weight: 700;
        text-align: center;
    }
    .card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 10px;
    }
    .stButton button {
        background-color: #1565C0;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<p class='title'>📚 مكتبة التراث الصوتية</p>", unsafe_allow_html=True)
st.markdown("### استعرض الوثائق بسهولة واستمع للنص مباشرة.")

# رابط CSV
csv_url = "https://raw.githubusercontent.com/Ahmed-Mohamed-Ali2023/heritage-audio-library/refs/heads/main/heritage_texts.csv"

# تحميل البيانات
with st.spinner("📥 يتم تحميل البيانات من GitHub..."):
    try:
        data = pd.read_csv(csv_url)
        st.success("✅ تم تحميل البيانات بنجاح.")
    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء تحميل البيانات: {e}")
        st.stop()

# إنشاء مجلد الملفات الصوتية
if not os.path.exists('audio_files'):
    os.makedirs('audio_files')

# توليد الملفات الصوتية
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

# تقسيم الأعمدة: عمود النتائج (يسار) وعمود البحث (يمين)
col_content, col_select = st.columns([3, 1], gap="large", reversed=True)

# ==== عمود البحث - على اليمين ====
with col_select:
    st.markdown("""
        <div style='background-color: #E3F2FD; padding: 20px; border-radius: 10px;'>
    """, unsafe_allow_html=True)

    st.markdown("## 🔍 البحث والاختيار")

    search_col1, search_col2 = st.columns([3, 1])
    search_query = search_col1.text_input("🔎 ابحث في العنوان أو المؤلف:", label_visibility="collapsed", placeholder="اكتب كلمة للبحث...")
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

    st.markdown("</div>", unsafe_allow_html=True)

# ==== عمود النتائج - على اليسار ====
with col_content:
    if selected_title != "-- اختر وثيقة --":
        row = filtered_data[filtered_data['Title'] == selected_title].iloc[0]
        safe_title = "".join(c for c in row['Title'] if c.isalnum() or c in (' ', '_', '-')).rstrip()
        audio_file = f"audio_files/{safe_title}.mp3"

        # بطاقة عرض جذابة
        st.markdown(f"""
            <div class='card'>
                <img src="{row['Image']}" width="100%" style="border-radius: 10px; max-height: 300px; object-fit: cover; margin-bottom: 10px;">
                <h2 style="color:#0D47A1; text-align:center;">📖 {row['Title']}</h2>
                <p><b>✍️ المؤلف:</b> {row['Author']}</p>
                <p><b>📅 سنة النشر:</b> {row['Year']}</p>
                <p><b>🏢 الناشر:</b> {row['Publisher']}</p>
                <p><b>🏷️ المجال:</b> {row['Field']}</p>
                <p><b>📄 عدد الصفحات:</b> {row['Pages']}</p>
                <h4>📜 النص:</h4>
                <p>{row['Text'][:1500] + "..." if len(row['Text']) > 1500 else row['Text']}</p>
            </div>
        """, unsafe_allow_html=True)

        if os.path.exists(audio_file):
            st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("⚠️ الملف الصوتي غير متوفر.")
    else:
        st.info("📑 اختر وثيقة من القائمة اليمنى للاطلاع على التفاصيل.")
