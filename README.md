# 📚 مكتبة التراث الصوتية

تطبيق ويب مبني باستخدام [Streamlit](https://streamlit.io/) يسمح للمستخدمين **باستعراض الوثائق التراثية بسهولة والاستماع إلى نصوصها مباشرة** باستخدام تحويل النص إلى كلام باللغة العربية.

![heritage](https://img.shields.io/badge/Heritage-Audio_Library-blue) ![streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red) ![license](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 الميزات

✅ تحميل الوثائق التراثية تلقائيًا من ملف CSV موجود على GitHub.  
✅ استعراض البيانات وعرض تفاصيل الوثائق مع الصورة والمعلومات الأساسية.  
✅ تحويل النص إلى صوت تلقائي باستخدام [gTTS](https://pypi.org/project/gTTS/) وحفظ الملفات محليًا.  
✅ إمكانية البحث في العنوان أو المؤلف وتصفيتها لسهولة الوصول إلى الوثائق المطلوبة.  
✅ تشغيل الصوت مباشرة داخل التطبيق للاستماع للنص.

---

## 🛠️ المتطلبات

- Python 3.8 أو أحدث
- مكتبات:
  - `streamlit`
  - `pandas`
  - `gtts`

يمكن تثبيت المتطلبات باستخدام:

```bash
pip install streamlit pandas gtts
