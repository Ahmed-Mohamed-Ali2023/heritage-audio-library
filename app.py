import streamlit as st
import pandas as pd
from gtts import gTTS
import os

st.set_page_config(page_title="📚 مكتبة التراث الصوتية", layout="wide")
st.title("📚 مكتبة التراث الصوتية")
st.markdown("### استعرض الوثائق بسهولة واستمع للنص مباشرة.")

uploaded_file = st.file_uploader(
    "📂 قم برفع ملف CSV يحتوي على الأعمدة (Title, Text, Author, Year, Image, Pages, Publisher, Field)",
    type=['csv']
)

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    if not os.path.exists('audio_files'):
        os.makedirs('audio_files')

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

    # تقسيم الأعمدة: content | قائمة البحث
    col_content, col_select = st.columns([3, 1], gap="large")

    with col_select:
        st.markdown("## 🔍 البحث والاختيار")

        # مربع البحث + زر البحث الصغير
        search_col1, search_col2 = st.columns([3, 1])
        search_query = search_col1.text_input("🔎 ابحث في العنوان أو المؤلف:", label_visibility="collapsed", placeholder="ابحث هنا...")
        search_button = search_col2.button("🔍 بحث")

        # عند الضغط على زر البحث
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

        # عرض قائمة الوثائق أسفل البحث مباشرة
        if not filtered_data.empty:
            with st.expander("📄 الوثائق المتاحة بعد البحث (انقر للاطلاع):", expanded=True):
                for idx, row in filtered_data.iterrows():
                    st.markdown(f"- {row['Title']} ({row['Author']} - {row['Year']})")
        else:
            st.warning("❌ لم يتم العثور على أي وثائق مطابقة.")

        # قائمة اختيار الوثيقة
        titles_list = filtered_data['Title'].tolist()
        selected_title = st.selectbox("📑 اختر الوثيقة:", ["-- اختر وثيقة --"] + titles_list)

    with col_content:
        if selected_title != "-- اختر وثيقة --":
            row = filtered_data[filtered_data['Title'] == selected_title].iloc[0]

            st.image(row['Image'], width=300)
            st.markdown(f"## 📖 {row['Title']}")
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
            st.info("📑 اختر وثيقة من القائمة اليمنى للاطلاع على التفاصيل.")

else:
    st.info("📄 يرجى رفع ملف CSV للبدء في استعراض المكتبة.")

