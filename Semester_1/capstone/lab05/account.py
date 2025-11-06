class Account:
    __id: int = 0
    __balance:float = 0
    __annual_interest_rate: float = 0

    def __init__(self, id: int=0, balance: float=0, annual_interest_rate: float=0):
        self.__id = id
        self.__balance = balance
        self.__annual_interest_rate = annual_interest_rate

    def get_id(self):
        return self.__id

    def get_balance(self):
        return self.__balance

    def get_annual_interest_rate(self):
        return self.__annual_interest_rate

    def set_balance(self, balance: float):
        self.__balance = balance

    def set_id(self, new_id: int):
        self.__id = new_id

    def set_annual_interest_rate(self, new_annual_interest_rate: float):
        self.__annual_interest_rate = new_annual_interest_rate

    def get_monthly_interest_rate(self):
        return self.__annual_interest_rate / 12

    def get_monthly_interest(self):
        return self.__balance * self.get_monthly_interest_rate()

    def withdraw(self, amount: float):
        self.__balance -= amount

    def deposit(self, amount: float):
        self.__balance += amount


my_account = Account(id=1122, balance=20000, annual_interest_rate=0.045)
my_account.withdraw(amount=2500)
my_account.deposit(amount=3000)

print(f"Id: {my_account.get_id()}")
print(f"Current Balance: ${my_account.get_balance():.2f}")
print(f"Monthly Interest Number is {my_account.get_monthly_interest_rate() * 100:.3f}%")
print(f"Monthly Interest: ${my_account.get_monthly_interest():.2f}")

