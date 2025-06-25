import tkinter as tk
from tkinter import messagebox, filedialog
import csv

class StockTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Stock Portfolio Tracker")
        self.root.geometry("600x550")
        self.root.configure(bg="#1e1e1e")

        self.stock_prices = {
            "AAPL": 180,
            "TSLA": 250,
            "GOOG": 140,
            "MSFT": 300,
            "AMZN": 190
        }

        self.portfolio = {}

        # Title
        tk.Label(root, text="Track Your Stock Portfolio", font=("Segoe UI", 18, "bold"), bg="#1e1e1e", fg="#ffffff").pack(pady=15)

        # Stock Entry
        tk.Label(root, text="Stock Symbol (AAPL, TSLA, etc):", bg="#1e1e1e", fg="#bbbbbb", font=("Segoe UI", 12)).pack()
        self.stock_entry = tk.Entry(root, font=("Segoe UI", 12), bg="#2a2a2a", fg="#ffffff", insertbackground="white")
        self.stock_entry.pack(pady=5)

        # Quantity Entry
        tk.Label(root, text="Quantity:", bg="#1e1e1e", fg="#bbbbbb", font=("Segoe UI", 12)).pack()
        self.qty_entry = tk.Entry(root, font=("Segoe UI", 12), bg="#2a2a2a", fg="#ffffff", insertbackground="white")
        self.qty_entry.pack(pady=5)

        # Buttons
        self.add_btn = tk.Button(root, text="Add to Portfolio", command=self.add_stock,
                                 bg="#007acc", fg="white", font=("Segoe UI", 11, "bold"))
        self.add_btn.pack(pady=10)

        self.calculate_btn = tk.Button(root, text="Calculate Total & Save", command=self.calculate_total,
                                       bg="#00a676", fg="white", font=("Segoe UI", 11, "bold"))
        self.calculate_btn.pack()

        # Output Display
        self.output = tk.Text(root, height=12, bg="#2a2a2a", fg="#00ffcc", font=("Consolas", 11),
                              relief="sunken", bd=2)
        self.output.pack(padx=20, pady=15, fill='both', expand=True)
        self.output.config(state='disabled')

        # Footer
        tk.Label(root, text="Made by Malaika 💻", font=("Segoe UI", 9), bg="#1e1e1e", fg="#888888").pack(pady=5)

    def add_stock(self):
        stock = self.stock_entry.get().upper()
        qty = self.qty_entry.get()

        if stock not in self.stock_prices:
            messagebox.showerror("Error", f"Stock '{stock}' not recognized.")
            return

        try:
            qty = int(qty)
            if qty <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Quantity must be a positive number.")
            return

        self.portfolio[stock] = self.portfolio.get(stock, 0) + qty
        messagebox.showinfo("Added", f"{qty} shares of {stock} added.")
        self.stock_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)

    def calculate_total(self):
        total = 0
        output_lines = []
        output_lines.append("Stock | Quantity × Price = Value")

        for stock, qty in self.portfolio.items():
            price = self.stock_prices[stock]
            value = price * qty
            total += value
            output_lines.append(f"{stock:<5} | {qty} × ${price} = ${value}")

        output_lines.append("\n" + "-"*35)
        output_lines.append(f"Total Investment: ${total}")

        # Display in text area
        self.output.config(state='normal')
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "\n".join(output_lines))
        self.output.config(state='disabled')

        # Ask to save
        save = messagebox.askyesno("Save Result", "Would you like to save this to a file?")
        if save:
            self.save_result(output_lines)

    def save_result(self, lines):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("CSV File", "*.csv")],
            title="Save Portfolio Summary"
        )
        if not file_path:
            return

        try:
            if file_path.endswith(".csv"):
                with open(file_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Stock", "Quantity", "Price", "Value"])
                    for stock, qty in self.portfolio.items():
                        price = self.stock_prices[stock]
                        value = qty * price
                        writer.writerow([stock, qty, price, value])
                    writer.writerow([])
                    writer.writerow(["Total Investment", "", "", total])
            else:
                with open(file_path, "w") as f:
                    for line in lines:
                        f.write(line + "\n")
            messagebox.showinfo("Saved", "Your portfolio has been saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file.\n{e}")

# Run the app
root = tk.Tk()
StockTrackerGUI(root)
root.mainloop()
