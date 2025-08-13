import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pdf2image import convert_from_path
import threading

POPPLER_PATH = r"C:\Users\DEV\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"

def pdf_to_jpg(pdf_input_path, status_callback=None, progress_callback=None):
    pdf_files = []

    if os.path.isfile(pdf_input_path) and pdf_input_path.lower().endswith(".pdf"):
        pdf_files = [pdf_input_path]
    elif os.path.isdir(pdf_input_path):
        for filename in sorted(os.listdir(pdf_input_path)):
            if filename.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(pdf_input_path, filename))
    else:
        message = "PDF 파일 또는 폴더 경로가 올바르지 않습니다."
        if status_callback:
            status_callback(message)
        else:
            print(message)
        return

    if not pdf_files:
        message = "PDF 파일을 찾을 수 없습니다."
        if status_callback:
            status_callback(message)
        else:
            print(message)
        return

    for pdf_path in pdf_files:
        pdf_dir = os.path.dirname(pdf_path)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        jpg_dir = os.path.join(pdf_dir, "jpg", pdf_name)
        os.makedirs(jpg_dir, exist_ok=True)

        message = f"\n[INFO] 변환 시작: {pdf_name}"
        if status_callback:
            status_callback(message)
        else:
            print(message)
        start_time = time.time()

        # 먼저 총 페이지 수 확인
        try:
            from pdf2image.pdf2image import pdfinfo_from_path
            info = pdfinfo_from_path(pdf_path, poppler_path=POPPLER_PATH)
            total_pages = info["Pages"]
        except Exception as e:
            message = f"[ERROR] 페이지 수 확인 실패: {pdf_path} → {e}"
            if status_callback:
                status_callback(message)
            else:
                print(message)
            continue

        num_digits = 4 if total_pages >= 1000 else 3

        for page_number in range(1, total_pages + 1):
            message = f"    [INFO] 페이지 {page_number}/{total_pages} 변환 중..."
            if status_callback:
                status_callback(message)
            else:
                print(message)
                
            if progress_callback:
                progress_callback(page_number, total_pages)
                
            try:
                images = convert_from_path(pdf_path, dpi=300, first_page=page_number, last_page=page_number, poppler_path=POPPLER_PATH)
                img = images[0]
            except Exception as e:
                message = f"    [ERROR] 페이지 {page_number} 변환 실패: {e}"
                if status_callback:
                    status_callback(message)
                else:
                    print(message)
                continue

            img_filename = f"{pdf_name}_{page_number:0{num_digits}d}.jpg"
            img_path = os.path.join(jpg_dir, img_filename)
            img.save(img_path, "JPEG")
            
            message = f"    [✓] 저장됨: {img_path}"
            if status_callback:
                status_callback(message)
            else:
                print(message)

        elapsed = time.time() - start_time
        message = f"[DONE] 완료: {pdf_name} ({total_pages} 페이지 변환됨, {elapsed:.2f}초 소요)"
        if status_callback:
            status_callback(message)
        else:
            print(message)

class PDFtoJPGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to JPG Converter")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.folder_path = tk.StringVar()
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Folder selection section
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(folder_frame, text="폴더 경로:").pack(side=tk.LEFT, padx=(0, 5))
        
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path, width=50)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_button = ttk.Button(folder_frame, text="폴더 선택", command=self.browse_folder)
        browse_button.pack(side=tk.LEFT)
        
        # Conversion button
        convert_button = ttk.Button(main_frame, text="PDF를 JPG로 변환", command=self.start_conversion)
        convert_button.pack(pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        # Status text area
        status_frame = ttk.LabelFrame(main_frame, text="상태 메시지")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.status_text = tk.Text(status_frame, wrap=tk.WORD, height=20)
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
        
        # Set initial status
        self.update_status("PDF를 JPG로 변환할 폴더를 선택하세요.")
        
        # Flag to track if conversion is running
        self.is_converting = False
    
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.update_status(f"선택된 폴더: {folder_selected}")
    
    def update_status(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_progress(self, current, total):
        progress_percent = (current / total) * 100
        self.progress_var.set(progress_percent)
        self.root.update_idletasks()
    
    def start_conversion(self):
        if self.is_converting:
            messagebox.showwarning("진행 중", "변환이 이미 진행 중입니다.")
            return
            
        folder_path = self.folder_path.get().strip()
        if not folder_path:
            messagebox.showerror("오류", "폴더를 선택해주세요.")
            return
            
        if not os.path.exists(folder_path):
            messagebox.showerror("오류", "선택한 폴더가 존재하지 않습니다.")
            return
        
        # Clear previous status messages
        self.status_text.delete(1.0, tk.END)
        self.update_status(f"폴더 '{folder_path}'에서 PDF 변환을 시작합니다...")
        
        # Reset progress bar
        self.progress_var.set(0)
        
        # Start conversion in a separate thread
        self.is_converting = True
        threading.Thread(target=self.run_conversion, args=(folder_path,), daemon=True).start()
    
    def run_conversion(self, folder_path):
        try:
            pdf_to_jpg(folder_path, self.update_status, self.update_progress)
            self.update_status("모든 변환이 완료되었습니다.")
        except Exception as e:
            self.update_status(f"오류 발생: {str(e)}")
        finally:
            self.is_converting = False

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFtoJPGApp(root)
    root.mainloop()
