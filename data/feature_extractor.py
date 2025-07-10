import json
import re

def parse_price(text):
    # تبدیل فارسی به انگلیسی و حذف کاما
    return int(re.sub(r"[^\d]", "", text.replace("٬", "")))

def extract_features(divar_json: dict) -> dict:
    features = {}
    features["title"] = divar_json.get("share", {}).get("title")
    features["city"] = divar_json.get("seo", {}).get("web_info", {}).get("city_persian")
    features["location_lat"] = float(divar_json.get("seo", {}).get("post_seo_schema", {}).get("geo", {}).get("latitude", 0))
    features["location_lon"] = float(divar_json.get("seo", {}).get("post_seo_schema", {}).get("geo", {}).get("longitude", 0))
    
    features["price_total"] = divar_json.get("webengage", {}).get("price", 0)

    # استخراج از LIST_DATA
    for section in divar_json.get("sections", []):
        if section.get("section_name") == "LIST_DATA":
            for widget in section.get("widgets", []):
                data = widget.get("data", {})
                wtype = widget.get("widget_type")
                
                if wtype == "GROUP_INFO_ROW":
                    for item in data.get("items", []):
                        title = item.get("title")
                        val = item.get("value")
                        if title == "متراژ":
                            features["meterage"] = int(val)
                        elif title == "ساخت":
                            features["build_year"] = int(val)
                        elif title == "اتاق":
                            features["room_count"] = int(val)
                
                elif wtype == "UNEXPANDABLE_ROW":
                    title = data.get("title")
                    value = data.get("value")
                    if title == "قیمت هر متر":
                        features["price_per_meter"] = parse_price(value)
                    elif title == "طبقه":
                        match = re.search(r"(\d+)?\s*از\s*(\d+)", value)
                        if match:
                            features["floor_number"] = int(match.group(1)) if match.group(1) else 0
                            features["total_floors"] = int(match.group(2))
                        elif "همکف" in value:
                            features["floor_number"] = 0

    # محاسبه سن بنا
    current_year = 1404  # فرض فعلاً
    features["age_of_building"] = current_year - features.get("build_year", current_year)

    # امکانات (features)
    bool_features = {
        "has_elevator": False,
        "has_parking": False,
        "has_anbari": False,
        "balcony": False,
    }

    string_features = {
        "floor_material": None,
        "wc_type": None,
        "cooling": None,
        "heating": None,
        "water_heater": None,
        "document_type": None,
        "direction": None,
        "renovated": None,
    }

    # گشتن در امکانات
    for section in divar_json.get("sections", []):
        if section.get("section_name") == "LIST_DATA":
            for widget in section.get("widgets", []):
                wtype = widget.get("widget_type")
                data = widget.get("data", {})

                if wtype == "GROUP_FEATURE_ROW" or wtype == "FEATURE_ROW":
                    items = data.get("items", [])
                    for item in items:
                        title = item.get("title", "").strip()

                        if "آسانسور ندارد" in title:
                            bool_features["has_elevator"] = False
                        elif "آسانسور" in title:
                            bool_features["has_elevator"] = True

                        if "پارکینگ ندارد" in title:
                            bool_features["has_parking"] = False
                        elif "پارکینگ" in title:
                            bool_features["has_parking"] = True

                        if "انباری" in title:
                            bool_features["has_anbari"] = True

                        if "بالکن" in title:
                            bool_features["balcony"] = True

                        if "جنس کف" in title:
                            string_features["floor_material"] = title.replace("جنس کف", "").strip()

                        if "سرویس بهداشتی" in title:
                            string_features["wc_type"] = title.replace("سرویس بهداشتی", "").strip()

                        if "سرمایش" in title:
                            string_features["cooling"] = title.replace("سرمایش", "").strip()

                        if "گرمایش" in title:
                            string_features["heating"] = title.replace("گرمایش", "").strip()

                        if "تأمین‌کننده آب گرم" in title or "پکیج" in title:
                            string_features["water_heater"] = "پکیج"

                        if "سند" in title:
                            string_features["document_type"] = data.get("value")

                        if "جهت ساختمان" in title:
                            string_features["direction"] = data.get("value")

                        if "وضعیت واحد" in title:
                            v = data.get("value", "")
                            string_features["renovated"] = False if "بازسازی نشده" in v else True

    # جمع‌کردن تمام فیچرها
    features.update(bool_features)
    features.update(string_features)

    # نمره امکانات
    features["features_score"] = int(bool_features["has_elevator"]) + int(bool_features["has_parking"]) + \
                                 int(bool_features["has_anbari"]) + int(bool_features["balcony"])

    return features
