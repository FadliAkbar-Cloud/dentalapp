# # from ultralytics import YOLO

# # # Load model
# # model = YOLO('best.pt')  # ganti dengan path ke best.pt Anda

# # # 1. Lihat nama kelas (yang bisa dideteksi)
# # print("=" * 50)
# # print("NAMA KELAS YANG BISA DIDETEKSI:")
# # print(model.names)
# # print("=" * 50)

# # # 2. Lihat jumlah kelas
# # print(f"Jumlah kelas: {len(model.names)}")

# # # 3. Lihat informasi model (jika ada)
# # print("=" * 50)
# # print("INFORMASI MODEL:")
# # print(f"Tipe model: {type(model.model)}")

# # # 4. Coba prediksi dummy untuk lihat output
# # import numpy as np
# # dummy_image = np.zeros((640, 640, 3), dtype=np.uint8)
# # results = model.predict(dummy_image, verbose=False)
# # print(f"Output shape: {len(results[0].boxes) if results[0].boxes else 'Tidak ada deteksi'}")
# # from ultralytics import YOLO

# # model = YOLO('best.pt')

# # # Lihat struktur layer (panjang)
# # print(model.model.model)

# # Hitung jumlah parameter
# from pyexpat import model


# total_params = sum(p.numel() for p in model.model.parameters())
# print(f"Total parameter: {total_params:,}")

# # Lihat ukuran file
# import os
# size = os.path.getsize('best.pt') / (1024 * 1024)
# print(f"Ukuran file: {size:.2f} MB")

from ultralytics import YOLO
import cv2
import os

# Load model
model = YOLO('best.pt')

# Coba dengan gambar (ganti dengan path gambar rontgen Anda)
image_path = '../static/images/fadil.png'  # ganti dengan file gambar Anda

if os.path.exists(image_path):
    results = model.predict(image_path, conf=0.5)
    
    # Tampilkan hasil
    for r in results:
        # Gambar bounding box
        im_array = r.plot()
        cv2.imshow('Hasil Deteksi', im_array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Print deteksi
        if r.boxes:
            for box in r.boxes:
                class_id = int(box.cls[0])
                conf = float(box.conf[0])
                print(f"Deteksi: {model.names[class_id]} dengan confidence {conf:.2f}")
else:
    print(f"File {image_path} tidak ditemukan")