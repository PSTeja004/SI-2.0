import tkinter as tk
from tkinter import messagebox

class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        
        # Input fields
        self.label1 = tk.Label(self, text="Input 1")
        self.label1.grid(row=0, column=0)

        self.Input1 = tk.Entry(self)
        self.Input1.grid(row=0, column=1)

        self.label2 = tk.Label(self, text="Input 2")
        self.label2.grid(row=0, column=2)

        self.Input2 = tk.Entry(self)
        self.Input2.grid(row=0, column=3)

        # Buttons
        self.Addbtn = tk.Button(self, text="Add", command=self.add_numbers)
        self.Addbtn.grid(row=1, column=0, columnspan=2)


        self.Clrbtn = tk.Button(self, text="Clear", command=self.clear_inputs)
        self.Clrbtn.grid(row=1, column=2, columnspan=2)

        # Output field
        self.label = tk.Label(self, text="Output")
        self.label.grid(row=2, column=0)

        self.Output = tk.Entry(self)
        self.Output.grid(row=2, column=1, columnspan=3)

    def add_numbers(self):
        try:
            num1 = int(self.Input1.get())
            num2 = int(self.Input2.get())
            result = num1 + num2
            self.Output.delete(0, tk.END)
            self.Output.insert(0, str(result))
            self.result_window.update_result(result)
        except ValueError:
            messagebox.showwarning("Error", "Please enter valid numbers.")

    def clear_inputs(self):
        self.Input1.delete(0, tk.END)
        self.Input2.delete(0, tk.END)
        self.Output.delete(0, tk.END)
        self.result_window.update_result(0)

    def get_inputs(self):
        return [self.label1.cget("text"), self.label2.cget("text")]
    
    def get_outputs(self):
        return [self.label.cget("text")]



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Addition")

    main_window = MainWindow(root)
    main_window.pack(side=tk.TOP, padx=10, pady=10)

    root.mainloop()