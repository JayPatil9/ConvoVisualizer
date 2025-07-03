import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk

class ConvVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("2D Convolution Visualizer")
        self.root.geometry("750x500")
        
        self.original_image = None
        self.processed_image = None
        self.current_kernel = np.array([[0, -1, 0], [-1, 5, -1], [-0, -1, 0]])
        
        self.setup_gui()

    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        ttk.Button(control_frame, text="Load Image", command=self.load_image).grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Label(control_frame, text="Kernel (3x3):").grid(row=1, column=0, columnspan=2, pady=(20, 5))
        
        self.kernel_entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = ttk.Entry(control_frame, width=6, justify='center')
                entry.grid(row=i+2, column=j, padx=2, pady=2)
                entry.insert(0, str(self.current_kernel[i][j]))
                row_entries.append(entry)
            self.kernel_entries.append(row_entries)
        
        ttk.Button(control_frame, text="Apply Convolution", command=self.apply_convolution).grid(row=5, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        display_frame = ttk.LabelFrame(main_frame, text="Image Display", padding="10")
        display_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.canvas = tk.Canvas(display_frame, bg='white', width=800, height=600)
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        h_scrollbar = ttk.Scrollbar(display_frame, orient='horizontal', command=self.canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        v_scrollbar = ttk.Scrollbar(display_frame, orient='vertical', command=self.canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        
        if file_path:
            try:
                pil_image = Image.open(file_path)
                
                if pil_image.mode != 'L':
                    self.previous_mode = pil_image.mode
                    pil_image = pil_image.convert('L')
                
                max_size = 500
                if pil_image.width > max_size or pil_image.height > max_size:
                    pil_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                self.original_image = np.array(pil_image)
                
                self.display_image(pil_image)
                
                messagebox.showinfo("Success", f"Image loaded successfully!\nSize: {self.original_image.shape}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def display_image(self, pil_image):
        photo = ImageTk.PhotoImage(pil_image.convert(self.previous_mode if hasattr(self, 'previous_mode') else 'L'))
        
        self.canvas.delete("all")
        
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def get_kernel_from_entries(self):
        try:
            kernel = np.zeros((3, 3))
            for i in range(3):
                for j in range(3):
                    kernel[i][j] = float(self.kernel_entries[i][j].get())
            return kernel
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for kernel values")
            return None
        
    def apply_convolution(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        kernel = self.get_kernel_from_entries()
        if kernel is None:
            return
        
        try:
            result = self.convolve2d(self.original_image, kernel)
            
            result_normalized = np.clip(result, 0, 255).astype(np.uint8)
            result_pil = Image.fromarray(result_normalized)
            
            self.display_image(result_pil)
            self.processed_image = result_normalized
            
            messagebox.showinfo("Success", "Convolution applied successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Convolution failed: {str(e)}")

    def convolve2d(self, image, kernel):
        img_height, img_width = image.shape
        kernel_height, kernel_width = kernel.shape
        
        pad_h = kernel_height // 2
        pad_w = kernel_width // 2
        
        padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
        
        output = np.zeros_like(image, dtype=np.float32)
        
        for i in range(img_height):
            for j in range(img_width):
                roi = padded_image[i:i+kernel_height, j:j+kernel_width]
                
                output[i, j] = np.sum(roi * kernel)
        
        return output
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ConvVisualizer(root)
    root.mainloop()