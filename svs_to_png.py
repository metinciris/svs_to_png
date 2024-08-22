import openslide
from PIL import Image
import winsound

# SVS dosya yollarını belirtin
file1_path = r"C:\svs\dosya1.svs"
file2_path = r"C:\svs\dosya2.svs"

# SVS dosyalarını açın
slide1 = openslide.OpenSlide(file1_path)
slide2 = openslide.OpenSlide(file2_path)

# En büyük çözünürlükte resimleri al
image1 = slide1.read_region((0, 0), 0, slide1.level_dimensions[0])
image2 = slide2.read_region((0, 0), 0, slide2.level_dimensions[0])

# Resimleri PNG formatında kaydetme
output_path1 = r"C:\svs\output_image1.png"
output_path2 = r"C:\svs\output_image2.png"
image1.save(output_path1, 'PNG')
image2.save(output_path2, 'PNG')

print(f"Resim 1 PNG olarak kaydedildi: {output_path1}")
print(f"Resim 2 PNG olarak kaydedildi: {output_path2}")

# Windows'ta işlem tamamlandığında bir sistem sesi çalın
winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
