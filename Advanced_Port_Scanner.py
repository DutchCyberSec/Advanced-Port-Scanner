import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import shutil

class PortScannerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Port Scanner")

        # Replace 'YourGitHubUsername' and 'YourGitHubRepo' with your GitHub username and repository name
        self.github_username = 'DutchCyberSec'
        self.github_repo = 'Advanced-Port-Scanner'

        # Create menu bar
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        # Update menu
        self.update_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.update_menu.add_command(label="Check for Updates", command=self.check_for_updates)
        self.update_menu.add_command(label="Download New Update", command=self.download_new_update)
        self.menu_bar.add_cascade(label="Update", menu=self.update_menu)

        # Scan menu
        self.scan_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.scan_menu.add_command(label="TCP Scan", command=lambda: self.start_scan("TCP"))
        self.scan_menu.add_command(label="UDP Scan", command=lambda: self.start_scan("UDP"))
        self.scan_menu.add_command(label="ICMP Scan", command=lambda: self.start_scan("ICMP"))
        self.menu_bar.add_cascade(label="Scan", menu=self.scan_menu)

        # Admin Page Scan menu
        self.admin_scan_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.admin_scan_menu.add_command(label="Admin Page Scan", command=self.scan_admin_pages)
        self.menu_bar.add_cascade(label="Admin Scan", menu=self.admin_scan_menu)

        # Display tool name and creator
        self.tool_name_label = ttk.Label(master, text="Tool: Advanced Port Scanner")
        self.tool_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.creator_label = ttk.Label(master, text="Creator: Dutch Cyber Sec")
        self.creator_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # Version label
        self.version_label = ttk.Label(master, text=f"Version: {self.get_current_version()}")
        self.version_label.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # GUI components
        self.target_label = ttk.Label(master, text="Target:")
        self.target_label.grid(row=2, column=0, padx=10, pady=10)

        self.target_entry = ttk.Entry(master)
        self.target_entry.grid(row=2, column=1, padx=10, pady=10)

        self.result_text = tk.Text(master, height=10, width=50)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Disclaimer label
        disclaimer_text = "This tool is for educational purposes only. Use it responsibly and with proper authorization."
        self.disclaimer_label = ttk.Label(master, text=disclaimer_text, font=('Helvetica', 8), foreground='red')
        self.disclaimer_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    
    def get_current_version(self):
        # You can implement your version retrieval logic here
        return "1.2"

    def check_for_updates(self):
        try:
            # Directly download the updated script from GitHub raw URL
            raw_url = f"https://raw.githubusercontent.com/DutchCyberSec/Advanced-Port-Scanner/main/Advanced_Port_Scanner.py"
            response = requests.get(raw_url)

            if response.status_code == 200:
                try:
                    updated_script_path = 'Advanced_Port_Scanner.py'
                    with open(updated_script_path, 'w') as updated_script:
                        updated_script.write(response.text)

                    # Replace the current script with the updated one
                    current_script_path = os.path.abspath(__file__)
                    shutil.move(updated_script_path, current_script_path)

                    messagebox.showinfo("Update Complete", "Script updated successfully. Restart the application.")
                    self.version_label.config(text=f"Version: {self.get_current_version()}")
                except Exception as write_error:
                    messagebox.showerror("Error", f"Error writing updated script: {str(write_error)}")
            else:
                messagebox.showerror("Error", f"Error downloading update: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating script: {str(e)}")

    def download_new_update(self):
        # Replace 'YourGitHubUsername' and 'YourGitHubRepo' with your GitHub username and repository name
        github_username = 'DutchCyberSec'
        github_repo = 'Advanced-Port-Scanner'

        # GitHub API URL to get the latest release
        api_url = f"https://raw.githubusercontent.com/DutchCyberSec/Advanced-Port-Scanner/main/Advanced_Port_Scanner.py"

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                updated_script_path = 'Advanced_Port_Scanner'
                with open(updated_script_path, 'w') as updated_script:
                    updated_script.write(response.text)

                # Replace the current script with the updated one
                current_script_path = os.path.abspath(__file__)
                shutil.move(updated_script_path, current_script_path)

                messagebox.showinfo("Update Complete", "Script updated successfully. Restart the application.")
                self.version_label.config(text=f"Version: {self.get_current_version()}")
            else:
                messagebox.showerror("Error", f"Error downloading update: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating script: {str(e)}")

    def start_scan(self, scan_type):
        target = self.target_entry.get()

        if not target:
            self.result_text.insert(tk.END, "Please enter a target.\n")
            return

        self.result_text.delete(1.0, tk.END)  # Clear previous results
        self.result_text.insert(tk.END, f"Scanning {scan_type} ports on {target}\n")
        self.result_text.insert(tk.END, "-------------------------\n")

        scanner = PortScanner(target, self.result_text)

        if scan_type.lower() == "tcp":
            scanner.start_scan_tcp()
        elif scan_type.lower() == "udp":
            scanner.start_scan_udp()
        elif scan_type.lower() == "icmp":
            scanner.start_scan_icmp()
        else:
            self.result_text.insert(tk.END, "Invalid scan type. Use 'TCP', 'UDP', or 'ICMP'\n")

    def scan_admin_pages(self):
        target = self.target_entry.get()

        if not target:
            self.result_text.insert(tk.END, "Please enter a target.\n")
            return

        # Append http:// or https:// or www. if missing
        if not target.startswith(('http://', 'https://', 'www.')):
            target = 'http://' + target

        self.result_text.delete(1.0, tk.END)  # Clear previous results
        self.result_text.insert(tk.END, f"Scanning for Admin Pages on {target}\n")
        self.result_text.insert(tk.END, "-------------------------\n")

        scanner = AdminPageScanner(target, self.result_text)
        scanner.scan_admin_pages()

class AdminPageScanner:
    def __init__(self, target, result_text):
        self.target = target
        self.result_text = result_text

    def scan_admin_pages(self):
        admin_pages = [
            "/admin",
            "/admin/login",
            "/admin/dashboard",
            # Add more admin page paths as needed
        ]

        for page in admin_pages:
            url = f"{self.target}{page}"
            response = requests.get(url)

            if response.status_code == 200:
                result = f"[+] Found Admin Page: {url}\n"
                self.result_text.insert(tk.END, result)
                self.result_text.yview(tk.END)

def main():
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
