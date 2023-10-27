import tkinter as tk
from tkinter import  ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter  import PhotoImage
from tkinter import *
from PIL import ImageTk, Image
import xmlrpc.client
 
       

class FlowRateAppClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Navistar Flow Meter Test Bench")
        self.root.configure(bg='lightblue')
       # self.server_proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

        # Flow rate display label
        self.flow_rate_label = ttk.Label(root, text="Flow Rate: 0 GPM",style='Large.TButton')
        self.flow_rate_label.grid(row=0, column=0, pady=30)

        # Start and Stop buttons
        self.start_button = ttk.Button(root, text="Start Measurement", command=self.start_measurement,style='Large.TButton')
        self.stop_button = ttk.Button(root, text="Stop Measurement", command=self.stop_measurement, state=tk.DISABLED,style='Large.TButton')

        self.start_button.grid(row=1, column=0, padx=10, pady=30)
        self.stop_button.grid(row=1, column=1, padx=10, pady=30)
        
        
        #Create Menu
        menu = tk.Menu(root)
        root.config(menu=menu)
        
        filemenu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New',command=self.refresh_window)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=root.quit)
        
        self.tabs = ttk.Notebook(root,style="Custom .TNotebook")
        self.tabs.grid(row=0, column=2, padx=30, pady=30)

        # Additional buttons
        email_frame = ttk.Frame(self.tabs)
        self.tabs.add(email_frame, text="Email")
        email_button = ttk.Button(email_frame, text="Send Email",command=self.send_email)
        entry= ttk.Entry(email_frame)
        entry.grid(padx=20,pady=20)


        
        
        waveform_button = ttk.Button(root, text="Waveform", command=self.show_waveform,style= 'Large.TButton')
        waveform_button.grid(padx=20, pady=20,row=1,column=2)
        
        raw_data_frame = ttk.Frame(self.tabs)
        self.tabs.add(raw_data_frame, text="Raw Data")
        raw_data_button = ttk.Button(raw_data_frame, text="Show Raw Data", command=self.show_raw_data)
        raw_data_button.grid(padx=10, pady=10,row=1,column=3)



        
        # Create a custom ttk style for larger buttons
        self.style = ttk.Style()
        self.style.configure('Large.TButton', font=('Helvetica', 20), padding=15)

        # Measurement variables
        self.is_measuring = False
        self.flow_rate_value = 0
        self.time_intervals = []  # To store time intervals for the waveform plot
        self.flow_rate_history = []  # To store flow rate data for the waveform plot

        # Matplotlib figure for the waveform plot
        self.fig, self.ax = plt.subplots(figsize=(10,5)) #Adjust width and height
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=3, column=4, padx=30, pady=40)

    
    def start_measurement(self):
        self.is_measuring = True
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        self.measure_flow_rate()

    def stop_measurement(self):
        self.is_measuring = False
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)

    #def update_flow_rate(self):
        # Get the flow rate from the server
        #flow_rate = self.server_proxy.get_flow_rate()
        #self.flow_rate_label.configure(text=f"Flow Rate: {flow_rate:.2f} L/s")
        #self.root.after(1000, self.update_flow_rate)  # Update every 1 second   

    def measure_flow_rate(self):
        if self.is_measuring:
            # Replace this with your actual flow rate measurement logic
            # For simulation purposes, we're updating the flow rate value
            self.flow_rate_value += 0.1  # Simulated increment
            self.flow_rate_label.configure(text=f"Flow Rate: {self.flow_rate_value:.2f} GPM")
            
            # Store flow rate data for the waveform plot
            self.flow_rate_history.append(self.flow_rate_value)
            self.time_intervals.append(len(self.flow_rate_history)*2)  # 2-second intervals
            
            # Update the waveform plot
            self.update_waveform_plot()

            self.root.after(2000, self.measure_flow_rate)  # Repeat every 2 seconds (2000 milliseconds)

    def send_email(self):
        # Add your code to send an email with flow rate data
        pass

    
    def show_waveform(self):
        # Update the waveform plot when the "Waveform" button is pressed
        self.update_waveform_plot()

    def update_waveform_plot(self):
        self.ax.clear()
        self.ax.plot(self.time_intervals, self.flow_rate_history, label='Tested Flow Rate (GPM)')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Flow Rate (GPM)')
        self.ax.legend()
        self.canvas.draw()

    def show_raw_data(self):
        # Add your code to display raw data of flow rate measurements
        pass

    def refresh_window(self):
        # Destroy existing widgets and recreate the GUI
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)
    
    
    
    

def main():
    root=tk.Tk()
    image_path= PhotoImage(file=r"C:\Users\faral\Downloads\Navistar logo(resize).png") #image defined and image path
    bg_image= tk.Label(root,image=image_path) #image set in window 
    bg_image.place(relheight=0.5,relwidth=0.25) #image size
    bg_image.grid(row=0,column=4)#image location in the window
    
    #def callback(e):
    # image_path2 = ImageTk.PhotoImage(Image.open(file=r"C:\Users\faral\Downloads\Navistar logo(resize).png"))
     #bg_image.configure(image=image_path2)
     #bg_image = image_path2

    # root.bind("<Return>", e)
    
    
    app= FlowRateAppClient(root)
    root.mainloop()
    
    

if __name__ == "__main__":
    main()
