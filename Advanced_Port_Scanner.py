import tkinter as tk
from tkinter import ttk, messagebox
import requests
from threading import Thread

class PortScannerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Port Scanner")

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
        # GUI components
        self.target_label = ttk.Label(master, text="Target:")
        self.target_label.grid(row=1, column=0, padx=10, pady=10)

        self.target_entry = ttk.Entry(master)
        self.target_entry.grid(row=1, column=1, padx=10, pady=10)

        self.result_text = tk.Text(master, height=10, width=50)
        self.result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Disclaimer label
        disclaimer_text = "This tool is for educational purposes only. Use it responsibly and with proper authorization."
        self.disclaimer_label = ttk.Label(master, text=disclaimer_text, font=('Helvetica', 8), foreground='red')
        self.disclaimer_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    def check_for_updates(self):
        # Replace 'YourGitHubUsername' and 'YourGitHubRepo' with your GitHub username and repository name
        github_username = 'DutchCyberSec'
        github_repo = 'YourGitHubRepo'

        # GitHub API URL to get the latest release
        api_url = f"https://api.github.com/repos/{github_username}/{github_repo}/releases/latest"

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                latest_version = response.json()['tag_name']
                current_version = '1.0'  # Replace with your actual current version

                if current_version < latest_version:
                    message = f"A new version ({latest_version}) is available. Do you want to update?"
                    response = messagebox.askyesno("Update Available", message)
                    if response:
                        # Implement the update logic here
                        self.download_new_update()
                else:
                    messagebox.showinfo("No Updates", "Your script is up to date.")
            else:
                messagebox.showerror("Error", f"Error checking for updates: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error checking for updates: {str(e)}")

    def download_new_update(self):
        # Replace 'YourGitHubUsername' and 'YourGitHubRepo' with your GitHub username and repository name
        github_username = 'DutchCyberSec'
        github_repo = 'YourGitHubRepo'

        # GitHub API URL to get the latest release
        api_url = f"https://api.github.com/repos/{github_username}/{github_repo}/releases/latest"

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                download_url = response.json()['zipball_url']
                download_path = 'update.zip'

                # Download the zip file
                with requests.get(download_url) as download_response:
                    with open(download_path, 'wb') as zip_file:
                        zip_file.write(download_response.content)

                # Extract the contents
                extract_path = 'update'
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)

                # Copy the updated files to the script directory
                for item in os.listdir(extract_path):
                    source = os.path.join(extract_path, item)
                    destination = os.path.join(os.path.dirname(os.path.realpath(__file__)), item)
                    shutil.copy2(source, destination)

                # Clean up
                shutil.rmtree(extract_path)
                os.remove(download_path)

                messagebox.showinfo("Update Complete", "Script updated successfully. Restart the application.")
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
