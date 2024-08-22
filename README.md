# svs_to_png
SVS to PNG Converter

This is a simple Python script that converts SVS (Aperio) slide image files to PNG format using the OpenSlide library.

## Requirements

- Python 3.x
- OpenSlide-Python
- Pillow (PIL)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/svs-to-png.git
   cd svs-to-png
   ```

2. Install the required libraries:
   ```bash
   pip install openslide-python Pillow
   ```

## Usage

1. Place your SVS files in the directory you want to process them.
2. Update the file paths in the `svs_to_png.py` script:

   ```python
   file1_path = r"C:\svs\dosya1.svs"
   file2_path = r"C:\svs\dosya2.svs"

   output_path1 = r"C:\svs\output_image1.png"
   output_path2 = r"C:\svs\output_image2.png"
   ```

3. Run the script:
   ```bash
   python svs_to_png.py
   ```

4. The script will generate PNG files from the provided SVS files and save them to the specified output paths. A sound notification will play when the conversion is complete.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
```

### Açıklamalar:
- **Proje Yapısı:** `svs_to_png.py` dosyası Python betiğini içerir, `README.md` dosyası ise projeyi açıklayan bir doküman sunar.
- **`README.md` İçeriği:** `README.md` dosyasında proje hakkında genel bilgi, gereksinimler, kurulum adımları, kullanım talimatları ve lisans bilgileri bulunur.
- **Python Kodları:** Kod, SVS dosyalarını PNG formatına dönüştürür ve bir ses çalınarak işlemin tamamlandığını bildirir.

### Adımlar:
1. Bu dosyaları yerel projenize ekleyin.
2. `README.md` dosyasını ihtiyacınıza göre özelleştirin ve GitHub'da projeyi paylaşın.

Bu sayede, projeyi GitHub'da barındırabilir ve diğer kullanıcıların bu aracı kullanmasını kolaylaştırabilirsiniz. Eğer başka bir konuda yardıma ihtiyacınız olursa, lütfen bana bildirin!
