import streamlit as st
import os

# ---------- إعداد واجهة التطبيق ----------
st.set_page_config(page_title="📚 مكتبة التراث الصوتية", layout="centered")
st.title("📚 مكتبة التراث الصوتية")
st.write("🎧 استمع إلى نصوص التراث العربي والإسلامي بصوت واضح، وابحث حسب العنوان بسهولة.")

# ---------- تحديد مجلد الملفات ----------
audio_folder = "audio_files"
if not os.path.exists(audio_folder):
    st.error("❌ لم يتم العثور على مجلد الملفات الصوتية.")
else:
    files = [f for f in os.listdir(audio_folder) if f.endswith(".mp3")]
    titles = [os.path.splitext(f)[0] for f in files]
    file_paths = [os.path.join(audio_folder, f) for f in files]
    data = list(zip(titles, file_paths))

    # ---------- مربع البحث ----------
    query = st.text_input("🔍 ابحث بعنوان أو كلمة مفتاحية:")

    if query:
        query = query.strip().lower()
        matches = [(title, path) for title, path in data if query in title.lower()]
        if matches:
            for title, path in matches:
                st.subheader(f"📖 {title}")
                with open(path, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/mp3')
        else:
            st.info("❌ لا توجد نتائج مطابقة، حاول بكلمة أخرى.")
    else:
        st.info("🪐 من فضلك أدخل كلمة مفتاحية في مربع البحث لعرض الملفات الصوتية.")
