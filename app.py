import streamlit as st
import pandas as pd
from gtts import gTTS
import os

st.set_page_config(page_title="📚 مكتبة التراث الصوتية", layout="wide")
st.title("📚 مكتبة التراث الصوتية")
st.markdown("### ابحث عن الوثائق، اختر الوثيقة، واستمع للنص بسهولة.")

uploaded_file = st.file_uploader(
    "📂 قم برفع ملف CSV يحتوي على الأعمدة (Title, Text, Author, Year, Image, Pages, Publisher, Field)",
    type=['csv']
)

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    if not os.path.exists('audio_files'):
        os.makedirs('audio_files')

    with st.spinner("📥 يتم تجهيز الملفات الصوتية..."):
        for idx, row in data.iterrows():
            title = row['Title']
            text = str(row['Text'])[:3000]
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
            filename = f"audio_files/{safe_title}.mp3"
            if not os.path.exists(filename):
                tts = gTTS(text, lang='ar')
                tts.save(filename)
    st.success("✅ تم تجهيز الملفات الصوتية")

    # البحث
    query = st.text_input("🔍 أدخل كلمة للبحث في العنوان أو المؤلف:")

    if query:
        query = query.strip().lower()
        filtered_data = data[
            data['Title'].str.lower().str.contains(query) |
            data['Author'].str.lower().str.contains(query)
        ]
    else:
        filtered_data = data

    if not filtered_data.empty:
        st.markdown(f"### 📝 عدد الوثائق المعروضة: {len(filtered_data)}")

        # قائمة بالعناوين للاختيار
        options = [f"{row['Title']} - {row['Author']} ({row['Year']})" for idx, row in filtered_data.iterrows()]
        selected_option = st.selectbox("📑 اختر الوثيقة لعرض التفاصيل:", options)

        if selected_option:
            selected_index = options.index(selected_option)
            row = filtered_data.iloc[selected_index]

            st.markdown("---")
            st.markdown(f"## 📖 {row['Title']}")
            st.image(row['Image'], width=300)
            st.markdown(f"**✍️ المؤلف:** {row['Author']}")
            st.markdown(f"**📅 سنة النشر:** {row['Year']}")
            st.markdown(f"**🏢 الناشر:** {row['Publisher']}")
            st.markdown(f"**🏷️ المجال:** {row['Field']}")
            st.markdown(f"**📄 عدد الصفحات:** {row['Pages']}")

            st.markdown("### 📜 النص:")
            st.write(row['Text'][:1500] + "..." if len(row['Text']) > 1500 else row['Text'])

            safe_title = "".join(c for c in row['Title'] if c.isalnum() or c in (' ', '_', '-')).rstrip()
            audio_file = f"audio_files/{safe_title}.mp3"
            if os.path.exists(audio_file):
                st.audio(audio_file, format="audio/mp3")
            else:
                st.warning("⚠️ الملف الصوتي غير متوفر.")
    else:
        st.info("❌ لم يتم العثور على نتائج مطابقة.")
else:
    st.info("📄 يرجى رفع ملف CSV أولًا للبدء.")
