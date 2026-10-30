import csv
import json
import os

# إعدادات الملفات
INPUT_CSV = 'sku.csv'
OUTPUT_JSON = 'plato_items.json'

def generate_plato_json():
    if not os.path.exists(INPUT_CSV):
        print(f"❌ خطأ: لم يتم العثور على الملف '{INPUT_CSV}'. تأكد من وجوده في نفس المجلد.")
        return

    clean_data = []
    skipped_rows = 0

    print(f"⏳ جاري معالجة الملف '{INPUT_CSV}'...")

    try:
        with open(INPUT_CSV, 'r', encoding='utf-8') as file:
            # استخدام csv.reader للتعامل مع الفواصل والاقتباسات بشكل صحيح
            reader = csv.reader(file)
            
            for row_num, row in enumerate(reader, start=1):
                # التأكد من أن الصف يحتوي على عدد كافٍ من الأعمدة لتجنب الأخطاء
                if len(row) >= 12:
                    sku = str(row[0]).strip()
                    name = str(row[2]).strip()
                    description = str(row[3]).strip()
                    price = str(row[5]).strip()
                    img1 = str(row[11]).strip()

                    # تنظيف البيانات والتحقق من صحتها
                    # نتجاهل الصفوف التي لا تحتوي على SKU رقمي أو اسم فارغ (مثل صفوف العناوين أو الفارغة)
                    if sku and name and sku.isdigit():
                        clean_data.append({
                            "sku": sku,
                            "name": name,
                            "description": description,
                            "price": price,
                            "img1": img1 if img1 and img1.lower() != 'nan' else ""
                        })
                    else:
                        skipped_rows += 1
                else:
                    skipped_rows += 1

        # كتابة البيانات إلى ملف JSON بصيغة مضغوطة (Minified) لتقليل حجم الملف وتسريع الموقع
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as json_file:
            json.dump(clean_data, json_file, ensure_ascii=False, separators=(',', ':'))

        # حساب حجم الملف النهائي
        file_size_kb = os.path.getsize(OUTPUT_JSON) / 1024

        print("✅ تم الانتهاء بنجاح!")
        print(f"📊 عدد العناصر التي تم معالجتها: {len(clean_data)} عنصر")
        print(f"⏭️ عدد الصفوف التي تم تجاهلها (غير صالحة): {skipped_rows}")
        print(f"💾 حجم ملف JSON الناتج: {file_size_kb:.2f} كيلوبايت")
        print(f"📁 تم حفظ الملف باسم: '{OUTPUT_JSON}'")

    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع أثناء المعالجة: {e}")

if __name__ == "__main__":
    generate_plato_json()
