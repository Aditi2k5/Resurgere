import tkinter as tk
from tkinter import ttk, messagebox
import time
import random
from threading import Thread
import webbrowser
import subprocess
import sys
import os

class EmergencyResponseSystem:
    def _init_(self, master):
        self.master = master
        self.master.title("Emergency Response System")
        self.master.geometry("400x600")
        self.master.configure(bg="#f0f0f0")  # Light gray background

        self.user_location = None
        self.emergency_contacts = []
        self.emergency_services = {
            "Police": "100",
            "Ambulance": "108"
        }

        self.create_widgets()
        self.start_gps_tracking()

    def create_widgets(self):
        # Create a frame for the SOS button
        sos_frame = tk.Frame(self.master, bg="#f0f0f0")
        sos_frame.pack(pady=20)

        # SOS Button
        button_size = 150  # Diameter of the button
        self.sos_button = tk.Canvas(sos_frame, width=button_size, height=button_size, 
                                    bg="#f0f0f0", highlightthickness=0)
        self.sos_button.pack()

        # Create a circle on the canvas with a gradient effect
        padding = 5  # Space between the edge of the canvas and the circle
        x0, y0, x1, y1 = padding, padding, button_size - padding, button_size - padding
        self.sos_button.create_oval(x0, y0, x1, y1, fill='#ff0000', outline='#cc0000', width=2, tags='sos')
        self.sos_button.create_text(button_size/2, button_size/2, text="SOS", 
                                    font=("Arial", 28, "bold"), fill="white", tags='sos')

        # Bind click event
        self.sos_button.tag_bind('sos', '<Button-1>', self.activate_sos)

        # Tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#f0f0f0")
        style.configure("TNotebook.Tab", background="#e0e0e0", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#ffffff")])

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Messages Tab (Replacing the location tab with the messages)
        messages_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(messages_frame, text="Messages")
        self.messages_text = tk.Text(messages_frame, wrap=tk.WORD, height=10, font=("Arial", 12), bg="#ffffff")
        self.messages_text.pack(pady=10, padx=10, fill="both", expand=True)

        # Contacts Tab
        contacts_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(contacts_frame, text="Contacts")
        ttk.Label(contacts_frame, text="Name:", font=("Arial", 12)).pack(pady=5)
        self.contact_name_entry = ttk.Entry(contacts_frame, width=40, font=("Arial", 12))
        self.contact_name_entry.pack(pady=5)
        ttk.Label(contacts_frame, text="Number:", font=("Arial", 12)).pack(pady=5)
        self.contact_number_entry = ttk.Entry(contacts_frame, width=40, font=("Arial", 12))
        self.contact_number_entry.pack(pady=5)
        ttk.Button(contacts_frame, text="Add Contact", command=self.add_emergency_contact,
                   style='TButton').pack(pady=10)
        self.contacts_listbox = tk.Listbox(contacts_frame, width=40, height=5, font=("Arial", 12))
        self.contacts_listbox.pack(pady=10)

        # Emergency Services Tab
        services_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(services_frame, text="Services")
        for service, number in self.emergency_services.items():
            ttk.Label(services_frame, text=f"{service}: {number}", 
                      font=("Arial", 12, "bold")).pack(pady=10)

    def start_gps_tracking(self):
        def gps_loop():
            while True:
                try:
                    # Simulating GPS data for demonstration
                    self.user_location = (random.uniform(-90, 90), random.uniform(-180, 180))
                    time.sleep(5)
                except Exception as e:
                    print(f"GPS Error: {e}")
                    time.sleep(5)
        Thread(target=gps_loop, daemon=True).start()

    def add_emergency_contact(self):
        name = self.contact_name_entry.get()
        number = self.contact_number_entry.get()
        if name and number:
            self.emergency_contacts.append({"name": name, "number": number})
            self.contacts_listbox.insert(tk.END, f"{name}: {number}")
            self.contact_name_entry.delete(0, tk.END)
            self.contact_number_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter both name and number.")

    def activate_sos(self, event=None):
        if not self.user_location:
            messagebox.showerror("Error", "Location not available. Please wait for GPS signal.")
            return

        response = messagebox.askokcancel("SOS Activation", "Are you sure you want to activate the emergency response system?")
        if response:
            self.sos_button.config(state="disabled")
            Thread(target=self._sos_sequence).start()

    def _sos_sequence(self):
        self.update_status("Contacting emergency services...")
        self.call_emergency_services()

        for contact in self.emergency_contacts:
            self.update_status(f"Alerting {contact['name']} at {contact['number']}...")
            time.sleep(1)

        self.update_status("Emergency response completed.")
        self.sos_button.config(state="normal")

    def call_emergency_services(self):
        for service, number in self.emergency_services.items():
            self.simulate_phone_call(service, number)

    def simulate_phone_call(self, service, number):
        self.update_status(f"Calling {service} ({number})...")
        time.sleep(5)
        self.update_status(f"Call to {service} ({number}) ended.")

    def update_status(self, message):
        self.messages_text.insert(tk.END, f"{message}\n")
        self.messages_text.see(tk.END)
        self.master.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = EmergencyResponseSystem(root)
    root.mainloop()