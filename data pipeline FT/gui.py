import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
import main # Import your main.py


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BUSA IRP MILE GENERATOR")
        self.geometry("500x400")
        
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # A simple status label
        self.status_label = ttk.Label(self.main_frame, text="Ready to generate report.")
        self.status_label.pack(pady=10)
        
        # The button to run the process
        self.run_button = ttk.Button(self.main_frame, text="Run", command=self.start_process)
        self.run_button.pack(pady=10)
        
        # Text widget for showing the output of print statements
        self.log_text = tk.Text(self.main_frame, height=10, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Redirect standard output to the text widget
        self.old_stdout = sys.stdout
        sys.stdout = self
    
    def write(self, s):
        """Method to redirect print() to the log widget."""
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, s)
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')
    
    def flush(self):
        """Method to handle flushing, required for a file-like object."""
        pass

    def start_process(self):
        """Starts the main process in a new thread."""
        self.run_button.config(state=tk.DISABLED)
        self.status_label.config(text="Processing started. Please wait...")
        
        # Clear previous logs
        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.configure(state='disabled')
        
        # Start the process in a separate thread
        process_thread = threading.Thread(target=self.run_main_in_thread)
        process_thread.start()

    def run_main_in_thread(self):
        """The function that runs in the separate thread."""
        try:
            main.main()
            self.after(0, lambda: self.status_label.config(text="Processing complete!"))
            self.after(0, lambda: messagebox.showinfo("Success", "IFTA Report successfully generated."))
        except Exception as e:
            # We catch the exception raised from main.py and display it
            self.after(0, lambda: self.status_label.config(text=f"An error occurred."))
            self.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {e}"))
        finally:
            # Re-enable the button regardless of success or failure
            self.after(0, lambda: self.run_button.config(state=tk.NORMAL))

if __name__ == "__main__":
    app = App()
    app.mainloop()