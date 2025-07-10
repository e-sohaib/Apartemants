import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd


# --- فرض کنید دیتافریم شما 'df' نام دارد و شامل 'location_lat', 'location_lon' و 'location_cluster' است ---
# اگر 'location_cluster' را ندارید، می توانید آن را حذف کنید یا نقاط را بدون رنگ آمیزی خوشه ببینید.

# 1. ایجاد یک نقشه Folium (می توانید مرکز نقشه را به مرکز تقریبی شهر خود تنظیم کنید)
# برای تهران:
center_lat = 35.66600765543488  # Latitude sanandaj 
center_lon = 51.37501743545668  # Longitude sanadaj

m = folium.Map(location=[center_lat, center_lon], zoom_start=11) # مرکز تقریبی تهران

# 2. اضافه کردن نقاط به نقشه
# اگر تعداد نقاط زیاد است، از MarkerCluster برای عملکرد بهتر استفاده کنید
marker_cluster = MarkerCluster().add_to(m)
def mapit(df):
    # تعیین پالت رنگی برای خوشه ها (اختیاری، اگر location_cluster را دارید)
    if 'location_cluster' in df.columns:
        num_clusters = df['location_cluster'].nunique()
        colors = plt.cm.get_cmap('viridis', num_clusters) # پالت رنگی

        for idx, row in df.iterrows():
            # رنگ بر اساس خوشه (اگر خوشه بندی انجام شده است)
            cluster_color_index = row['location_cluster'] if pd.notna(row['location_cluster']) else 0
            color_rgb = colors(cluster_color_index) # رنگ دهی بر اساس ایندکس خوشه
            hex_color = matplotlib.colors.rgb2hex(color_rgb[:3])

            # اضافه کردن مارکر برای هر نقطه
            if pd.notna(row['location_lat']) and pd.notna(row['location_lon']): # اطمینان از وجود مختصات
                folium.CircleMarker(
                    location=[row['location_lat'], row['location_lon']],
                    radius=3, # اندازه نقطه
                    color=hex_color, # رنگ نقطه بر اساس خوشه
                    fill=True,
                    fill_color=hex_color,
                    fill_opacity=0.7,
                    tooltip=f"Lat: {row['location_lat']:.4f}, Lon: {row['location_lon']:.4f}" # اطلاعات در هاور
                    # می توانید اطلاعات دیگری مثل price_total یا meterage را به tooltip اضافه کنید
                ).add_to(marker_cluster)
    else: # اگر خوشه بندی انجام نشده است، فقط نقاط را اضافه کنید
         for idx, row in df.iterrows():
            if pd.notna(row['location_lat']) and pd.notna(row['location_lon']):
                folium.CircleMarker(
                    location=[row['location_lat'], row['location_lon']],
                    radius=3,
                    color='blue',
                    fill=True,
                    fill_color='blue',
                    fill_opacity=0.7,
                    tooltip=f"Lat: {row['location_lat']:.4f}, Lon: {row['location_lon']:.4f}"
                ).add_to(marker_cluster)

    # 3. ذخیره نقشه به صورت یک فایل HTML (یا نمایش در Jupyter Notebook/Lab)
    map_filename = 'apartment_locations_map.html'
    m.save(map_filename)
    print(f"نقشه در فایل {map_filename} ذخیره شد. آن را در مرورگر خود باز کنید.")

    # در Jupyter Notebook/Lab، می توانید مستقیماً m را در آخرین خط سلول بنویسید تا نمایش داده شود:
    # m