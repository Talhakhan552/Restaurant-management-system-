import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime



tables = {
    1: {"status": "available", "capacity": 4},
    2: {"status": "available", "capacity": 6},
    3: {"status": "occupied", "capacity": 2},
    4: {"status": "available", "capacity": 8},
}
reservations = {}
orders = {}
menu = {
    "Italian": [
        {"name": "Margherita Pizza", "price": 10, "time": 15, "category": "Main"},
        {"name": "Pasta Alfredo", "price": 12, "time": 20, "category": "Main"},
        {"name": "Tiramisu", "price": 7, "time": 5, "category": "Dessert"},
    ],
    "Chinese": [
        {"name": "Kung Pao Chicken", "price": 11, "time": 18, "category": "Main"},
        {"name": "Fried Rice", "price": 9, "time": 12, "category": "Main"},
        {"name": "Spring Rolls", "price": 6, "time": 8, "category": "Appetizer"},
    ],
    "Mexican": [
        {"name": "Tacos", "price": 10, "time": 12, "category": "Main"},
        {"name": "Guacamole", "price": 8, "time": 10, "category": "Appetizer"},
        {"name": "Churros", "price": 7, "time": 7, "category": "Dessert"},
    ]
}

class ReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management System")
        self.root.geometry("800x600")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", padding=6, font=("Arial", 10))
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), background="#3d3d3d", foreground="white")
        
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = ttk.Frame(self.main_frame, style="Header.TFrame")
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(header_frame, text="Restaurant Management System", style="Header.TLabel").pack(pady=10)
        
        reservation_frame = ttk.LabelFrame(self.main_frame, text="Table Reservation", padding=10)
        reservation_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(reservation_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(reservation_frame, width=25)
        self.name_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(reservation_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W)
        self.phone_entry = ttk.Entry(reservation_frame, width=25)
        self.phone_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(reservation_frame, text="Table:").grid(row=2, column=0, sticky=tk.W)
        self.table_combo = ttk.Combobox(reservation_frame, values=self.get_available_tables(), width=22)
        self.table_combo.grid(row=2, column=1, padx=5)
        
        ttk.Button(reservation_frame, text="Reserve", command=self.reserve_table).grid(row=3, columnspan=2, pady=5)
        ttk.Button(reservation_frame, text="Cancel Reservation", command=self.cancel_reservation).grid(row=4, columnspan=2)
        


        management_frame = ttk.Frame(self.main_frame)
        management_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(management_frame, text="View Tables", command=self.view_tables).pack(side=tk.LEFT, padx=5)
        ttk.Button(management_frame, text="View Menu", command=self.view_menu).pack(side=tk.LEFT, padx=5)
        ttk.Button(management_frame, text="View Orders", command=self.view_orders).pack(side=tk.LEFT, padx=5)
        ttk.Button(management_frame, text="Generate Bill", command=self.generate_bill).pack(side=tk.LEFT, padx=5)
        

        self.status_bar = ttk.Label(self.main_frame, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def get_available_tables(self):
        return [f"Table {num} ({info['capacity']} seats)" 
                for num, info in tables.items() if info['status'] == "available"]
    
    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.after(3000, lambda: self.status_bar.config(text="Ready"))
    
    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10
    
    def reserve_table(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        table_str = self.table_combo.get()
        
        if not name or not phone or not table_str:
            messagebox.showerror("Error", "All fields are required!")
            return
            
        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number (10 digits required)")
            return
            
        try:
            table_num = int(table_str.split()[1])
        except:
            messagebox.showerror("Error", "Please select a valid table from the dropdown")
            return
            
        reservations[table_num] = {
            "name": name,
            "phone": phone,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "orders": []
        }
        tables[table_num]["status"] = "occupied"
        self.table_combo["values"] = self.get_available_tables()
        self.update_status(f"Table {table_num} reserved for {name}")
        messagebox.showinfo("Success", f"Table {table_num} reserved successfully!")
        
    def cancel_reservation(self):
        table_num = simpledialog.askinteger("Cancel Reservation", "Enter table number:")
        if table_num and table_num in reservations:
            del reservations[table_num]
            tables[table_num]["status"] = "available"
            self.table_combo["values"] = self.get_available_tables()
            self.update_status(f"Reservation for Table {table_num} cancelled")
        else:
            messagebox.showerror("Error", "Invalid table number")
    
    def view_tables(self):
        table_window = tk.Toplevel(self.root)
        table_window.title("Table Status")
        table_window.geometry("400x300")
        
        tree = ttk.Treeview(table_window, columns=("Table", "Status", "Capacity"), show="headings")
        tree.heading("Table", text="Table")
        tree.heading("Status", text="Status")
        tree.heading("Capacity", text="Capacity")
        
        for num, info in tables.items():
            status = info["status"].capitalize()
            tree.insert("", tk.END, values=(num, status, info["capacity"]))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
    def view_menu(self):
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Menu")
        menu_window.geometry("600x500")
        
        notebook = ttk.Notebook(menu_window)
        
        for cuisine, items in menu.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=cuisine)
            
            tree = ttk.Treeview(frame, columns=("Dish", "Price", "Category"), show="headings")
            tree.heading("Dish", text="Dish")
            tree.heading("Price", text="Price ($)")
            tree.heading("Category", text="Category")
            
            for item in items:
                tree.insert("", tk.END, values=(item["name"], item["price"], item["category"]))
            
            tree.pack(fill=tk.BOTH, expand=True)
            ttk.Button(frame, text="Order", command=lambda: self.take_order(menu_window)).pack(pady=5)
        
        notebook.pack(fill=tk.BOTH, expand=True)
    
    
    
    
    def take_order(self, menu_window):
        table_num = simpledialog.askinteger("Order", "Enter table number:")
        if table_num not in reservations:
            messagebox.showerror("Error", "Invalid table number or table not reserved")
            return
            
        order_window = tk.Toplevel(menu_window)
        order_window.title("Place Order")
        
        self.order_vars = {}
        for cuisine, items in menu.items():
            frame = ttk.Frame(order_window)
            frame.pack(fill=tk.X, padx=5, pady=2)
            ttk.Label(frame, text=cuisine, font=("Arial", 10, "bold")).pack(anchor=tk.W)
            
            for item in items:
                row = ttk.Frame(frame)
                row.pack(fill=tk.X, padx=10)
                ttk.Label(row, text=f"{item['name']} (${item['price']})").pack(side=tk.LEFT)
                spin = ttk.Spinbox(row, from_=0, to=10, width=5)
                spin.pack(side=tk.RIGHT)
                self.order_vars[item["name"]] = spin
        
        ttk.Button(order_window, text="Confirm Order", 
                 command=lambda: self.process_order(table_num, order_window)).pack(pady=10)
        
        
        
        
        
        
        
        

    def process_order(self, table_num, window):
        order_items = []
        for dish, widget in self.order_vars.items():
            try:
                quantity = int(widget.get())
            except ValueError:
                quantity = 0  
            if quantity > 0:
                order_items.append((dish, quantity))
        
        if not order_items:
            messagebox.showerror("Error", "No items selected")
            return
            
        total_price = 0
        total_time = 0
        order_details = []
        
        for dish, qty in order_items:
            for cuisine in menu.values():
                for item in cuisine:
                    if item["name"] == dish:
                        total_price += item["price"] * qty
                        total_time = max(total_time, item["time"])
                        order_details.append(f"{qty}x {dish} (${item['price']} each)")
                        break
        
        order_id = len(orders) + 1
        orders[order_id] = {
            "table": table_num,
            "items": order_details,
            "total": total_price,
            "time": datetime.now().strftime("%H:%M"),
            "status": "Preparing"
        }
        reservations[table_num]["orders"].append(order_id)
        messagebox.showinfo("Success", f"Order placed!\nTotal: ${total_price}\nEst. Time: {total_time} mins")
        window.destroy()

    
    
    
    def view_orders(self):
        order_window = tk.Toplevel(self.root)
        order_window.title("Current Orders")
        
        tree = ttk.Treeview(order_window, columns=("ID", "Table", "Total", "Status"), show="headings")
        tree.heading("ID", text="Order ID")
        tree.heading("Table", text="Table")
        tree.heading("Total", text="Total ($)")
        tree.heading("Status", text="Status")
        
        for oid, details in orders.items():
            tree.insert("", tk.END, values=(oid, details["table"], details["total"], details["status"]))
        
        tree.pack(fill=tk.BOTH, expand=True)
    
    def generate_bill(self):
        table_num = simpledialog.askinteger("Generate Bill", "Enter table number:")
        if table_num not in reservations:
            messagebox.showerror("Error", "Invalid table number")
            return
            
        bill_window = tk.Toplevel(self.root)
        bill_window.title(f"Bill for Table {table_num}")
        
        total = 0
        text = f"Bill for Table {table_num}\n\n"
        text += f"Customer: {reservations[table_num]['name']}\n"
        text += f"Phone: {reservations[table_num]['phone']}\n\n"
        text += "Orders:\n"
        
        for oid in reservations[table_num]["orders"]:
            order = orders[oid]
            text += f"Order #{oid} ({order['time']}):\n"
            for item in order["items"]:
                text += f"- {item}\n"
            total += order["total"]
            text += "\n"
        
        text += f"\nTotal Amount: ${total}"
        
        ttk.Label(bill_window, text=text, padding=20).pack()
        ttk.Button(bill_window, text="Mark as Paid", 
                 command=lambda: self.close_table(table_num, bill_window)).pack(pady=10)
    
    def close_table(self, table_num, window):
        del reservations[table_num]
        tables[table_num]["status"] = "available"
        self.table_combo["values"] = self.get_available_tables()
        window.destroy()
        messagebox.showinfo("Success", "Table closed and bill paid")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReservationApp(root)
    root.mainloop()