import csv
import sqlite3
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# ==========================================
# CONSTANTE DE DESIGN (MODERN & PROFESSIONAL)
# ==========================================
C_BG_DARK = "#1E1E24"  # Fundal principal
C_BG_PANEL = "#2A2A35"  # Fundal panouri/containere
C_ACCENT = "#10B981"  # Verde (Butoane, Progres)
C_ACCENT_HOVER = "#059669"  # Verde închis la hover
C_TEXT_LIGHT = "#F3F4F6"  # Text principal
C_TEXT_MUTED = "#9CA3AF"  # Text secundar


class ModernScraperApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Data Extraction Professional Suite v1.0")
        self.geometry("750x550")
        self.configure(bg=C_BG_DARK)
        self.resizable(False, False)

        # Variabile de control
        self.is_running = False
        self.db_name = "fiverr_extracted_data.db"

        self.setup_styles()
        self.create_widgets()
        self.init_database()

    # ------------------------------------------
    # Helper: rulează o funcție UI pe thread-ul principal
    # ------------------------------------------
    def ui(self, func, *args, **kwargs):
        """Programează în siguranță o actualizare de interfață din alt thread."""
        self.after(0, lambda: func(*args, **kwargs))

    def setup_styles(self):
        """Configurează stilurile moderne pentru widget-urile TTK."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(".", background=C_BG_DARK, foreground=C_TEXT_LIGHT)

        self.style.configure(
            "TLabelframe",
            background=C_BG_PANEL,
            bordercolor=C_TEXT_MUTED,
            borderwidth=1,
        )
        self.style.configure(
            "TLabelframe.Label",
            background=C_BG_PANEL,
            foreground=C_ACCENT,
            font=("Segoe UI", 10, "bold"),
        )

        self.style.configure(
            "TButton",
            background=C_ACCENT,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            focusthickness=0,
            padding=8,
        )
        self.style.map(
            "TButton",
            background=[("active", C_ACCENT_HOVER), ("disabled", "#4B5563")],
        )

        self.style.configure(
            "Horizontal.TProgressbar",
            background=C_ACCENT,
            troughcolor=C_BG_DARK,
            borderwidth=0,
        )

        self.style.configure(
            "Treeview",
            background=C_BG_PANEL,
            fieldbackground=C_BG_PANEL,
            foreground=C_TEXT_LIGHT,
            rowheight=25,
            font=("Segoe UI", 9),
        )
        self.style.configure(
            "Treeview.Heading",
            background=C_BG_DARK,
            foreground=C_ACCENT,
            font=("Segoe UI", 9, "bold"),
            borderwidth=0,
        )
        self.style.map(
            "Treeview",
            background=[("selected", C_ACCENT)],
            foreground=[("selected", "white")],
        )

    def create_widgets(self):
        """Construiește interfața grafică."""
        # 1. HEADER
        header = tk.Label(
            self,
            text="📊 ENTERPRISE DATA EXTRACTOR",
            bg=C_BG_DARK,
            fg=C_TEXT_LIGHT,
            font=("Segoe UI", 16, "bold"),
        )
        header.pack(pady=15)

        # 2. PANOU DE CONFIGURARE
        config_frame = ttk.Labelframe(
            self, text=" Configuration & Target ", padding=15
        )
        config_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            config_frame,
            text="Target URL Directory:",
            bg=C_BG_PANEL,
            fg=C_TEXT_MUTED,
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.url_entry = tk.Entry(
            config_frame,
            bg=C_BG_DARK,
            fg=C_TEXT_LIGHT,
            insertbackground=C_TEXT_LIGHT,
            bd=1,
            relief="solid",
            font=("Segoe UI", 10),
        )
        self.url_entry.insert(0, "http://books.toscrape.com/catalogue/page-1.html")
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        tk.Label(
            config_frame,
            text="Pages to Scan:",
            bg=C_BG_PANEL,
            fg=C_TEXT_MUTED,
            font=("Segoe UI", 9, "bold"),
        ).grid(row=1, column=0, sticky="w", padx=5, pady=2)

        self.pages_spin = tk.Spinbox(
            config_frame,
            from_=1,
            to=50,
            width=5,
            bg=C_BG_DARK,
            fg=C_TEXT_LIGHT,
            insertbackground=C_TEXT_LIGHT,
            bd=1,
            relief="solid",
            font=("Segoe UI", 10),
        )
        self.pages_spin.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        config_frame.columnconfigure(1, weight=1)

        # 3. BUTOANE
        btn_frame = tk.Frame(self, bg=C_BG_DARK)
        btn_frame.pack(fill="x", padx=20, pady=10)

        self.btn_start = ttk.Button(
            btn_frame, text="▶ START SCRAPING", command=self.start_scraping_thread
        )
        self.btn_start.pack(side="left", padx=5)

        self.btn_stop = ttk.Button(
            btn_frame, text="🛑 STOP", command=self.stop_scraping, state="disabled"
        )
        self.btn_stop.pack(side="left", padx=5)

        self.btn_export = ttk.Button(
            btn_frame, text="📥 EXPORT CSV", command=self.export_to_csv
        )
        self.btn_export.pack(side="right", padx=5)

        # Status și progres
        progress_panel = tk.Frame(self, bg=C_BG_DARK)
        progress_panel.pack(fill="x", padx=20, pady=2)

        self.status_label = tk.Label(
            progress_panel,
            text="Status: Ready to extract.",
            bg=C_BG_DARK,
            fg=C_TEXT_MUTED,
            font=("Segoe UI", 9, "italic"),
        )
        self.status_label.pack(side="left")

        self.progress_bar = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            style="Horizontal.TProgressbar",
        )
        self.progress_bar.pack(fill="x", padx=20, pady=5)

        # 4. TABEL REZULTATE
        table_frame = tk.Frame(self, bg=C_BG_DARK)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        coloane = ("nume", "pret", "stoc")
        self.tree = ttk.Treeview(table_frame, columns=coloane, show="headings")
        self.tree.heading("nume", text="Item Name / Company")
        self.tree.heading("pret", text="Extracted Price")
        self.tree.heading("stoc", text="Availability Status")

        self.tree.column("nume", width=380, anchor="w")
        self.tree.column("pret", width=120, anchor="center")
        self.tree.column("stoc", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ==========================================
    # BAZĂ DE DATE (SQLITE)
    # ==========================================
    def init_database(self):
        """Creează structura SQLite."""
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS scraped_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT UNIQUE,
                    price TEXT,
                    availability TEXT
                )
                """
            )
            conn.commit()
        self.load_data_from_db()

    def load_data_from_db(self):
        """Încarcă datele salvate în tabel la deschiderea aplicației."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title, price, availability FROM scraped_items ORDER BY id DESC"
            )
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)

    # ==========================================
    # SCRAPING (MULTITHREADING)
    # ==========================================
    def start_scraping_thread(self):
        """Pornește thread-ul secundar pentru a menține GUI-ul fluid."""
        url = self.url_entry.get().strip()
        try:
            max_pages = int(self.pages_spin.get())
            if max_pages < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid number of pages.")
            return

        if not url.startswith(("http://", "https://")):
            messagebox.showerror("Error", "Please provide a valid HTTP/HTTPS URL.")
            return

        self.is_running = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.btn_export.config(state="disabled")

        threading.Thread(
            target=self.run_scraper, args=(url, max_pages), daemon=True
        ).start()

    def run_scraper(self, start_url, max_pages):
        """Logica de scraping executată în thread separat."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        target_url = start_url
        current_page = 1
        final_status = "Status: Extraction completed successfully!"

        self.ui(self.progress_bar.config, value=0, maximum=max_pages)

        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                while target_url and current_page <= max_pages and self.is_running:
                    self.ui(
                        self.status_label.config,
                        text=f"Status: Fetching page {current_page}...",
                    )

                    try:
                        response = requests.get(target_url, headers=headers, timeout=10)
                        response.raise_for_status()
                    except requests.RequestException as e:
                        final_status = f"Status: Request failed - {e}"
                        break

                    # response.content -> BeautifulSoup detectează corect encoding-ul (evită "Â£")
                    soup = BeautifulSoup(response.content, "html.parser")
                    items = soup.find_all("article", class_="product_pod")
                    if not items:
                        final_status = "Status: No items found on this page."
                        break

                    for item in items:
                        if not self.is_running:
                            break

                        title = item.h3.a["title"].strip()
                        price = item.find("p", class_="price_color").text.strip()
                        stock = item.find("p", class_="availability").text.strip()

                        cursor.execute(
                            """
                            INSERT OR IGNORE INTO scraped_items (title, price, availability)
                            VALUES (?, ?, ?)
                            """,
                            (title, price, stock),
                        )

                        if cursor.rowcount > 0:
                            self.ui(
                                self.tree.insert, "", 0, values=(title, price, stock)
                            )

                    conn.commit()

                    self.ui(self.progress_bar.config, value=current_page)

                    # Urmărește linkul "next" pentru paginare
                    next_link = soup.select_one("li.next > a")
                    target_url = (
                        urljoin(response.url, next_link["href"]) if next_link else None
                    )

                    current_page += 1
                    time.sleep(0.5)  # Delay fin pentru stabilitate

                if not self.is_running and final_status.startswith("Status: Extraction completed"):
                    final_status = "Status: Stopped by user."

        except Exception as e:
            final_status = f"Status: Unexpected error - {e}"

        # Resetare UI
        self.is_running = False
        self.ui(self.status_label.config, text=final_status)
        self.ui(self.btn_start.config, state="normal")
        self.ui(self.btn_stop.config, state="disabled")
        self.ui(self.btn_export.config, state="normal")

    def stop_scraping(self):
        """Oprește bucla de scraping."""
        self.is_running = False
        self.status_label.config(text="Status: Stopping execution...")

    # ==========================================
    # EXPORT CSV
    # ==========================================
    def export_to_csv(self):
        """Exportă baza de date într-un fișier CSV ales de utilizator."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Save Extracted Dataset",
        )
        if not file_path:
            return

        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT title, price, availability FROM scraped_items")
                rows = cursor.fetchall()

            with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(["Item Name / Title", "Price Rate", "Stock Availability"])
                writer.writerows(rows)

            messagebox.showinfo(
                "Export Success", f"Dataset exported safely to:\n{file_path}"
            )
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not export data: {e}")


if __name__ == "__main__":
    app = ModernScraperApp()
    app.mainloop()