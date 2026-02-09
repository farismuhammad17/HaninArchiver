import tkinter as tk
from PIL import Image, ImageTk, UnidentifiedImageError

class HaninViewer:
    def view_dupes(self):
        for orig, dupe in self.dupes:
            root = tk.Tk()
            root.title(f"{orig.name} | {dupe.name}")

            try:
                def get_tk_img(path):
                    img = Image.open(path)
                    img.thumbnail((600, 600))
                    return ImageTk.PhotoImage(img)

                img1tk = get_tk_img(orig)
                img2tk = get_tk_img(dupe)

            except UnidentifiedImageError:
                root.destroy()
                continue

            lbl1 = tk.Label(root, image=img1tk)
            lbl1.pack(side="left", padx=10, pady=10)

            lbl2 = tk.Label(root, image=img2tk)
            lbl2.pack(side="left", padx=10, pady=10)

            # Keep references so the images don't disappear due to Garbage Collection
            root.image_refs = [img1tk, img2tk]

            root.mainloop()
