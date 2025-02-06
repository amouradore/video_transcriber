# برنامج تحويل الفيديو إلى نص

هذا المشروع عبارة عن تطبيق Python مع واجهة رسومية (CustomTkinter) باللغة العربية يتيح لك تحويل مقاطع فيديو YouTube إلى نص مكتوب باستخدام خدمة Google Speech Recognition.

## المميزات

- تحويل الفيديو إلى نص: تحويل المحتوى الصوتي من فيديوهات YouTube إلى نص مكتوب
- دعم متعدد اللغات: يدعم العربية، الإنجليزية، الفرنسية، الصينية والإيطالية
- واجهة رسومية حديثة: استخدام CustomTkinter لتجربة مستخدم عصرية وسهلة
- حفظ النص: إمكانية حفظ النص المستخرج في ملف نصي
- معالجة الأخطاء: نظام متكامل لمعالجة الأخطاء وعرض رسائل مناسبة للمستخدم

## المتطلبات الأساسية

- Python 3.8 أو أحدث
- FFmpeg مثبت على النظام
- المكتبات المطلوبة (يتم تثبيتها عبر ملف requirements.txt)

## التثبيت

نسخ المستودع:

git clone https://github.com/amouradore/video_transcriber.git 
cd video_transcriber

تثبيت المتطلبات:

pip install -r requirements.txt

تثبيت FFmpeg:
- Windows: تحميل من [الموقع الرسمي](https://ffmpeg.org/download.html)
- Linux: `sudo apt-get install ffmpeg`
- MacOS: `brew install ffmpeg`

## طريقة الاستخدام

قم بتشغيل البرنامج الرئيسي:

python video_transcriber.py

في النافذة التي تظهر:
1. اختر اللغة المناسبة من القائمة المنسدلة
2. قم بلصق رابط فيديو YouTube
3. انقر على زر "بدء التحويل"
4. انتظر حتى اكتمال عملية التحويل
5. يمكنك حفظ النص باستخدام زر "حفظ النص"

## الأخطاء الشائعة وحلولها

- خطأ HTTP 403: تأكد من صحة رابط الفيديو وأنه متاح للمشاهدة
- فشل التعرف على الكلام: تأكد من جودة الصوت واختيار اللغة الصحيحة
- مشاكل في التحميل: تأكد من اتصال الإنترنت وتثبيت FFmpeg بشكل صحيح

## الترخيص

هذا المشروع مرخص تحت رخصة MIT.

---

# Video to Text Converter

This Python application with a graphical interface (CustomTkinter) allows you to convert YouTube videos to text using Google Speech Recognition service.

## Features

- Video to Text Conversion: Convert audio content from YouTube videos to written text
- Multi-language Support: Supports Arabic, English, French, Chinese, and Italian
- Modern GUI: Using CustomTkinter for a modern and easy user experience
- Text Saving: Ability to save extracted text to a text file
- Error Handling: Integrated system for error handling and appropriate user messages

## Prerequisites

- Python 3.8 or newer
- FFmpeg installed on the system
- Required libraries (installed via requirements.txt)

## Installation

Clone the repository:

git clone https://github.com/amouradore/video_transcriber.git 
cd video_transcriber

Install requirements:

pip install -r requirements.txt

Install FFmpeg:
- Windows: Download from [official website](https://ffmpeg.org/download.html)
- Linux: `sudo apt-get install ffmpeg`
- MacOS: `brew install ffmpeg`

## Usage

Run the main program:

python video_transcriber.py

In the window that appears:
1. Select the appropriate language from the dropdown menu
2. Paste the YouTube video link
3. Click the "Start Conversion" button
4. Wait for the conversion process to complete
5. You can save the text using the "Save Text" button

## Common Issues and Solutions

- HTTP 403 Error: Verify that the video link is valid and the video is accessible
- Speech Recognition Failure: Check audio quality and correct language selection
- Download Issues: Verify internet connection and proper FFmpeg installation

## License

This project is licensed under the MIT License.
