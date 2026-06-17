from ultralytics import YOLO
import cv2
import os

class DentalXRayDetector:
    def __init__(self, model_path='model_data/best.pt'):
        # Cek apakah file model ada
        if os.path.exists(model_path):
            self.model = YOLO(model_path)
            print(f"✅ Model AI berhasil dimuat dari {model_path}")
        else:
            print(f"❌ File model tidak ditemukan di {model_path}")
            self.model = None
        
        self.class_names = {
            0: 'Karies (Gigi Berlubang)',
            1: 'Deep Caries (Karies Dalam)',
            2: 'Gigi Impaksi',
            3: 'Periapical Lesion',
        }
    
    def predict(self, image_path, conf_threshold=0.5):
        """Deteksi kondisi gigi dari gambar asli"""
        if self.model is None:
            return {'predictions': [], 'total_detections': 0, 'output_image': image_path}
        
        # Baca gambar
        img = cv2.imread(image_path)
        result_img = img.copy()
        
        # Prediksi dengan YOLO
        results = self.model.predict(
            image_path,
            conf=conf_threshold,
            save=False,
            verbose=False
        )
        
        predictions = []
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()
                    x1, y1, x2, y2 = map(int, bbox)
                    
                    predictions.append({
                        'class_name': self.class_names.get(class_id, 'Unknown'),
                        'confidence': confidence,
                        'bbox': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
                    })
                    
                    # Gambar bounding box
                    cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f"{self.class_names.get(class_id, 'Unknown')}: {confidence:.2f}"
                    cv2.putText(result_img, label, (x1, y1-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Simpan gambar hasil
        output_path = image_path.replace('.', '_result.')
        cv2.imwrite(output_path, result_img)
        
        return {
            'predictions': predictions,
            'total_detections': len(predictions),
            'output_image': output_path
        }
    
    def get_summary(self, predictions):
        if not predictions:
            return {
                'status': 'normal',
                'message': '✅ Tidak ditemukan kondisi abnormal. Gigi terlihat sehat!',
                'recommendations': [
                    'Tetap jaga kesehatan gigi dengan rutin menyikat gigi 2x sehari.',
                    'Kontrol ke dokter gigi setiap 6 bulan sekali.'
                ]
            }
        
        # Kelompokkan berdasarkan jenis
        summary = {}
        for pred in predictions:
            name = pred['class_name']
            summary[name] = summary.get(name, 0) + 1
        
        # Buat rekomendasi
        # append untuk menambahkan rekomendasi berdasarkan jenis temuan yang ditemukan. Misalnya, jika ditemukan karies, maka rekomendasinya adalah untuk segera konsultasi ke dokter gigi untuk perawatan karies. Jika ditemukan deep caries, maka rekomendasinya adalah untuk segera konsultasi ke dokter gigi spesialis konservasi gigi. Jika ditemukan gigi impaksi, maka rekomendasinya adalah untuk konsultasi dengan dokter gigi spesialis bedah mulut untuk evaluasi pencabutan. Jika ditemukan periapical lesion, maka rekomendasinya adalah untuk segera konsultasi ke dokter gigi, mungkin perlu perawatan saluran akar.
        #append adalah metode untuk menambahkan elemen ke dalam list rekomendasi berdasarkan kondisi yang ditemukan dalam summary. Jadi, jika summary menunjukkan adanya karies, maka rekomendasi untuk konsultasi ke dokter gigi akan ditambahkan ke dalam list rekomendasi. Begitu juga untuk kondisi lainnya seperti deep caries, gigi impaksi, dan periapical lesion.
        recommendations = []
        if 'Karies (Gigi Berlubang)' in summary:
            recommendations.append("Segera konsultasikan dengan dokter gigi untuk perawatan karies.")
        if 'Deep Caries (Karies Dalam)' in summary:
            recommendations.append("Segera konsultasi ke dokter gigi spesialis konservasi gigi.")
        if 'Gigi Impaksi' in summary:
            recommendations.append("Konsultasi dengan dokter gigi spesialis bedah mulut untuk evaluasi pencabutan.")
        if 'Periapical Lesion' in summary:
            recommendations.append("Segera konsultasi ke dokter gigi, mungkin perlu perawatan saluran akar.")
        
        return {
            'status': 'abnormal',
            'summary': summary,
            'message': f"⚠️ Ditemukan {len(predictions)} area yang memerlukan perhatian.",
            'recommendations': recommendations
        }