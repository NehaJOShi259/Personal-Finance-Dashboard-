import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class FinanceDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Dashboard")
        self.root.geometry("950x700")
        self.data = pd.DataFrame(columns=["Item", "Category", "Amount"])
        self.categories = ["Housing", "Food", "Entertainment", "Transport", "Other"]
        self.create_ui()

    def create_ui(self):
        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Item").grid(row=0, column=0, padx=5)
        self.item_input = tk.Entry(input_frame)
        self.item_input.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Category").grid(row=0, column=2, padx=5)
        self.category_input = ttk.Combobox(input_frame, values=self.categories)
        self.category_input.set("Select Category")
        self.category_input.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Amount").grid(row=0, column=4, padx=5)
        self.amount_input = tk.Entry(input_frame)
        self.amount_input.grid(row=0, column=5, padx=5)

        add_btn = tk.Button(input_frame, text="Add Entry", command=self.add_entry)
        add_btn.grid(row=0, column=6, padx=5)

        # Table
        self.table = ttk.Treeview(self.root, columns=("Item", "Category", "Amount"), show="headings", height=10)
        self.table.heading("Item", text="Item")
        self.table.heading("Category", text="Category")
        self.table.heading("Amount", text="Amount")
        self.table.pack(pady=10, fill=tk.X)

        # Charts frame
        self.figure = Figure(figsize=(9,4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack()

        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        save_btn = tk.Button(btn_frame, text="Save CSV", command=self.save_csv)
        save_btn.grid(row=0, column=0, padx=5)
        load_btn = tk.Button(btn_frame, text="Load CSV", command=self.load_csv)
        load_btn.grid(row=0, column=1, padx=5)
        bar_btn = tk.Button(btn_frame, text="Bar Chart", command=self.plot_bar_chart)
        bar_btn.grid(row=0, column=2, padx=5)
        pie_btn = tk.Button(btn_frame, text="Pie Chart", command=self.plot_pie_chart)
        pie_btn.grid(row=0, column=3, padx=5)

        # Summary
        self.summary_label = tk.Label(self.root, text="Total Amount: 0")
        self.summary_label.pack(pady=5)

    def add_entry(self):
        item = self.item_input.get()
        category = self.category_input.get()
        if category not in self.categories:
            messagebox.showerror("Error", "Please select a valid category")
            return
        try:
            amount = float(self.amount_input.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return
        self.data = pd.concat([self.data, pd.DataFrame([{"Item": item, "Category": category, "Amount": amount}])], ignore_index=True)
        self.refresh_table()
        self.item_input.delete(0, tk.END)
        self.category_input.set("Select Category")
        self.amount_input.delete(0, tk.END)
        self.update_summary()

    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)
        for _, row in self.data.iterrows():
            self.table.insert("", tk.END, values=(row["Item"], row["Category"], row["Amount"]))

    def update_summary(self):
        total = self.data["Amount"].sum()
        self.summary_label.config(text=f"Total Amount: {total:.2f}")

    def save_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if path:
            self.data.to_csv(path, index=False)
            messagebox.showinfo("Saved", "Data saved successfully")

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
        if path:
            self.data = pd.read_csv(path)
            self.refresh_table()
            self.update_summary()
            messagebox.showinfo("Loaded", "Data loaded successfully")

    def plot_bar_chart(self):
        if self.data.empty:
            return
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        summary = self.data.groupby("Category")["Amount"].sum()
        summary.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title("Amount by Category")
        ax.set_ylabel("Amount")
        # Rotate and align labels to prevent overlap
        ax.set_xticklabels([s if len(s)<=15 else s[:12]+"..." for s in summary.index], rotation=45, ha='right')
        self.figure.tight_layout()
        self.canvas.draw()

    def plot_pie_chart(self):
        if self.data.empty:
            return
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        summary = self.data.groupby("Category")["Amount"].sum()
        summary.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
        ax.set_ylabel("")
        ax.set_title("Category Allocation")
        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceDashboard(root)
    root.mainloop()
