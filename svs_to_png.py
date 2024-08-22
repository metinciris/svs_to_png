import openslide
from PIL import Image
import winsound

def convert_svs_to_png(svs_file_path, output_png_path):
    # SVS dosyasını aç
    slide = openslide.OpenSlide(svs_file_path)

    # En büyük çözünürlükte resmi al
    image = slide.read_region((0, 0), 0, slide.level_dimensions[0])

    # Resmi PNG formatında kaydetme
    image.save(output_png_path, 'PNG')
    print(f"{output_png_path} kaydedildi.")

if __name__ == "__main__":
    # SVS dosya yollarını belirtin
    file1_path = r"C:\svs\dosya1.svs"
    file2_path = r"C:\svs\dosya2.svs"

    # PNG olarak kaydedilecek yollar
    output_path1 = r"C:\svs\output_image1.png"
    output_path2 = r"C:\svs\output_image2.png"

    # Dönüştürme işlemi
    convert_svs_to_png(file1_path, output_path1)
    convert_svs_to_png(file2_path, output_path2)

    # Windows'ta işlem tamamlandığında bir ses çalın
    winsound.Beep(1000, 1000)  # 1000 Hz frekansta, 1 saniye boyunca ses çalar
