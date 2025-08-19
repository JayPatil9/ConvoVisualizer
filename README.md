# ConvoVisualizer

An interactive tool built with Python and Tkinter that demonstrates 2D convolution operations on grayscale images with real-time animation and pixel-by-pixel visualization.


- **Real-time animation** showing convolution operation pixel-by-pixel
- **Pixel highlighting** on original image during processing
- **Side-by-side comparison** of original and filtered images
- **Multiple preset filters** (Sharpen, Edge Detect, Blur, Emboss, etc.)
- **Custom kernel editing** with 3×3 matrix input

### **Enhanced User Experience**
- **Large image support**
- **Adjustable animation speed** (1-50ms per frame)
- **Optimized performance** with smart frame sampling
- **Professional GUI** with organized control panels
- **Image save functionality** for processed results

### **Educational Value**
- **Step-by-step visualization** of convolution process
- **Immediate visual feedback** showing filter effects
- **Popular filter presets** for learning different effects
- **Interactive kernel customization** for experimentation

## 🚀 Getting Started

### **Prerequisites**
- Python 3.7 or higher
- Required Python packages:
  ```bash
  pip install tkinter numpy pillow
  ```

### **Installation**
1. Clone or download the repository
2. Ensure all dependencies are installed
3. Run the application:
   ```bash
   python main.py
   ```

## 📖 Usage Guide

### **Loading Images**
1. Click **"📁 Load Image"** to select an image file
2. Supported formats: JPG, JPEG, PNG.
3. Images are automatically converted to grayscale and resized (max 400×400)

### **Applying Filters**
1. **Use presets:** Select from dropdown (Sharpen, Edge Detect, Blur, etc.)
2. **Custom kernels:** Edit the 3×3 matrix values manually
3. Click **"⚡ Apply Convolution & Animate"** to start processing

### **Animation Controls**
- **Speed slider:** Adjust animation speed (1-50ms per frame)
- **Real-time progress:** Watch the convolution build up pixel-by-pixel
- **Pixel highlighting:** Red rectangle shows current processing position

### **Additional Features**
- **"🔍 Compare Images":** Opens side-by-side comparison window
- **"💾 Save Result":** Save the filtered image to disk
- **Status updates:** Real-time feedback on processing and animation

## 🔧 Technical Details

### **Optimization Features**
- **Smart frame sampling:** Reduces animation frames for larger images while maintaining visual quality
- **Dynamic performance scaling:**
  - Large images (>200×200): 80 frames
  - Medium images (>100×100): 120 frames  
  - Small images (<100×100): 150 frames
- **Memory efficient:** Optimized image processing and display

### **Architecture**
- **Object-oriented design** with clean separation of concerns
- **Event-driven GUI** with responsive controls
- **Efficient image handling** using PIL/Pillow
- **NumPy-based convolution** for fast mathematical operations


## 📋 Preset Filters Included

| Filter | Effect |  Kernel |
|--------|---------|---------|
| **Sharpen** | Enhances edges and details | $$ \begin{bmatrix} 0 & -1 & 0 \\ -1 & 5 & -1 \\ 0 & -1 & 0 \end {bmatrix} $$ |
| **Edge Detect** | Highlights object boundaries | $$ \begin{bmatrix} -1 & -1 & -1 \\ -1 & 8 & -1 \\ -1 & -1 & -1 \end {bmatrix} $$ |
| **Blur** | Smooths image details |  $$ \frac{1}{9} \begin{bmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end {bmatrix} $$ |
| **Emboss** | Creates 3D-like effect | $$ \begin{bmatrix} -2 & 1 & 0 \\ -1 & 1 & 1 \\ 0 & 1 & 2 \end {bmatrix} $$ |
| **Sobel X** | Detects vertical edges | $$ \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end {bmatrix} $$ |
| **Laplacian** | Edge enhancement | $$ \begin{bmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0 \end {bmatrix} $$ |
| **Identity** | No change (reference) | $$ \begin{bmatrix} 0 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end {bmatrix} $$ |


## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Additional filter presets
- Support for color images
- Export animation as GIF/video
- Larger kernel sizes (5×5, 7×7)


## 🙏 Acknowledgments

- Built with Tkinter
- Image processing powered by PIL/Pillow
- Mathematical operations optimized with NumPy