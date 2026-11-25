import argparse
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  
import sys
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, "readers"))

from readers.Fastq_project import FastqReader

BG_MAIN = "#F0F4F8"       
BG_CARD = "#FFFFFF"       
ACCENT = "#2563EB"        
ACCENT_HOVER = "#1D4ED8" 
TEXT_DARK = "#1E293B"     
TEXT_MUTED = "#64748B"    
BORDER_COLOR = "#CBD5E1"  

FONT_TITLE = ("Ubuntu", 18, "bold")
FONT_BTN = ("Ubuntu", 11, "bold")
FONT_STATS = ("Ubuntu", 11)
def run_fastq_gui():
    root = tk.Tk()
    root.title("Урезанный FastQC")
    root.geometry("850x600")

    def select_file():
        filepath = filedialog.askopenfilename(
            title="Выберите FASTQ файл",
            filetypes=[("FASTQ файлы", "*.fastq *.fq"), ("Все файлы", "*.*")]
        )
        if not filepath:
            return

        try:
            reader = FastqReader(filepath)
            count = reader.count_sequences()
            avg_len = reader.get_average_length()

            # Обновляем текстовую статистику
            stats_label.config(
                text=f"Файл: {os.path.basename(filepath)}  |  "
                     f"Количество ридов: {count}  |  "
                     f"Средняя длина: {avg_len:.1f} bp"
            )

            temp_img_path = "temp_fastq_report.png"
            reader.plot_quality(save_path=temp_img_path)

            img = Image.open(temp_img_path)
            img.thumbnail((800, 480))  # подгоняем размер под окно
            photo = ImageTk.PhotoImage(img)

            image_label.config(image=photo)
            image_label.image = photo  # сохраняем ссылку, чтобы картинка не пропала

        except Exception as e:
            messagebox.showerror("Ошибка обработки", str(e))

    
    btn = tk.Button(root, text="Выбрать FASTQ файл", command=select_file, font=("Arial", 12))
    btn.pack(pady=10)

    stats_label = tk.Label(root, text="Выберите файл для анализа", font=("Arial", 11))
    stats_label.pack(pady=5)

    image_label = tk.Label(root)
    image_label.pack(expand=True)
    
    def on_closing():
        root.destroy()
        os._exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Работа с форматом FASTQ")
    parser.add_argument("--gui", action="store_true", help="Запустить графический интерфейс")
    args = parser.parse_args()

    if args.gui:
        run_fastq_gui()
    else:
        print("Используйте флаг --gui для запуска интерфейса")