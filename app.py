import streamlit as st
import os

# ---------- عنوان التطبيق ----------
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
    else:
        matches = data  # عرض جميع الملفات في حال عدم كتابة كلمة مفتاحية

    # ---------- عرض النتائج ----------
    if matches:
        for title, path in matches:
            st.subheader(f"📖 {title}")
            audio_file = open(path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
            audio_file.close()
    else:
        st.info("❌ لا توجد نتائج مطابقة، حاول بكلمة أخرى.")
