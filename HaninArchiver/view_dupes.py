import tkinter as tk

from PIL import Image, ImageTk, UnidentifiedImageError

class HaninViewer:
    def view_dupes(self):
        for orig, dupe in self.dupes:
            win1 = tk.Tk()
            win2 = tk.Toplevel(win1)

            win1.title(orig.name)
            win2.title(dupe.name)

            try:
                img1 = Image.open(orig)
                img1tk = ImageTk.PhotoImage(img1)

                img2 = Image.open(dupe)
                img2tk = ImageTk.PhotoImage(img2)

            except UnidentifiedImageError:
                continue

            tk.Label(win1, image=img1tk).pack(side="left", padx=10)
            tk.Label(win2, image=img2tk).pack(side="left", padx=10)

            win1.images = img1tk, img2tk
            win1.mainloop()
