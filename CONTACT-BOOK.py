import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

class ContactBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def view_contacts(self):
        return self.contacts

    def search_contact(self, query):
        return [c for c in self.contacts if query.lower() in c.name.lower() or query in c.phone]

    def update_contact(self, index, new_contact):
        if 0 <= index < len(self.contacts):
            self.contacts[index] = new_contact
            return True
        return False

    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            return self.contacts.pop(index)
        return None

class ContactBookGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("800x600")  # Enlarged Dimensions

        self.contact_book = ContactBook()

        self.create_widgets()

    def create_widgets(self):
        # Frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        btn_font = ("Arial", 14)

        tk.Button(button_frame, text="Add Contact", font=btn_font, command=self.add_contact).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Search Contact", font=btn_font, command=self.search_contact).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Update Contact", font=btn_font, command=self.update_contact).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="Delete Contact", font=btn_font, command=self.delete_contact).grid(row=0, column=3, padx=10)

        # Treeview for displaying contacts
        self.tree = ttk.Treeview(self.root, columns=("Name", "Phone", "Email", "Address"), show='headings', height=15)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Address", text="Address")

        self.tree.column("Name", width=150)
        self.tree.column("Phone", width=120)
        self.tree.column("Email", width=200)
        self.tree.column("Address", width=250)

        self.tree.pack(pady=10)

        self.refresh_tree()

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for contact in self.contact_book.view_contacts():
            self.tree.insert("", tk.END, values=(contact.name, contact.phone, contact.email, contact.address))

    def add_contact(self):
        name = simpledialog.askstring("Input", "Enter Name:")
        phone = simpledialog.askstring("Input", "Enter Phone Number:")
        email = simpledialog.askstring("Input", "Enter Email:")
        address = simpledialog.askstring("Input", "Enter Address:")

        if name and phone:
            contact = Contact(name, phone, email, address)
            self.contact_book.add_contact(contact)
            self.refresh_tree()
            messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
        else:
            messagebox.showwarning("Input Error", "Name and Phone are required.")

    def search_contact(self):
        query = simpledialog.askstring("Search", "Enter Name or Phone Number to Search:")
        if not query:
            return

        results = self.contact_book.search_contact(query)
        if results:
            self.tree.delete(*self.tree.get_children())
            for contact in results:
                self.tree.insert("", tk.END, values=(contact.name, contact.phone, contact.email, contact.address))
        else:
            messagebox.showinfo("No Results", "No matching contacts found.")

    def update_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a contact to update.")
            return

        index = self.tree.index(selected[0])
        current = self.contact_book.view_contacts()[index]

        name = simpledialog.askstring("Update", "Enter New Name:", initialvalue=current.name)
        phone = simpledialog.askstring("Update", "Enter New Phone:", initialvalue=current.phone)
        email = simpledialog.askstring("Update", "Enter New Email:", initialvalue=current.email)
        address = simpledialog.askstring("Update", "Enter New Address:", initialvalue=current.address)

        if name and phone:
            new_contact = Contact(name, phone, email, address)
            self.contact_book.update_contact(index, new_contact)
            self.refresh_tree()
            messagebox.showinfo("Updated", f"Contact updated successfully!")
        else:
            messagebox.showwarning("Input Error", "Name and Phone are required.")

    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a contact to delete.")
            return

        index = self.tree.index(selected[0])
        contact = self.contact_book.view_contacts()[index]

        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete '{contact.name}'?")
        if confirm:
            self.contact_book.delete_contact(index)
            self.refresh_tree()
            messagebox.showinfo("Deleted", "Contact deleted successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookGUI(root)
    root.mainloop()