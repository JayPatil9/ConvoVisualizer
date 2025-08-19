import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk, ImageDraw

class ConvVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("2D Convolution Visualizer")
        self.root.geometry("900x650")
        
        self.original_image = None
        self.processed_image = None
        self.steps = []
        self.current_step = 0
        self.animating = False
        
        self.presets = {
            "Sharpen": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
            "Edge Detect": np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]),
            "Blur": np.ones((3, 3))/9,
            "Identity": np.array([[0,0,0],[0,1,0],[0,0,0]]),
            "Emboss": np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]]),
            "Sobel X": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
            "Laplacian": np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        }
        self.current_kernel = np.copy(self.presets["Sharpen"])
        
        self.setup_gui()

    def setup_gui(self):
        self.root.configure(bg='#f0f0f0')

        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        control_frame = ttk.LabelFrame(main_frame, text="🎛️ Controls", padding=15)
        control_frame.grid(row=0, column=0, rowspan=2, sticky="ns", padx=(0, 15))
        
        file_frame = ttk.LabelFrame(control_frame, text="File Operations", padding=10)
        file_frame.pack(fill=tk.X, pady=(0,10))
        ttk.Button(file_frame, text="📁 Load Image", command=self.load_image).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="💾 Save Result", command=self.save_result).pack(fill=tk.X, pady=2)

        filter_frame = ttk.LabelFrame(control_frame, text="Filter Selection", padding=10)
        filter_frame.pack(fill=tk.X, pady=(0,10))
        
        ttk.Label(filter_frame, text="Preset Filters:").pack()
        self.preset_var = tk.StringVar(value="Sharpen")
        preset_combo = ttk.Combobox(filter_frame, values=list(self.presets.keys()), 
                                    textvariable=self.preset_var, state="readonly")
        preset_combo.pack(pady=(5,10), fill=tk.X)
        preset_combo.bind("<<ComboboxSelected>>", self.apply_preset)
        
        ttk.Label(filter_frame, text="Custom Kernel (3×3):").pack()
        self.kernel_entries = []
        kernel_frame = ttk.Frame(filter_frame)
        kernel_frame.pack(pady=5)
        
        for i in range(3):
            row = []
            for j in range(3):
                e = ttk.Entry(kernel_frame, width=7, justify="center")
                e.grid(row=i, column=j, padx=1, pady=1)
                e.insert(0, str(self.current_kernel[i][j]))
                row.append(e)
            self.kernel_entries.append(row)
        
        process_frame = ttk.LabelFrame(control_frame, text="Processing", padding=10)
        process_frame.pack(fill=tk.X, pady=(0,10))
        
        self.apply_button = ttk.Button(process_frame, text="⚡ Apply Convolution & Animate", 
                                      command=self.apply_convolution)
        self.apply_button.pack(fill=tk.X, pady=2)

        ttk.Button(process_frame, text="🔍 Compare Images", command=self.compare_images).pack(fill=tk.X, pady=2)

        speed_frame = ttk.LabelFrame(control_frame, text="Animation Speed", padding=10)
        speed_frame.pack(fill=tk.X, pady=(0,10))
        ttk.Label(speed_frame, text="Speed (ms per frame):").pack()
        self.speed_var = tk.IntVar(value=10)
        speed_scale = ttk.Scale(speed_frame, from_=1, to=50, variable=self.speed_var, orient=tk.HORIZONTAL)
        speed_scale.pack(fill=tk.X, pady=2)

        self.status_var = tk.StringVar(value="🟢 Ready - Load image")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, 
                               foreground="blue", font=('Arial', 9), wraplength=200)
        status_label.pack(pady=(10,0))

        display_frame = ttk.LabelFrame(main_frame, text="🖼️ Image Display", padding=15)
        display_frame.grid(row=0, column=1, sticky="nsew")
        display_frame.columnconfigure((0,1), weight=1)
        display_frame.rowconfigure(0, weight=1)

        orig_frame = ttk.Frame(display_frame)
        orig_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        orig_frame.columnconfigure(0, weight=1)
        orig_frame.rowconfigure(0, weight=1)
        
        self.orig_canvas = tk.Canvas(orig_frame, bg='white', relief='sunken', bd=2, 
                                   width=400, height=400)
        self.orig_canvas.grid(row=0, column=0, sticky="nsew")
        ttk.Label(orig_frame, text="📸 Original Image", 
                 font=('Arial', 10, 'bold')).grid(row=1, column=0, pady=(5,0))

        
        proc_frame = ttk.Frame(display_frame)
        proc_frame.grid(row=0, column=1, sticky="nsew")
        proc_frame.columnconfigure(0, weight=1)
        proc_frame.rowconfigure(0, weight=1)
        
        self.proc_canvas = tk.Canvas(proc_frame, bg='white', relief='sunken', bd=2, 
                                   width=400, height=400)
        self.proc_canvas.grid(row=0, column=0, sticky="nsew")
        ttk.Label(proc_frame, text="🎬 Filtered Result", 
                 font=('Arial', 10, 'bold')).grid(row=1, column=0, pady=(5,0))

    def apply_preset(self, *args):
        kernel = self.presets[self.preset_var.get()]
        for i in range(3):
            for j in range(3):
                self.kernel_entries[i][j].delete(0, tk.END)
                self.kernel_entries[i][j].insert(0, str(kernel[i][j]))
        self.status_var.set(f"🎯 Filter set to {self.preset_var.get()}")

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif")]
        )
        
        if file_path:
            try:
                pil_image = Image.open(file_path)
                pil_image = pil_image.convert('L')
                
                max_size = 400
                pil_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                self.original_image = np.array(pil_image)
                self.show_img(self.orig_canvas, pil_image)
                self.proc_canvas.delete("all")
                self.processed_image = None
                self.steps = []
                self.current_step = 0
                
                self.status_var.set(f"✅ Image loaded ({self.original_image.shape[0]}×{self.original_image.shape[1]})")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                self.status_var.set("❌ Failed to load image")

    def get_kernel_from_entries(self):
        try:
            k = np.zeros((3, 3))
            for i in range(3):
                for j in range(3):
                    value = self.kernel_entries[i][j].get().strip()
                    if value:
                        k[i][j] = float(value)
            return k
        except ValueError:
            messagebox.showerror("Error", "Invalid kernel values. Please enter numbers only.")
            return None

    def apply_convolution(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first.")
            return
        kernel = self.get_kernel_from_entries()
        if kernel is None: 
            return

        self.status_var.set("⚙️ Processing image convolution...")
        self.root.update()

        try:
            kh, kw = kernel.shape
            pad_h, pad_w = kh//2, kw//2
            padded = np.pad(self.original_image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')

            out_img = np.zeros_like(self.original_image, dtype=np.float32)
            out_img.fill(255)
            self.steps = []
            self.pixel_positions = []

            total_pixels = self.original_image.shape[0] * self.original_image.shape[1]
            
            if total_pixels > 40000: 
                max_frames = 80
            elif total_pixels > 10000:
                max_frames = 120
            else:
                max_frames = 150
                
            skip_factor = max(1, total_pixels // max_frames)

            pixel_count = 0
            for i in range(self.original_image.shape[0]):
                for j in range(self.original_image.shape[1]):
                    roi = padded[i:i+kh, j:j+kw]
                    result = np.sum(roi * kernel)
                    out_img[i, j] = result
                    
                    if pixel_count % skip_factor == 0:
                        partial_result = np.clip(out_img.copy(), 0, 255).astype(np.uint8)
                        self.steps.append(partial_result)
                        self.pixel_positions.append((i, j))
                    
                    pixel_count += 1

            self.processed_image = np.clip(out_img, 0, 255).astype(np.uint8)
            if len(self.steps) == 0 or not np.array_equal(self.steps[-1], self.processed_image):
                self.steps.append(self.processed_image.copy())
                self.pixel_positions.append((-1, -1))

            self.current_step = 0
            self.apply_button.config(state="disabled", text="🎬 Animating Image...")
            self.animate_step()

        except Exception as e:
            messagebox.showerror("Error", f"Convolution failed: {str(e)}")
            self.status_var.set("❌ Convolution failed")

    def animate_step(self):
        if not self.animating:
            self.animating = True

        if self.current_step < len(self.steps):
            frame = self.steps[self.current_step]
            self.show_img(self.proc_canvas, Image.fromarray(frame))
            
            i, j = self.pixel_positions[self.current_step]
            if i >= 0 and j >= 0:
                self.highlight_pixel(i, j)
            else:
                self.show_img(self.orig_canvas, Image.fromarray(self.original_image))
            
            progress = int((self.current_step + 1) / len(self.steps) * 100)
            self.status_var.set(f"🎬 Animating image... {progress}% ({self.current_step+1}/{len(self.steps)} frames)")
            
            self.current_step += 1
            self.root.after(self.speed_var.get(), self.animate_step)
        else:
            self.animating = False
            self.apply_button.config(state="normal", text="⚡ Apply Convolution & Animate")
            self.status_var.set(f"🎬 Animation completed! ({len(self.steps)} frames)")

    def highlight_pixel(self, i, j):
        try:
            pil_img = Image.fromarray(self.original_image).convert("RGB")
            draw = ImageDraw.Draw(pil_img)
            
            img_height, img_width = self.original_image.shape
            
            scale_x = pil_img.width / img_width
            scale_y = pil_img.height / img_height
            
            highlight_size = max(2, int(min(scale_x, scale_y)))
            
            x1 = int(j * scale_x)
            y1 = int(i * scale_y)
            x2 = int((j + 1) * scale_x)
            y2 = int((i + 1) * scale_y)
            
            draw.rectangle([x1-1, y1-1, x2+1, y2+1], outline='red', width=max(2, highlight_size))
            
            self.show_img(self.orig_canvas, pil_img)
            
        except Exception as e:
            self.show_img(self.orig_canvas, Image.fromarray(self.original_image))

    def compare_images(self):
        if self.original_image is None or self.processed_image is None:
            messagebox.showwarning("Warning", "Please load and process an image first.")
            return
            
        try:
            proc_pil = Image.fromarray(self.processed_image)
            orig_pil = Image.fromarray(self.original_image)
            w, h = orig_pil.size
            
            compare_img = Image.new('L', (2*w + 20, h), color=255)
            compare_img.paste(orig_pil, (0, 0))
            compare_img.paste(proc_pil, (w + 20, 0))
            
            compare_window = tk.Toplevel(self.root)
            compare_window.title("🔍 Image Comparison")
            compare_window.geometry(f"{min(1200, 2*w + 60)}x{min(800, h + 100)}")
            
            ttk.Label(compare_window, text="Original vs Filtered", 
                     font=('Arial', 12, 'bold')).pack(pady=10)
            
            canvas_frame = tk.Frame(compare_window)
            canvas_frame.pack(fill=tk.BOTH, expand=True)
            
            compare_canvas = tk.Canvas(canvas_frame, bg='gray90')
            scrollbar_v = ttk.Scrollbar(canvas_frame, orient="vertical", command=compare_canvas.yview)
            scrollbar_h = ttk.Scrollbar(canvas_frame, orient="horizontal", command=compare_canvas.xview)
            
            compare_canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
            
            scrollbar_v.pack(side="right", fill="y")
            scrollbar_h.pack(side="bottom", fill="x")
            compare_canvas.pack(side="left", fill="both", expand=True)
            
            photo = ImageTk.PhotoImage(compare_img)
            compare_canvas.create_image(10, 10, anchor=tk.NW, image=photo)
            compare_canvas.image = photo
            
            compare_canvas.configure(scrollregion=compare_canvas.bbox("all"))
            
            compare_canvas.create_text(w//2 + 10, h+25, text="Original", font=('Arial', 12, 'bold'))
            compare_canvas.create_text(w + 30 + w//2, h+25, text="Filtered", font=('Arial', 12, 'bold'))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create comparison: {str(e)}")

    def save_result(self):
        if self.processed_image is None:
            messagebox.showinfo("Info", "No processed image to save.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension='.png',
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("BMP files", "*.bmp")],
            title="Save Processed Image")
            
        if file_path:
            try:
                Image.fromarray(self.processed_image).save(file_path)
                self.status_var.set(f"💾 Processed image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

    def show_img(self, canvas, pil_img):
        try:
            canvas_width = canvas.winfo_width() or 400
            canvas_height = canvas.winfo_height() or 400
            
            img_copy = pil_img.copy()
            img_copy.thumbnail((canvas_width - 10, canvas_height - 10), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img_copy)
            canvas.delete("all")
            canvas.create_image(canvas_width//2, canvas_height//2, image=photo)
            canvas.image = photo
            
        except Exception as e:
            print(f"Display error: {e}")

    
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ConvVisualizer(root)
    root.mainloop()