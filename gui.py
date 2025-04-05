import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import pandas as pd

import annuity


def berechne_darlehen():
    betrag_str = entry_betrag.get().strip()
    laufzeit_str = entry_laufzeit.get().strip()
    zinssatz_str = entry_zinssatz.get().strip()
    sonderzahlung_str = entry_sonderzahlung.get().strip()

    if not betrag_str or not laufzeit_str or not zinssatz_str or not sonderzahlung_str:
        messagebox.showerror("Eingabefehler", "Bitte alle Felder ausfüllen.")
        return

    try:
        betrag = int(betrag_str)
        laufzeit = int(laufzeit_str)
        zinssatz = float(zinssatz_str)
        sonderzahlung = int(sonderzahlung_str)
    except ValueError:
        messagebox.showerror("Eingabefehler", "Bitte nur gültige Zahlen eingeben (z.B. Zinssatz: 3.5)")
        return

    if betrag <= 0 or laufzeit <= 0 or zinssatz <= 0:
        messagebox.showerror("Eingabefehler", "Darlehensbetrag, Laufzeit und Zinssatz müssen größer als 0 sein.")
        return
    if sonderzahlung < 0:
        messagebox.showerror("Eingabefehler", "Sonderzahlung darf nicht negativ sein.")
        return
    if zinssatz > 100:
        messagebox.showerror("Eingabefehler", "Zins darf nicht grösser als 100% sein.")
        return

    url = "http://127.0.0.1:5000/calc"
    params = {
        "principal": betrag,
        "duration": laufzeit,
        "nom_intr": zinssatz,
        "rdmp_intr": 3.0,
        "repay_amt": sonderzahlung,
        "period": combobox_period.get()
    }

    try:
        response = requests.get(url, params=params)
        filename = None
        if response.status_code == 200:
            # Versuche, den Dateinamen aus dem Content-Disposition-Header zu holen
            content_disposition = response.headers.get("content-disposition")
            if content_disposition and "filename=" in content_disposition:
                filename = content_disposition.split("filename=")[-1].strip('"')

        if filename is not None:
            with open(filename, "wb") as f:
                f.write(response.content)
            if checkbox_var.get():
                os.startfile(filename)
            else:
                df = pd.read_excel(filename)
                update_treeview(df)
                frame_excel.pack(fill="both", expand=True, padx=10, pady=10)
                root.geometry("600x600")
    except Exception as e:
        messagebox.showerror("Fehler bei der Berechnung", str(e))


def adjust_column_widths(df):
    for col in df.columns:
        max_len = max(df[col].apply(lambda x: len(str(x))))  # Get max length of column data
        max_len = max(max_len, len(col))  # Also consider the header length
        tree.column(col, width=max_len * 10)


def update_treeview(df):
    tree.delete(*tree.get_children())  # Clear existing content
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    # Setup columns and headings
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    # Add rows
    for row in df.itertuples(index=False):
        tree.insert("", "end", values=row)

    adjust_column_widths(df)


root = tk.Tk()
root.title("Annuitätendarlehen Rechner")
root.geometry("600x300")
root.resizable(True, True)

ttk.Label(root, text="Berechnung des Zins- und Tilgungsplan\n eines Annuitätendarlehens",
          font=("Arial", 14, "bold"), anchor="center", justify="center").pack(pady=20)


def add_input(label_text, default_value, row, col):
    ttk.Label(frame, text=label_text).grid(row=row, column=col, sticky="w", padx=5, pady=5)
    entry = ttk.Entry(frame)
    entry.insert(0, default_value)
    entry.grid(row=row + 1, column=col, padx=5)
    return entry


frame = ttk.Frame(root)
frame.pack(pady=10)

entry_betrag = add_input("Gesamtdarlehensbetrag (€):", 100000, 0, 0)
entry_zinssatz = add_input("Zinssatz (%):", 2, 0, 1)
entry_laufzeit = add_input("Laufzeit (Jahre):", 5, 0, 3)
entry_sonderzahlung = add_input("Sonderzahlung (€):", 0, 0, 4)

ttk.Label(root, text="Periodizität:").pack(pady=(10, 0))
combobox_period = ttk.Combobox(root, values=list(annuity.periods_per_year_map.keys()))
combobox_period.set("Monatlich")
combobox_period.pack()

ttk.Button(root, text="Berechnen", command=berechne_darlehen).pack(pady=10)
checkbox_var = tk.BooleanVar()
tk.Checkbutton(root, text="Excel öffnen", variable=checkbox_var).pack(pady=10)

frame_excel = ttk.Frame(root)

tree = ttk.Treeview(frame_excel)
vsb = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
tree.pack(fill="both", expand=True)
vsb.pack(side="right", fill="y")

root.mainloop()
