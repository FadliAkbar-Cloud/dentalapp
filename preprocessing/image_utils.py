import cv2
import numpy as np
from PIL import Image
import os
#cv2 library digunakan untuk memproses gambar, sedangkan PIL digunakan untuk membuat thumbnail. os digunakan untuk mengelola file dan direktori.
#cv2 itu sebagai tukang gambar untuk memproses gambar rontgen gigi, seperti mengubah ukuran, memberikan gambar bounding box hijau, meningkatkan kontras, dan menyimpan file yang diupload. Sedangkan PIL digunakan untuk membuat thumbnail dari gambar yang diupload agar bisa ditampilkan dengan ukuran yang lebih kecil di antarmuka pengguna.
def preprocess_dental_xray(image_path, target_size=(640, 640)):
    """
    Preprocessing gambar rontgen gigi untuk deteksi YOLO
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Gambar tidak dapat dibaca: {image_path}")
    
    # Convert ke RGB jika perlu
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    
    # Resize
    img = cv2.resize(img, target_size)
    
    # CLAHE untuk meningkatkan kontras /memperbaiki kualitas gambar 
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_enhanced = clahe.apply(l)
    lab_enhanced = cv2.merge([l_enhanced, a, b])
    img_enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2RGB)
    
    return img_enhanced

def save_uploaded_file(file, upload_folder='static/uploads'):
    """
    Menyimpan file yang diupload
    """
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    filename = f"upload_{os.urandom(8).hex()}.jpg"
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    
    return filepath, filename

def get_thumbnail(image_path, size=(300, 300)):
    """
    Membuat thumbnail untuk tampilan
    """
    img = Image.open(image_path)
    img.thumbnail(size)
    return img