import cv2
from tkinter import Tk, filedialog, messagebox
import os
# Open file dialog to choose an image
Tk().withdraw()  # hide root window
file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
)
if file_path:  # if user selected a file
    # Read image
    image = cv2.imread(file_path)
    # Convert to sketch
    gre_Image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gre_Image)
    blur = cv2.GaussianBlur(invert, (21, 21), 0)
    inverblur = cv2.bitwise_not(blur)
    sketch = cv2.divide(gre_Image, inverblur, scale=256.0)
    # Save in the same folder with "_sketch" name
    folder, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)
    save_path = os.path.join(folder, f"{name}_sketch.png")
    cv2.imwrite(save_path, sketch)
    # --- Resize image to fit screen ---
    root = Tk()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    root.destroy()
    img_h, img_w = sketch.shape[:2]
    scale_w = screen_w / img_w
    scale_h = screen_h / img_h
    scale = min(scale_w, scale_h, 1.0)  # never upscale beyond 100%
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    resized = cv2.resize(sketch, (new_w, new_h), interpolation=cv2.INTER_AREA)
    # Show the resized sketch
    cv2.imshow("Sketch", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
# Show popup with save path
    messagebox.showinfo("Image Saved", f"Your sketch has been saved at:\n{save_path}")
else:
    messagebox.showwarning("No Selection", "No file was selected.")
