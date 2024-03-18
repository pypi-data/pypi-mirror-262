import zuperscripts
import tkinter as tk

class BalanceChecker:
    def __init__(self, wallet_address, rpc_url):
        self.web3 = zuperscripts.TransactionERC(wallet_address, rpc_url)

    def get_balance(self):
        try:
            balance = self.web3.check_balance()
            return balance

        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def show_balance_gui(self):
        def update_balance():
            balance = self.get_balance()
            balance_label.config(text=str(balance))

        root = tk.Tk()
        root.title("Balance Checker")

        balance_label = tk.Label(root, text="Balance will be displayed here")
        balance_label.pack()

        check_balance_button = tk.Button(root, text="Check Balance", command=update_balance)
        check_balance_button.pack()

        root.mainloop()
