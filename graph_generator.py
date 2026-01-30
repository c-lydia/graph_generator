import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class EngineeringGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Engineering Graph Generator")
        self.fig = None
        self.curves = []

        self.create_widgets()

    def create_widgets(self):
        # --- Graph Type Selection ---
        type_frame = ttk.LabelFrame(self.root, text="Graph Type", padding=10)
        type_frame.pack(fill="x", padx=10, pady=5)

        self.graph_type = ttk.Combobox(type_frame, values=[
            "Custom Plot",
            "BJT Load Line"
        ], width=20)
        self.graph_type.set("BJT Load Line") # Set default to BJT for convenience
        self.graph_type.pack(side="left", padx=5)

        # --- General Graph Settings ---
        settings = ttk.LabelFrame(self.root, text="Graph Settings (Custom Plot Only)", padding=10)
        settings.pack(fill="x", padx=10, pady=5)

        ttk.Label(settings, text="Title:").grid(row=0, column=0, sticky="w")
        self.entry_title = ttk.Entry(settings, width=40)
        self.entry_title.grid(row=0, column=1)

        ttk.Label(settings, text="X-axis Label:").grid(row=1, column=0, sticky="w")
        self.entry_xlabel = ttk.Entry(settings, width=40)
        self.entry_xlabel.grid(row=1, column=1)

        ttk.Label(settings, text="Y-axis Label:").grid(row=2, column=0, sticky="w")
        self.entry_ylabel = ttk.Entry(settings, width=40)
        self.entry_ylabel.grid(row=2, column=1)
        
        # --- BJT Load Line Parameters ---
        bjt_frame = ttk.LabelFrame(self.root, text="BJT Load Line Parameters", padding=10)
        bjt_frame.pack(fill="x", padx=10, pady=5)

        # Defaults based on your handwritten image
        ttk.Label(bjt_frame, text="VCC (V):").grid(row=0, column=0, sticky="w")
        self.entry_vcc = ttk.Entry(bjt_frame, width=20)
        self.entry_vcc.grid(row=0, column=1)
        self.entry_vcc.insert(0, "22") 

        ttk.Label(bjt_frame, text="RC (Ω):").grid(row=1, column=0, sticky="w")
        self.entry_rc = ttk.Entry(bjt_frame, width=20)
        self.entry_rc.grid(row=1, column=1)
        self.entry_rc.insert(0, "10000")

        ttk.Label(bjt_frame, text="RE (Ω):").grid(row=2, column=0, sticky="w")
        self.entry_re = ttk.Entry(bjt_frame, width=20)
        self.entry_re.grid(row=2, column=1)
        self.entry_re.insert(0, "1500")

        ttk.Label(bjt_frame, text="IB (μA):").grid(row=3, column=0, sticky="w")
        self.entry_ib = ttk.Entry(bjt_frame, width=20)
        self.entry_ib.grid(row=3, column=1)
        self.entry_ib.insert(0, "5.96")

        ttk.Label(bjt_frame, text="Beta:").grid(row=4, column=0, sticky="w")
        self.entry_beta = ttk.Entry(bjt_frame, width=20)
        self.entry_beta.grid(row=4, column=1)
        self.entry_beta.insert(0, "178")
        
        # --- Custom Curve Input ---
        curve_frame = ttk.LabelFrame(self.root, text="Add Custom Curve", padding=10)
        curve_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(curve_frame, text="Curve Name:").grid(row=0, column=0, sticky="w")
        self.entry_curve_name = ttk.Entry(curve_frame, width=30)
        self.entry_curve_name.grid(row=0, column=1)

        ttk.Label(curve_frame, text="X values:").grid(row=1, column=0, sticky="w")
        self.entry_x = ttk.Entry(curve_frame, width=50)
        self.entry_x.grid(row=1, column=1)

        ttk.Label(curve_frame, text="Y values:").grid(row=2, column=0, sticky="w")
        self.entry_y = ttk.Entry(curve_frame, width=50)
        self.entry_y.grid(row=2, column=1)

        ttk.Label(curve_frame, text="Plot Type:").grid(row=3, column=0, sticky="w")
        self.plot_type = ttk.Combobox(curve_frame, values=["Line", "Scatter", "Line+Scatter"], width=15)
        self.plot_type.set("Line")
        self.plot_type.grid(row=3, column=1, sticky="w")

        ttk.Button(curve_frame, text="Add Curve", command=self.add_curve).grid(row=4, column=0, pady=5)
        ttk.Button(curve_frame, text="Clear Curves", command=self.clear_curves).grid(row=4, column=1, pady=5)

        # --- Actions ---
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(action_frame, text="Generate Graph", command=self.generate_graph).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Save Graph", command=self.save_graph).pack(side="left", padx=5)

        # --- Plot Area ---
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ---------------- ADD CURVE ----------------
    def add_curve(self):
        try:
            name = self.entry_curve_name.get() or f"Curve {len(self.curves)+1}"
            x_vals = list(map(float, self.entry_x.get().split(",")))
            y_vals = list(map(float, self.entry_y.get().split(",")))
            if len(x_vals) != len(y_vals):
                messagebox.showerror("Error", "X and Y must have the same length.")
                return
            style = self.plot_type.get()
            self.curves.append((name, x_vals, y_vals, style))
            messagebox.showinfo("Added", f"Curve '{name}' added.")
            self.entry_curve_name.delete(0, tk.END)
            self.entry_x.delete(0, tk.END)
            self.entry_y.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def clear_curves(self):
        self.curves.clear()
        messagebox.showinfo("Cleared", "All curves removed.")

    # ---------------- GENERATE GRAPH ----------------
    def generate_graph(self):
        if self.graph_type.get() == "BJT Load Line":
            self.generate_bjt_load_line()
            return

        # Custom / multipurpose plot
        if not self.curves:
            messagebox.showwarning("Warning", "No curves to plot.")
            return

        self.fig, ax = plt.subplots(figsize=(7,5))
        title = self.entry_title.get()
        xlabel = self.entry_xlabel.get()
        ylabel = self.entry_ylabel.get()

        for name, x_vals, y_vals, style in self.curves:
            if style == "Line":
                ax.plot(x_vals, y_vals, label=name)
            elif style == "Scatter":
                ax.scatter(x_vals, y_vals, label=name)
            elif style == "Line+Scatter":
                ax.plot(x_vals, y_vals, marker="o", label=name)

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend()

        self.draw_figure()

    # ---------------- BJT LOAD LINE (CORRECTED) ----------------
    def generate_bjt_load_line(self):
        try:
            VCC = float(self.entry_vcc.get())
            RC = float(self.entry_rc.get())
            RE = float(self.entry_re.get())
            IB_uA = float(self.entry_ib.get())
            IB = IB_uA * 1e-6  # Convert to Amps
            beta = float(self.entry_beta.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid BJT parameters.")
            return

        # Total resistance in the loop
        R_total = RC + RE

        # 1. Calculate Load Line Points
        # Y-intercept: Saturation current (Ic_sat) when Vce = 0
        Ic_sat = VCC / R_total
        
        # X-intercept: Cutoff voltage (Vce_off) when Ic = 0
        Vce_off = VCC

        # Create data points for plotting the load line
        VCE_load = np.linspace(0, VCC, 100)
        IC_load_line = (VCC - VCE_load) / R_total

        # 2. Calculate Transistor Characteristic Curve
        # We use a tanh function to simulate the realistic "knee" behavior at origin
        # instead of a flat constant line.
        VCE_curve = np.linspace(0, VCC * 1.1, 200)
        Ic_max_theory = beta * IB
        # np.tanh(VCE / 0.7) creates the curve shape starting from 0 and flattening out
        IC_curve = Ic_max_theory * np.tanh(VCE_curve / 0.7)

        # 3. Calculate Q-Point (Intersection)
        # Theoretical Q-point based on KVL
        Ic_q = beta * IB
        Vce_q = VCC - Ic_q * R_total

        # --- PLOTTING ---
        self.fig, ax = plt.subplots(figsize=(8, 6))

        # Plot Load Line (Blue)
        ax.plot(VCE_load, IC_load_line * 1e3, color='navy', linewidth=2, label='DC Load Line')

        # Plot Characteristic Curve (curved line)
        ax.plot(VCE_curve, IC_curve * 1e3, color='royalblue', label=f'IB = {IB_uA} µA')

        # Plot Q-point (Red Dot)
        ax.scatter([Vce_q], [Ic_q * 1e3], color='red', s=80, zorder=10, label='Q-point')

        # --- ANNOTATIONS (Matching the handwritten image) ---
        
        # Label Y-intercept (1.91 mA)
        ax.annotate(f'{Ic_sat*1e3:.2f} mA', 
                    xy=(0, Ic_sat*1e3), 
                    xytext=(1, Ic_sat*1e3),
                    arrowprops=dict(facecolor='black', arrowstyle="->"),
                    fontsize=10)

        # Label X-intercept (22 V)
        ax.annotate(f'{Vce_off} V', 
                    xy=(Vce_off, 0), 
                    xytext=(Vce_off - 3, 0.1),
                    arrowprops=dict(facecolor='black', arrowstyle="->"),
                    fontsize=10)

        # Label Q-point coordinates
        ax.text(Vce_q + 0.5, (Ic_q * 1e3) + 0.1, 
                f"Q ({Vce_q:.1f}V, {Ic_q*1e3:.2f}mA)", 
                fontsize=9, fontweight='bold', color='darkred')
        
        # Label the Curve on the right side
        ax.text(VCE_curve[-1], IC_curve[-1]*1e3, f" IB={IB_uA} µA", va='center')

        # Formatting axes
        ax.set_title("BJT DC Load Line Analysis")
        ax.set_xlabel("$V_{CE}$ (Volts)")
        ax.set_ylabel("$I_C$ (mA)")
        
        # Set limits to include origin and provide some breathing room
        ax.set_xlim(left=0, right=VCC * 1.1)
        ax.set_ylim(bottom=0, top=Ic_sat * 1e3 * 1.2)
        
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()

        self.draw_figure()

    def draw_figure(self):
        for w in self.plot_frame.winfo_children():
            w.destroy()
        canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------------- SAVE ----------------
    def save_graph(self):
        if self.fig is None:
            messagebox.showwarning("Warning", "Generate a graph first.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image","*.png"), ("JPEG Image","*.jpg"), ("PDF File","*.pdf")]
        )
        if file_path:
            self.fig.savefig(file_path)
            messagebox.showinfo("Saved", f"Graph saved:\n{file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    # Handle high-DPI displays (optional but recommended for clear text)
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
        
    app = EngineeringGraphApp(root)
    root.mainloop()