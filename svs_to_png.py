import openslide
from PIL import Image
import winsound

def convert_svs_to_png(svs_path, output_path, min_output_path, resize_width=3840):
    slide = openslide.OpenSlide(svs_path)
    
    # Orijinal boyutta PNG olarak kaydet
    dimensions = slide.dimensions
    original_image = slide.read_region((0, 0), 0, dimensions)
    original_image = original_image.convert("RGB")
    original_image.save(output_path)
    print(f"Orijinal PNG olarak kaydedildi: {output_path}")

    # Küçük boyutlu PNG (4K) olarak kaydet
    aspect_ratio = dimensions[1] / dimensions[0]
    new_height = int(resize_width * aspect_ratio)
    min_image = original_image.resize((resize_width, new_height), Image.Resampling.LANCZOS)
    min_image.save(min_output_path)
    print(f"Küçük boyutlu PNG olarak kaydedildi: {min_output_path}")

if __name__ == "__main__":
    # SVS dosya yollarını belirtin
    file1_path = r"C:\svs\dosya1.svs"
    file2_path = r"C:\svs\dosya2.svs"

    # Çıktı dosya yollarını belirtin
    output_path1 = r"C:\svs\output_image1.png"
    min_output_path1 = r"C:\svs\output_image1_min.png"
    output_path2 = r"C:\svs\output_image2.png"
    min_output_path2 = r"C:\svs\output_image2_min.png"

    # SVS dosyalarını PNG'ye dönüştürme
    convert_svs_to_png(file1_path, output_path1, min_output_path1)
    convert_svs_to_png(file2_path, output_path2, min_output_path2)

    # Windows'ta işlem tamamlandığında bir sistem sesi çalın
    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
