from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import sys

# Tambahkan path untuk import module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocessing.image_utils import save_uploaded_file, preprocess_dental_xray
from model.detector import DentalXRayDetector

app = Flask(__name__)
app.secret_key = 'dental-xray-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Buat folder upload jika belum ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inisialisasi detektor (gunakan model dummy jika best.pt tidak ada)
try:
    detector = DentalXRayDetector('model_data/best.pt')
    print("✅ Model berhasil dimuat")
except Exception as e:
    print(f"⚠️ Model tidak ditemukan: {e}")
    print("Menggunakan mode demo (deteksi dummy)")
    detector = None

# Ekstensi file yang diizinkan
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Halaman utama (Homepage)"""
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    """Halaman untuk memilih jenis analisis rontgen"""
    return render_template('analysis.html')

@app.route('/dental-analysis')
def dental_analysis():
    """Halaman upload untuk analisis rontgen gigi"""
    return render_template('dental_analysis.html')

@app.route('/upload-dental', methods=['POST'])
def upload_dental():
    """Proses upload gambar dan analisis rontgen gigi"""
    if 'xray_image' not in request.files:
        flash('Tidak ada file yang dipilih', 'error')
        return redirect(url_for('dental_analysis'))
    
    file = request.files['xray_image']
    
    if file.filename == '':
        flash('Tidak ada file yang dipilih', 'error')
        return redirect(url_for('dental_analysis'))
    
    if file and allowed_file(file.filename):
        try:
            # Simpan file yang diupload
            filepath, filename = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
            
            # ========== INI BAGIAN YANG DIGANTI ==========
            if detector:
                # 🔥 DETEKSI NYATA DENGAN AI 🔥
                results = detector.predict(filepath)
                summary = detector.get_summary(results['predictions'])
                output_image = results.get('output_image', filepath)
                print(f"✅ Deteksi selesai: {results['total_detections']} temuan")
            else:
                # Mode demo: simulasi hasil deteksi (fallback)
                results = {
                    'predictions': [
                        {'class_name': 'Karies (Gigi Berlubang)', 'confidence': 0.87, 
                         'bbox': {'x1': 120, 'y1': 85, 'x2': 195, 'y2': 160}},
                        {'class_name': 'Tambalan (Filling)', 'confidence': 0.92,
                         'bbox': {'x1': 230, 'y1': 90, 'x2': 290, 'y2': 145}}
                    ],
                    'total_detections': 2,
                    'output_image': filepath
                }
                summary = {
                    'status': 'abnormal',
                    'message': '⚠️ Mode Demo: Ini hanya simulasi. Model AI tidak tersedia.',
                    'summary': {'Karies (Gigi Berlubang)': 1, 'Tambalan (Filling)': 1},
                    'recommendations': [
                        'Pastikan file best.pt ada di folder model_data/',
                        'Jalankan: pip install ultralytics opencv-python'
                    ]
                }
                output_image = filepath
            # ========== SAMPAI SINI YANG DIGANTI ==========
            
            # Render halaman hasil
            return render_template('result.html',
                                 original_image=filepath,
                                 output_image=output_image,
                                 predictions=results['predictions'],
                                 summary=summary,
                                 total_detections=results['total_detections'])
        
        except Exception as e:
            flash(f'Error saat menganalisis gambar: {str(e)}', 'error')
            return redirect(url_for('dental_analysis'))
    
    else:
        flash('Format file tidak didukung. Gunakan: PNG, JPG, JPEG', 'error')
        return redirect(url_for('dental_analysis'))

@app.route('/api/dental-predict', methods=['POST'])
def api_dental_predict():
    """API endpoint untuk prediksi (opsional)"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    
    if file and allowed_file(file.filename):
        filepath, _ = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
        
        if detector:
            results = detector.predict(filepath)
        else:
            results = {
                'predictions': [
                    {'class_name': 'Demo Detection', 'confidence': 0.95}
                ],
                'total_detections': 1
            }
        
        return jsonify(results)
    
    return jsonify({'error': 'Invalid file'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)