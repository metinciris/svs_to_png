import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps, ImageFile, ImageDraw
import winsound

# Pillow'un decompression bomb limitini yükseltin
Image.MAX_IMAGE_PIXELS = None

class ImageAligner:
    def __init__(self, master, image1_path, image2_path):
        self.master = master
        self.master.title("Görsel Hizalayıcı")

        # Arayüz yüklenmeden önce ses çıkmaması için ses çalmayı sona erteleyin
        self.master.after(500, lambda: winsound.PlaySound("SystemStart", winsound.SND_ALIAS))

        # Resimleri yükle ve boyutlarını küçült
        resize_dimension = 800  # Resimleri 800x800 boyutuna küçült
        self.image1 = Image.open(image1_path).resize((resize_dimension, resize_dimension), Image.Resampling.LANCZOS)
        self.image2 = Image.open(image2_path).resize((resize_dimension, resize_dimension), Image.Resampling.LANCZOS)

        # Resimleri çember içine yerleştir ve merkez nokta ekle
        self.image1 = self.crop_to_circle(self.image1)
        self.image2 = self.crop_to_circle(self.image2)

        # Üstteki resmin şeffaflığı ve koyuluğunu ayarla
        self.image2 = ImageOps.colorize(self.image2.convert("L"), black="black", white="white")
        self.image2 = self.image2.convert("RGBA")
        self.image2.putalpha(150)

        # İnce ayar modu ve ayarlar
        self.fine_tune_mode = False
        self.zoom_scale = 1.0  # Zoom sabit kalacak

        # Sol kısımda kontrol butonları için bir çerçeve oluşturun
        controls_frame = tk.Frame(self.master)
        controls_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Canvas ve Görüntüleri yerleştir
        self.canvas = tk.Canvas(self.master, width=resize_dimension, height=resize_dimension)
        self.canvas.pack(side=tk.RIGHT)

        self.image1_tk = ImageTk.PhotoImage(self.image1)
        self.image2_tk = ImageTk.PhotoImage(self.image2)

        self.image1_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image1_tk)
        self.image2_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image2_tk)

        # Başlangıç döndürme, pozisyon, şeffaflık ve koyuluk
        self.angle = 0
        self.offset_x = 0
        self.offset_y = 0
        self.transparency = 150
        self.rotation_center = (resize_dimension // 2, resize_dimension // 2)

        # Fare kontrolleri için başlangıç pozisyonları
        self.start_x = 0
        self.start_y = 0

        # Fare olaylarını bağla
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.move_image)
        self.canvas.bind("<MouseWheel>", self.zoom_image)

        # Ayar butonları
        self.create_controls(controls_frame)

    def crop_to_circle(self, image):
        """Resmi bir çember içine kırpar ve merkez nokta ekler."""
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + image.size, fill=255)
        result = Image.new("RGBA", image.size)
        result.paste(image, mask=mask)
        
        # Merkezde bir nokta ekleyin
        draw = ImageDraw.Draw(result)
        center = (image.size[0] // 2, image.size[1] // 2)
        draw.ellipse((center[0]-5, center[1]-5, center[0]+5, center[1]+5), fill="red")
        
        return result

    def create_controls(self, parent_frame):
        # Döndürme kontrolü
        rotate_label = tk.Label(parent_frame, text="Döndür:")
        rotate_label.grid(row=0, column=0, sticky='w')
        self.rotate_slider = tk.Scale(parent_frame, from_=-180, to=180, orient=tk.HORIZONTAL, command=self.update_rotation)
        self.rotate_slider.grid(row=0, column=1)

        # + ve - düğmeleri
        plus_button = tk.Button(parent_frame, text="+", command=lambda: self.adjust_rotation(0.1))
        plus_button.grid(row=1, column=1, sticky='w')
        minus_button = tk.Button(parent_frame, text="-", command=lambda: self.adjust_rotation(-0.1))
        minus_button.grid(row=1, column=0, sticky='e')

        # Şeffaflık kontrolü
        transparency_label = tk.Label(parent_frame, text="Şeffaflık:")
        transparency_label.grid(row=2, column=0, sticky='w')
        self.transparency_slider = tk.Scale(parent_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_transparency)
        self.transparency_slider.grid(row=2, column=1)

        # Ince Ayar butonu
        self.fine_tune_button = tk.Button(parent_frame, text="Ince Ayar", command=self.toggle_fine_tune)
        self.fine_tune_button.grid(row=3, column=0, columnspan=2)

        # Merkez Hizalama butonu
        self.align_center_button = tk.Button(parent_frame, text="Merkez hizalandı ise tıkla", command=self.set_new_rotation_center)
        self.align_center_button.grid(row=4, column=0, columnspan=2)

        # Kaydetme butonu
        save_button = tk.Button(parent_frame, text="Kaydet", command=self.save_settings)
        save_button.grid(row=5, column=0, columnspan=2)

        # Çıkış butonu
        exit_button = tk.Button(parent_frame, text="Çıkış", command=self.master.quit)
        exit_button.grid(row=6, column=0, columnspan=2)

        # Kontrol butonlarının görevlerini gösteren bir etiket ekleyin
        instructions_label = tk.Label(parent_frame, text="Kontroller:\n- Döndürme: Kaydırıcı / + / - \n- Şeffaflık: Kaydırıcı\n- Ince Ayar: Buton\n- Zoom: Fare Tekerleği\n- Taşıma: Fare Sürükle\n- Merkez hizalama: Buton\n- Çıkış: Çıkış Butonu")
        instructions_label.grid(row=7, column=0, columnspan=2, sticky='w')

    def start_move(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def move_image(self, event):
        move_step = 0.05 if self.fine_tune_mode else 0.5
        self.offset_x += (event.x - self.start_x) * move_step
        self.offset_y += (event.y - self.start_y) * move_step
        self.start_x = event.x
        self.start_y = event.y
        self.update_image()

    def update_rotation(self, value):
        rotation_step = 0.05 if self.fine_tune_mode else 0.5
        self.angle = float(value) * rotation_step
        self.update_image()

    def adjust_rotation(self, step):
        self.angle += step
        self.update_image()

    def update_transparency(self, value):
        self.transparency = int(value)
        self.update_image()

    def zoom_image(self, event):
        zoom_step = 0.005 if self.fine_tune_mode else 0.05
        if event.delta > 0:
            self.zoom_scale *= (1 + zoom_step)  # Büyütme
        else:
            self.zoom_scale *= (1 - zoom_step)  # Küçültme
        self.update_image()

    def update_image(self):
        rotated_image = self.image2.rotate(self.angle, resample=Image.BICUBIC, center=self.rotation_center)
        scaled_image = rotated_image.resize((int(self.image2.width * self.zoom_scale), int(self.image2.height * self.zoom_scale)), Image.Resampling.LANCZOS)
        scaled_image.putalpha(self.transparency)
        self.image2_tk = ImageTk.PhotoImage(scaled_image)
        self.canvas.coords(self.image2_id, self.offset_x, self.offset_y)
        self.canvas.itemconfig(self.image2_id, image=self.image2_tk)

    def set_new_rotation_center(self):
        self.rotation_center = (self.start_x, self.start_y)
        self.align_center_button.config(text="Yeni merkez hizalandı")
        print(f"Yeni döndürme merkezi: {self.rotation_center}")

    def toggle_fine_tune(self):
        self.fine_tune_mode = not self.fine_tune_mode
        self.fine_tune_button.config(bg="green" if self.fine_tune_mode else "SystemButtonFace")
        mode = "aktif" if self.fine_tune_mode else "deaktif"
        print(f"Ince Ayar modu {mode} hale getirildi.")

    def save_settings(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="manual_align", filetypes=[("Text files", "*.txt")])
        if save_path:
            with open(save_path, "w") as file:
                file.write(f"Angle: {self.angle}\n")
                file.write(f"Offset X: {self.offset_x}\n")
                file.write(f"Offset Y: {self.offset_y}\n")
                file.write(f"Transparency: {self.transparency}\n")
                file.write(f"Zoom Scale: {self.zoom_scale}\n")
                file.write(f"Rotation Center: {self.rotation_center}\n")
            print(f"Ayarlar kaydedildi: {save_path}")
            # Kaydedildikten sonra bir ses çalın
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

if __name__ == "__main__":
    root = tk.Tk()

    # Küçük boyutlu örnek resimler
    image1_path = r"C:\svs\output_image1_min.png"
    image2_path = r"C:\svs\output_image2_min.png"

    app = ImageAligner(root, image1_path, image2_path)
    root.mainloop()
