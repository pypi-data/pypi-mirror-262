import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

from ladock.ladock.ladockGUI import docking_conf
from ladock.md.gmxGUI import md_conf
from ladock.getdata.getdataGUI import getdata_conf
from ladock.dl.dlGUI import dl_conf
from ladock.test.testGUI import test_conf
from ladock.alphagl.alphaglGUI import alphagl_conf
from ladock.egfr.egfrGUI import egfr_conf


class LADOCKApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LADOCK - The Tools for AI Enabled Drug Design")
        self.style = ThemedStyle(root)
        self.style.set_theme("clearlooks")
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("TEntry", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("LabelFrame",
                             font=("Arial", 12),
                             foreground="blue",  # Warna teks
                             background="#E0E0E0",  # Warna latar belakang (gunakan kode warna HTML)
                             padding=(10, 5),  # Padding LabelFrame
                             borderwidth=2,  # Ketebalan garis frame
                             relief="solid"  # Jenis relief frame
                             )

        # Main Frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="ns")  
           
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Main Atas
        self.main_frame_up = ttk.Frame(self.main_frame)
        self.main_frame_up.grid(column=0, row=0)
        
        # Main Bawah
        self.main_frame_bottom = ttk.Frame(self.main_frame)
        self.main_frame_bottom.grid(column=0, row=1, sticky="ns")
        self.main_frame_bottom.grid_rowconfigure(0, weight=1)
        
        # Variable to track the selected option
        self.selected_option = tk.StringVar(value="Molecular Docking")

        # Create Radiobuttons for selecting options
        self.options = [
            "Molecular Docking", "Molecular Dynamics", "Descriptors Calculation", "Generate AI Model",
            "AI-driven Drug Screening", "EGFR Inhibitor Prediction", "Alpha Glucosidase Inhibitor Prediction"
        ]
        self.style.configure("Menu.TButton", font=("Arial", 10, "bold"))

        for i, option in enumerate(self.options):
            radiobutton = ttk.Radiobutton(
                self.main_frame_up,
                text=option,
                style="Menu.TButton",
                variable=self.selected_option,
                value=option,
                command=self.show_selected_frame
            )
            radiobutton.grid(column=i, row=0, sticky="ew")
            self.main_frame_up.columnconfigure(i, weight=1)

        # Frame 1
        self.frame1 = ttk.Frame(self.main_frame_bottom)
        self.frame1.grid(column=0, row=1, pady=(5, 0))
        docking_conf(self.frame1)

        # Frame 2
        self.frame2 = ttk.Frame(self.main_frame_bottom)
        self.frame2.grid(column=0, row=1, pady=(5, 0))
        self.frame2.grid_remove()
        md_conf(self.frame2)

        # Frame 3
        self.frame3 = ttk.Frame(self.main_frame_bottom)
        self.frame3.grid(column=0, row=1, pady=(5, 0))
        self.frame3.grid_remove()
        getdata_conf(self.frame3)

        # Frame 4
        self.frame4 = ttk.Frame(self.main_frame_bottom)
        self.frame4.grid(column=0, row=1, pady=(5, 0))
        self.frame4.grid_remove()
        dl_conf(self.frame4)

        # Frame 5
        self.frame5 = ttk.Frame(self.main_frame_bottom)
        self.frame5.grid(column=0, row=1, pady=(5, 0))
        self.frame5.grid_remove()
        test_conf(self.frame5)

        # Frame 6
        self.frame6 = ttk.Frame(self.main_frame_bottom)
        self.frame6.grid(column=0, row=1, pady=(5, 0))
        self.frame6.grid_remove()
        egfr_conf(self.frame6)

        # Frame 7
        self.frame7 = ttk.Frame(self.main_frame_bottom)
        self.frame7.grid(column=0, row=1, pady=(5, 0))
        self.frame7.grid_remove()
        alphagl_conf(self.frame7)

    def show_selected_frame(self):
        # Hide all frames in main_frame_bottom
        for frame in [self.frame1, self.frame2, self.frame3, self.frame4, self.frame5, self.frame6, self.frame7]:
            if frame:
                frame.grid_remove()

        # Show the selected frame
        selected_option = self.selected_option.get()
        if selected_option == "Molecular Docking":
            self.frame1.grid()
        elif selected_option == "Molecular Dynamics":
            self.frame2.grid()
        elif selected_option == "Descriptors Calculation":
            self.frame3.grid()
        elif selected_option == "Generate AI Model":
            self.frame4.grid()
        elif selected_option == "AI-driven Drug Screening":
            self.frame5.grid()
        elif selected_option == "EGFR Inhibitor Prediction":
            self.frame6.grid()
        elif selected_option == "Alpha Glucosidase Inhibitor Prediction":
            self.frame7.grid()
        self.main_frame_bottom.update()


def main():
    # Membuat root window
    root = tk.Tk()
    app = LADOCKApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
