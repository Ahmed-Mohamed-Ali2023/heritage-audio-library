# تحتاج تثبيت المكتبات:
# !pip install streamlit pandas gtts playsound

import streamlit as st
import pandas as pd
from gtts import gTTS
import os
from io import BytesIO

# تحميل الملف عبر Streamlit
uploaded_file = st.file_uploader("✅ ارفع ملف CSV يحتوي على بيانات الوثائق", type=["csv"])
if uploaded_file:
    data = pd.read_csv(uploaded_file)

    # إنشاء مجلد صوتيات إذا لم يكن موجودًا
    if not os.path.exists("audio_files"):
        os.makedirs("audio_files")

    # توليد ملفات الصوت (مرة واحدة فقط)
    for idx, row in data.iterrows():
        title = row['Title']
        text = str(row['Text'])[:3000]
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
        audio_path = f"audio_files/{safe_title}.mp3"
        if not os.path.exists(audio_path):
            tts = gTTS(text, lang='ar')
            tts.save(audio_path)

    st.title("📚 مكتبة التراث الصوتية")
    st.write("اكتب كلمة البحث ثم اضغط زر البحث، اختر وثيقة لعرض التفاصيل والاستماع.")

    # مربع البحث
    query = st.text_input("🔍 كلمة البحث (عنوان أو مؤلف)")

    if st.button("🔎 بحث"):
        if query.strip() == "":
            st.warning("الرجاء إدخال كلمة للبحث")
        else:
            query_lower = query.strip().lower()
            results = []
            for i, row in data.iterrows():
                if query_lower in str(row['Title']).lower() or query_lower in str(row['Author']).lower():
                    results.append((i, row['Title']))

            if not results:
                st.error("❌ لا توجد نتائج للبحث")
            else:
                # عرض قائمة بالنتائج
                titles = [title for idx, title in results]
                selected_title = st.selectbox("📝 اختر عنوان الوثيقة", titles)

                if selected_title:
                    row = data[data['Title'] == selected_title].iloc[0]
                    st.markdown(f"""
                    <div style="text-align: right; direction: rtl; font-family: 'Cairo', sans-serif; border:1px solid #ccc; padding:15px;">
                        <h3>📜 {row['Title']}</h3>
                        <p><b>المؤلف:</b> {row['Author']}</p>
                        <p><b>عدد الصفحات:</b> {row['Pages']}</p>
                        <p><b>الناشر:</b> {row['Publisher']}</p>
                        <p><b>سنة النشر:</b> {row['Year']}</p>
                        <p><b>المجال:</b> {row['Field']}</p>
                        <img src="{row['Image']}" alt="صورة الوثيقة" style="max-width:300px; margin-top:10px;">
                    </div>
                    """, unsafe_allow_html=True)

                    # تشغيل الصوت
                    safe_title = "".join(c for c in row['Title'] if c.isalnum() or c in (' ', '_', '-')).rstrip()
                    audio_path = f"audio_files/{safe_title}.mp3"
                    audio_file = open(audio_path, "rb").read()
                    st.audio(audio_file, format="audio/mp3")
