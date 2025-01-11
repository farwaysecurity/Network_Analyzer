import tkinter as tk
from tkinter import ttk
import psutil
import socket
import threading
import time



class NetworkAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Farway Network Analyzer 0.0.1")
       
        self.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create connections treeview
        self.tree = ttk.Treeview(self.main_frame, columns=('Protocol', 'Local Address', 'Remote Address', 'Status'))
        self.tree.heading('#0', text='ID')
        self.tree.heading('Protocol', text='Protocol')
        self.tree.heading('Local Address', text='Local Address')
        self.tree.heading('Remote Address', text='Remote Address')
        self.tree.heading('Status', text='Status')
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Create stats frame
        self.stats_frame = ttk.LabelFrame(self.main_frame, text="Network Statistics")
        self.stats_frame.pack(fill=tk.X, pady=10)
        
        # Stats labels
        self.bytes_sent = ttk.Label(self.stats_frame, text="Bytes Sent: 0")
        self.bytes_sent.pack(side=tk.LEFT, padx=10)
        
        self.bytes_recv = ttk.Label(self.stats_frame, text="Bytes Received: 0")
        self.bytes_recv.pack(side=tk.LEFT, padx=10)
        
        # Start monitoring thread
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_network)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def monitor_network(self):
        counter = 0
        while self.running:
            # Clear previous entries
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Get network connections
            connections = psutil.net_connections()
            for conn in connections:
                try:
                    protocol = 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP'
                    laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                    raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    status = conn.status
                    
                    self.tree.insert('', tk.END, text=str(counter), 
                                   values=(protocol, laddr, raddr, status))
                    counter += 1
                except:
                    continue
            
            # Update network stats
            net_stats = psutil.net_io_counters()
            self.bytes_sent.config(text=f"Bytes Sent: {net_stats.bytes_sent}")
            self.bytes_recv.config(text=f"Bytes Received: {net_stats.bytes_recv}")
            
            time.sleep(2)
    
    def on_closing(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    app = NetworkAnalyzer()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
