import streamlit as st
import pandas as pd
from gtts import gTTS
import os

st.set_page_config(page_title="📚 مكتبة التراث الصوتية", layout="wide")

query_params = st.experimental_get_query_params()
doc_id = query_params.get("doc_id", [None])[0]

if doc_id:
    # عند فتح الرابط برقم الوثيقة
    data = pd.read_csv("library_data.csv")  # أو الملف الافتراضي المرفوع في المستودع
    doc_id = int(doc_id)
    row = data.iloc[doc_id]
    st.title(f"📖 {row['Title']}")
    st.image(row['Image'], use_column_width=False, width=300)
    st.markdown(f"**✍️ المؤلف:** {row['Author']}")
    st.markdown(f"**📅 سنة النشر:** {row['Year']}")
    st.markdown(f"**🏢 الناشر:** {row['Publisher']}")
    st.markdown(f"**🏷️ المجال:** {row['Field']}")
    st.markdown(f"**📄 عدد الصفحات:** {row['Pages']}")
    st.markdown("### 📜 النص:")
    st.write(row['Text'][:1500] + "..." if len(row['Text']) > 1500 else row['Text'])

    audio_file = f"audio_files/{''.join(c for c in row['Title'] if c.isalnum() or c in (' ', '_', '-')).rstrip()}.mp3"
    if os.path.exists(audio_file):
        st.audio(audio_file, format="audio/mp3")
    else:
        st.warning("⚠️ الملف الصوتي غير متوفر.")

    st.markdown("[🔙 العودة إلى صفحة البحث](https://your-app.streamlit.app/)")
else:
    st.title("📚 مكتبة التراث الصوتية")
    st.markdown("### 🕋 مكتبة لتحويل محتوى الوثائق إلى صوت والبحث في العنوان والمؤلف والاستماع مباشرة")

    uploaded_file = st.file_uploader("📂 قم برفع ملف CSV يحتوي على الأعمدة (Title, Text, Author, Year, Image, Pages, Publisher, Field)", type=['csv'])

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

        query = st.text_input("🔍 أدخل كلمة للبحث في العنوان أو المؤلف:")

        if query:
            query = query.strip().lower()
            results = []
            for i, row in data.iterrows():
                if query in str(row['Title']).lower() or query in str(row['Author']).lower():
                    results.append((i, row))

            if results:
                st.markdown("### 📝 النتائج:")
                cols = st.columns(3)
                for idx, (i, row) in enumerate(results):
                    col = cols[idx % 3]
                    with col:
                        st.image(row['Image'], use_column_width=False, width=150)
                        st.markdown(f"**{row['Title']}**")
                        st.markdown(f"✍️ {row['Author']} | 📅 {row['Year']}")

                        doc_link = f"https://your-app.streamlit.app/?doc_id={i}"
                        st.markdown(f"[📖 عرض التفاصيل]({doc_link})")
            else:
                st.info("❌ لم يتم العثور على نتائج.")
    else:
        st.info("📄 يرجى رفع ملف CSV أولًا لبدء الاستخدام.")
