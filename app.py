import streamlit as st
import pandas as pd
from gtts import gTTS
import os

st.title("📚 مكتبة التراث الصوتية")
st.markdown("### استعرض الوثائق واستمع للنص مباشرة.")

# رابط الملف من GitHub بصيغة RAW
csv_url = "https://raw.githubusercontent.com/Ahmed-Mohamed-Ali2023/heritage-audio-library/refs/heads/main/heritage_texts.csv"

# قراءة البيانات
try:
    data = pd.read_csv(csv_url)
    st.success("✅ تم تحميل البيانات بنجاح.")
except Exception as e:
    st.error(f"❌ خطأ أثناء تحميل البيانات: {e}")
    st.stop()

# إنشاء مجلد للملفات الصوتية
if not os.path.exists('audio_files'):
    os.makedirs('audio_files')

# توليد الملفات الصوتية إن لم تكن موجودة
for idx, row in data.iterrows():
    title = row['Title']
    text = str(row['Text'])[:3000]
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
    filename = f"audio_files/{safe_title}.mp3"
    if not os.path.exists(filename):
        tts = gTTS(text, lang='ar')
        tts.save(filename)

# واجهة البحث (يعتمد على الضغط Enter فقط)
search_query = st.text_input("🔎 ابحث في العنوان:", placeholder="اكتب كلمة للبحث...")

# تصفية البيانات بالعنوان فقط
if search_query.strip():
    filtered_data = data[data['Title'].str.contains(search_query, case=False, na=False)]
else:
    filtered_data = data

# قائمة اختيار الوثيقة
titles_list = filtered_data['Title'].tolist()
selected_title = st.selectbox("📑 اختر الوثيقة:", ["-- اختر وثيقة --"] + titles_list)

# عرض الوثيقة
if selected_title != "-- اختر وثيقة --":
    row = filtered_data[filtered_data['Title'] == selected_title].iloc[0]

    st.write(f"### 📖 {row['Title']}")
    st.write(f"**✍️ المؤلف:** {row['Author']}")
    st.write(f"**📅 سنة النشر:** {row['Year']}")
    st.write(f"**🏢 الناشر:** {row['Publisher']}")
    st.write(f"**🏷️ المجال:** {row['Field']}")
    st.write(f"**📄 عدد الصفحات:** {row['Pages']}")
    st.write("### 📜 النص:")
    st.write(row['Text'][:1000] + "..." if len(row['Text']) > 1000 else row['Text'])

    safe_title = "".join(c for c in row['Title'] if c.isalnum() or c in (' ', '_', '-')).rstrip()
    audio_file = f"audio_files/{safe_title}.mp3"
    if os.path.exists(audio_file):
        st.audio(audio_file, format="audio/mp3")
    else:
        st.warning("⚠️ الملف الصوتي غير متوفر.")
else:
    st.info("📑 اختر وثيقة من القائمة للاطلاع على التفاصيل.")
