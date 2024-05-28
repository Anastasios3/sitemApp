import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

class SitemapGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sitemap Generator")
        self.geometry("600x500")

        self.path_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10, fill=tk.X)

        label = tk.Label(top_frame, text="Directory Path:")
        label.pack(side=tk.LEFT, padx=5)

        entry = tk.Entry(top_frame, textvariable=self.path_var, width=50)
        entry.pack(side=tk.LEFT, padx=5)

        browse_button = tk.Button(top_frame, text="Browse", command=self.browse_directory)
        browse_button.pack(side=tk.LEFT, padx=5)

        generate_button = tk.Button(top_frame, text="Generate Sitemap", command=self.generate_sitemap)
        generate_button.pack(side=tk.LEFT, padx=5)

        self.sitemap_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=20)
        self.sitemap_text.pack(pady=10, expand=True, fill=tk.BOTH)

        copy_button = tk.Button(self, text="Copy Sitemap", command=self.copy_sitemap)
        copy_button.pack(pady=10)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)

    def generate_sitemap(self):
        directory = self.path_var.get()
        if directory and os.path.isdir(directory):
            sitemap = self.get_sitemap(directory)
            self.sitemap_text.delete(1.0, tk.END)
            self.sitemap_text.insert(tk.END, sitemap)
        else:
            self.sitemap_text.delete(1.0, tk.END)
            self.sitemap_text.insert(tk.END, "Invalid directory path")

    def get_sitemap(self, directory):
        sitemap_lines = []
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith('.')]  # Exclude hidden directories
            level = root.replace(directory, '').count(os.sep)
            indent = ' ' * 4 * level
            sitemap_lines.append(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                sitemap_lines.append(f"{subindent}{f}")
        return "\n".join(sitemap_lines)

    def copy_sitemap(self):
        sitemap = self.sitemap_text.get(1.0, tk.END)
        self.clipboard_clear()
        self.clipboard_append(sitemap)
        messagebox.showinfo("Copied", "Sitemap copied to clipboard")

if __name__ == "__main__":
    app = SitemapGenerator()
    app.mainloop()
