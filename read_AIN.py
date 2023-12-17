import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import u3

class LabJackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LabJack AIN0 Voltage Monitor")

        # Set up LabJack device
        self.lj = u3.U3()
        self.lj.configU3()

        # Prompt user to apply 0 pressure
        messagebox.showinfo("Setup", "Please apply 0 (atmospheric) pressure, then click OK.")

        # Read initial voltage and set as offset
        self.offset_voltage = self.read_voltage()

        self.figure = Figure(figsize=(10, 4), dpi=100)
        self.ax = self.figure.add_subplot(121)  # First subplot for the bar graph
        self.ax2 = self.ax.twinx()  # Secondary y-axis for Bar
        self.ax3 = self.figure.add_subplot(122)  # Second subplot for the pressure graph

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.pressure_readings = [0] * 60  # Store last 60 readings, initialize with zeros.

        # Start the update loops
        self.update_bar_plot()
        self.update_pressure_plot()

        # Bind the window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def psi_to_bar(self, psi):
        return psi * 0.0689476

    def read_voltage(self):
        return self.lj.getAIN(0)

    def update_bar_plot(self):
        voltage = self.read_voltage()
        adjusted_voltage = voltage - self.offset_voltage
        psi = adjusted_voltage / 6.0 * 5000
        bar = self.psi_to_bar(psi)

        self.ax.clear()
        self.ax2.clear()

        self.ax.bar(['Pressure'], [psi], color='blue')
        self.ax.set_ylim(0, 6000)
        self.ax.set_ylabel('Pressure (PSI)')

        self.ax2.set_ylim(0, self.psi_to_bar(6000))

        self.ax.text(0.5, -0.1, f'Pressure: {psi:.2f} PSI', horizontalalignment='center', 
                     verticalalignment='top', transform=self.ax.transAxes)

        self.canvas.draw()

        # Update the bar plot every 100 milliseconds (10 Hz)
        self.after(100, self.update_bar_plot)

    def update_pressure_plot(self):
        voltage = self.read_voltage()
        adjusted_voltage = voltage - self.offset_voltage
        psi = adjusted_voltage / 6.0 * 5000

        # Update the readings list
        self.pressure_readings.insert(0, psi)
        self.pressure_readings = self.pressure_readings[:60]

        self.ax3.clear()
        self.ax3.plot(range(60), self.pressure_readings, '-', color='blue')
        self.ax3.set_ylim(0, 6000)
        self.ax3.set_ylabel('Pressure (Bar)')
        self.ax3.set_xlabel('Last 60 readings')
        self.ax3.set_xlim(0, 59)

        # Avoid overlapping labels
        self.figure.tight_layout()
        self.canvas.draw()

        self.canvas.draw()

        # Update the pressure plot every second (1 Hz)
        self.after(500, self.update_pressure_plot)

    def on_closing(self):
        self.lj.close()
        self.destroy()

if __name__ == "__main__":
    app = LabJackApp()
    app.mainloop()
