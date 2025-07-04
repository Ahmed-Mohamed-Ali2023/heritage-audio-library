import streamlit as st
import pandas as pd
from gtts import gTTS
import os

# إعداد الخط (Cairo)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stButton button {
        background-color: #1E88E5;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
    }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="📚 مكتبة التراث الصوتية", layout="wide")
st.title("📚 مكتبة التراث الصوتية")
st.markdown("### استعرض الوثائق بسهولة واستمع للنص مباشرة.")

# رابط الملف
csv_url = "https://raw.githubusercontent.com/Ahmed-Mohamed-Ali2023/heritage-audio-library/refs/heads/main/heritage_texts.csv"

# قراءة البيانات
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

# تقسيم الأعمدة مع ألوان الخلفية
col_content, col_select = st.columns([3, 1], gap="large")

# ==== عمود البحث بخلفية مميزة ====
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

# ==== عمود النتائج بخلفية هادئة ====
with col_content:
    st.markdown("""
        <div style='background-color: #FAFAFA; padding: 20px; border-radius: 10px;'>
    """, unsafe_allow_html=True)

    if selected_title != "-- اختر وثيقة --":
        row = filtered_data[filtered_data['Title'] == selected_title].iloc[0]
        st.markdown(
            f"""
            <div style='text-align: right; direction: rtl; font-family: "Cairo", sans-serif;'>
                <img src="{row['Image']}" width="300" style="display: block; margin: auto; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <h2 style="text-align: center; color: #1565C0;">📖 {row['Title']}</h2>
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

    st.markdown("</div>", unsafe_allow_html=True)
