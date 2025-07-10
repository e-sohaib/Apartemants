import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import seaborn as sns

def kluster(df : pd.DataFrame):
    X_coords = df[['location_lat', 'location_lon']]
    # محاسبه Inertia (مجموع مربعات فاصله نقاط تا مرکز خوشه‌هایشان) برای Kهای مختلف
    inertia = []
    # محدوده K را بر اساس تعداد نقاط و پراکندگی جغرافیایی تخمین بزنید.
    # معمولاً بین 2 تا 20 یا 30 خوشه برای یک شهر کافی است.
    K_range = range(2, min(30, len(X_coords) // 10)) # حداقل 2 خوشه، حداکثر 30 یا 1/10 تعداد داده‌ها
    if len(K_range) == 0:
        print("تعداد داده‌ها برای اجرای Elbow Method کافی نیست. K را دستی تنظیم کنید.")
        optimal_k = 5 # مقدار پیش‌فرض یا بر اساس دانش قبلی
    else:
        for k in K_range:
            try:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
                kmeans.fit(X_coords)
                inertia.append(kmeans.inertia_)
            except Exception as e:
                print(f"خطا در KMeans برای k={k}: {e}")
                inertia.append(np.nan) # برای نمایش در نمودار

        # رسم نمودار Elbow
        #if not all(pd.isna(inertia)): # اگر حداقل یک مقدار غیر NaN داریم
        #    plt.figure(figsize=(10, 6))
        #    plt.plot(K_range, inertia, marker='o', linestyle='--')
        #    plt.title('Elbow Method for Optimal Number of Clusters (K)')
        #    plt.xlabel('Number of Clusters (K)')
        #    plt.ylabel('Inertia')
        #    plt.grid(True)
        #    plt.xticks(K_range)
        #    plt.show()

        # انتخاب K بر اساس نمودار (جایی که شیب نمودار به طور ناگهانی کاهش می‌یابد)
        # این انتخاب معمولاً بصری است. برای مثال، فرض می‌کنیم 8 خوشه مناسب است.
        optimal_k = 8 # این مقدار را بر اساس نمودار Elbow خود تنظیم کنید!


    # --- مرحله 3: اعمال خوشه‌بندی KMeans با K بهینه ---
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init='auto')
    df['location_cluster'] = kmeans.fit_predict(X_coords) # اعمال خوشه‌بندی بر روی داده‌های پاکسازی شده

    # --- (اختیاری) نمایش خوشه‌ها روی نقشه (برای درک بهتر) ---


    # --- مرحله 4: رمزگذاری One-Hot برای ستون 'location_cluster' ---
    # این کار خوشه‌ها را به ویژگی‌های دودویی (0/1) تبدیل می‌کند که برای مدل قابل فهم هستند.
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    # `location_cluster` باید در یک ساختار 2 بعدی به fit_transform داده شود
    encoded_clusters = encoder.fit_transform(df[['location_cluster']])

    # ایجاد DataFrame از ویژگی‌های رمزگذاری شده
    # ستون‌های جدید نامگذاری می‌شوند: location_cluster_0, location_cluster_1, ...
    cluster_feature_names = [f'location_cluster_{int(c)}' for c in encoder.categories_[0]]
    encoded_clusters_df = pd.DataFrame(encoded_clusters, columns=cluster_feature_names, index=df.index)

    # ادغام ویژگی‌های رمزگذاری شده با دیتافریم اصلی
    df = pd.concat([df, encoded_clusters_df], axis=1)

    # --- مرحله 5: حذف ستون‌های اصلی مختصات و ستون موقت خوشه ---
    # حالا که One-Hot Encoded Cluster ها را داریم، نیازی به ستون‌های اصلی مختصات و Cluster نیست.
    df.drop(columns=['location_cluster',"distance_from_center_km"], inplace=True)
    return df[['meterage', 'room_count' , 'age' , 'floor_number' , 'total_floors' , 'has_elevator' ,'location_lat', 'location_lon','location_cluster_0','location_cluster_1','location_cluster_2','location_cluster_3','location_cluster_4','location_cluster_5','location_cluster_6','location_cluster_7','price_total']]

def plot_klusted(df):
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='location_lon', y='location_lat', hue='location_cluster', data=df, palette='viridis', s=50, alpha=0.8)
    plt.title('Apartment Locations Clustered by K-Means')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend(title='Cluster')
    plt.grid(True)
    plt.show()
