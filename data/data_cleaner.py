import pandas as pd
import numpy as np
sandaj_cords ={'center_lat' :35.319276405301174
               ,'center_lon':47.002139457173136}
tehran_cords ={'center_lat' : 35.66600765543488  
             ,'center_lon' : 51.37501743545668}
# --- 3. پاکسازی مختصات (مهم: قبل از محاسبه فاصله) ---

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # شعاع زمین بر حسب کیلومتر (میانگین)
    # R = 3956  # شعاع زمین بر حسب مایل

    # تبدیل درجه به رادیان
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)

    # اختلاف عرض و طول جغرافیایی
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # فرمول Haversine
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c
    return distance
def clean_by_price_per_meter(df: pd.DataFrame, min_price_per_meter: float = 10_000_000) -> pd.DataFrame:
    df_cleaned = df.copy() 
    df_cleaned['price_total'] = pd.to_numeric(df_cleaned['price_total'], errors='coerce')
    df_cleaned['meterage'] = pd.to_numeric(df_cleaned['meterage'], errors='coerce')

    # حذف سطرهایی که price_total یا meterage در آن‌ها NaN است
    # این کار برای جلوگیری از خطای تقسیم بر صفر یا NaN در محاسبه ضروری است
    df_cleaned.dropna(subset=['price_total', 'meterage'], inplace=True)

    # اگر meterage صفر باشد، تقسیم بر صفر اتفاق می‌افتد.
    # بهتر است این سطرها را هم حذف کنیم یا meterage را با یک مقدار کوچک جایگزین کنیم.
    # برای این سناریو، فرض می‌کنیم meterage صفر نامعتبر است و سطر را حذف می‌کنیم.
    df_cleaned = df_cleaned[df_cleaned['meterage'] > 0]

    # 2. محاسبه قیمت هر متر
    # از np.where برای مدیریت مواردی که meterage ممکن است صفر باشد استفاده می‌کنیم
    # اگر meterage صفر باشد، price_per_meter را NaN قرار می‌دهیم تا بعداً حذف شود
    df_cleaned['calculated_price_per_meter'] = np.where(
        df_cleaned['meterage'] > 0,
        df_cleaned['price_total'] / df_cleaned['meterage'],
        np.nan # اگر متراژ صفر باشد، NaN قرار دهید
    )

    # 3. حذف سطرهایی که calculated_price_per_meter کمتر از آستانه است
    # همچنین مطمئن می‌شویم که مقادیر NaN (که از تقسیم بر صفر یا غیرعددی بودن آمده‌اند) را حذف کنیم
    df_cleaned = df_cleaned[df_cleaned['calculated_price_per_meter'] >= min_price_per_meter]
    df_cleaned.dropna(subset=['calculated_price_per_meter'], inplace=True) # برای حذف NaN های احتمالی پس از محاسبه
    # حذف ستون کمکی 'calculated_price_per_meter' اگر نیازی به آن ندارید
    df_cleaned.drop(columns=['calculated_price_per_meter'], inplace=True)

    return df_cleaned


def clean(df : pd.DataFrame):
    print("records count befor: " , len(df))
    city = sandaj_cords
    numeric_cols = ['price_total','build_year' ,'meterage' ,'room_count','floor_number','total_floors','has_elevator']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df.dropna(subset=['total_floors'], inplace=True)
    df['age'] = 1404 - df['build_year']
    df = df[df['location_lat'] > 0].copy()
    df = df[df['location_lon'] > 0].copy()
    df = df[df['meterage'] < 10000].copy()
    df = df[df['meterage'] > 40].copy()
    df = df[df['price_total'] < 100000000000].copy()
    df = df[df['price_total'] > 50000000].copy()
    df = clean_by_price_per_meter(df=df , min_price_per_meter=30_000_000)
    df.loc[:, 'distance_from_center_km'] = haversine_distance(
        city['center_lat'], city['center_lon'],
        df['location_lat'], df['location_lon']
    )
    df = df[df['distance_from_center_km'] < 8].copy()
    print("records count after: " , len(df))
    return df

