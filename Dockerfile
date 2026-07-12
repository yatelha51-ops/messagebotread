# استخدام صورة Playwright الجاهزة
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# تحديد المجلد داخل الحاوية
WORKDIR /app

# نسخ ملفات المشروع إلى الحاوية
COPY . .

# تثبيت مكتبات بايثون المطلوبة
RUN pip install --no-cache-dir -r requirements.txt

# تثبيت المتصفح داخل الحاوية
RUN playwright install chromium

# تشغيل السكربت
CMD ["python", "last_pub_ai_reponse.py"]