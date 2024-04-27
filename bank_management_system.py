"""
Python Final Exam Bank Management System.
Md Ahasanul Alam

ADMIN USER NAME = admin
ADMIN PASSWORD = 123

"""

from abc import ABC, abstractmethod

class Account(ABC):
    def __init__(self, name, email, address, account_type, account_number):
        self.__name = name
        self.__email = email
        self.__address = address
        self.__account_type = account_type
        self.__account_number = account_number
        self.__balance = 0
        self.__transaction_history = []
        self.__num_loans_taken = 0

    @property
    def name(self):
        return self.__name

    @abstractmethod
    def deposit(self, amount):
        self.__balance += amount
        self.__transaction_history.append(f'Deposited ${amount}')

    @abstractmethod
    def withdraw(self, amount):
        if self.__balance <= 0:
            print('\tYou are Bankrupt!! Transaction canceled.')
        elif amount > self.__balance:
            print('\tWithdrawal Amount Exceeded!! Transaction canceled.')
        else:
            self.__balance -= amount
            self.__transaction_history.append(f'Withdrew ${amount}')

    @abstractmethod
    def transfer(self, recipient_account_number, amount, bank):
        if recipient_account_number in bank.users:
            recipient = bank.users[recipient_account_number]
            if amount <= self.__balance:
                self.withdraw(amount)
                recipient.deposit(amount)
                self.__transaction_history.append(f'Transferred ${amount} to {recipient.name}')
            else:
                print('\tAlert!! Insufficient Funds for Transfer.')
        else:
            print('\tAlert!! Account does not Exist.')

    @abstractmethod
    def check_balance(self):
        return self.__balance

    @abstractmethod
    def get_transaction_history(self):
        return self.__transaction_history

    def __take_loan(self, bank):
        if bank.is_loan_enabled() and self.__num_loans_taken < 2:
            loan_amount = float(input('\tEnter Loan Amount : $'))
            if loan_amount > 0:
                self.deposit(loan_amount)
                self.__num_loans_taken += 1
                bank._Bank__total_loan_amount += loan_amount
                print(f'\tLoan of ${loan_amount} successfully taken.')
            else:
                print('\tAlert!! Invalid Loan Amount. Please enter a positive value.')
        else:
            print(f'\tAlert!! Please contact the admin to enable your loan permission! OR You have exceeded the limit of two times loan application!')


class User(Account):
    def __init__(self, name, email, address, account_type, account_number):
        super().__init__(name, email, address, account_type, account_number)

    def deposit(self, amount):
        self._Account__balance += amount  # Accessing private attribute using name mangling
        self._Account__transaction_history.append(f'Deposited ${amount}')

    def withdraw(self, amount):
        if bank.is_bankrupt_enabled():
            print(f'\tAlert!! {bank.name} is Bankrupt. This Transaction canceled.')
        elif amount > self._Account__balance:
            print('\tAlert!! Withdrawal amount exceeded. Transaction canceled.')
        else:
            self._Account__balance -= amount
            self._Account__transaction_history.append(f'Withdrew ${amount}')

    def transfer(self, recipient_account_number, amount, bank):
        if bank.is_bankrupt_enabled():
            print(f'\tAlert!! {bank.name} is Bankrupt. This Transaction canceled.')
        elif recipient_account_number in bank.users:
            recipient = bank.users[recipient_account_number]
            if amount <= self._Account__balance:
                self.withdraw(amount)
                recipient.deposit(amount)
                self._Account__transaction_history.append(f'Transferred ${amount} to {recipient.name}')
                print(f'\tTransferred Amount: ${amount} to {recipient.name} is successful!')
            else:
                print('\tAlert!! Insufficient funds for transfer.')
        else:
            print('\tAlert!! Account does not exist.')

    def check_balance(self):
        return self._Account__balance

    def get_transaction_history(self):
        return self._Account__transaction_history

    def take_loan(self, bank):
        if bank.is_bankrupt_enabled():
            print(f'\tAlert!! {bank.name} is Bankrupt. This Transaction canceled.')
        else:
            self._Account__take_loan(bank)


class Admin:
    def create_account(self, bank):
        name = input('\tEnter Name : ')
        email = input('\tEnter Email : ')
        address = input('\tEnter Address : ')
        account_type = input('\tEnter Account Type [Savings/Current] : ').capitalize()
        account_number = name.replace(' ','_') + '_00' + str(len(bank.users) + 1)  # Generating account number
        user = User(name, email, address, account_type, account_number)
        bank.users[account_number] = user
        print(f'\n\tAccount created successfully! Account Number : [ {account_number} ]')

    def delete_account(self, bank):
        account_number = input('\tEnter Account Number to Delete : ')
        if account_number in bank.users:
            del bank.users[account_number]
            print(f'\n\tAccount {account_number} Deleted Successfully.')
        else:
            print('\n\tAccount Not Found!!')

    def get_user_accounts(self, bank):
        print('****** User Accounts: ******')
        for account_number, user in bank.users.items():
            print(f'\tAccount Number: {account_number}, Name: {user.name}, Type: {user._Account__account_type}')

    def get_total_balance(self, bank):
        total_balance = sum(user._Account__balance for user in bank.users.values())
        print(f'\tTotal Bank Balance : ${total_balance}')
    
    def get_total_loan_amount(self, bank):
        print(f'\tTotal Bank Loan Amount : ${bank._Bank__total_loan_amount}')

    def toggle_loan_feature(self, bank):
        enabled = input('\tEnable [Y] or Disable [N] Loan Feature? [Y/N] : ').upper()
        if enabled == 'Y':
            bank.enable_loan()
            print('\tLoan Feature Enabled.')
        elif enabled == 'N':
            bank.disable_loan()
            print('\tLoan Feature Disabled.')
        else:
            print('\tInvalid input. Please enter "Y" or "N".')

    def toggle_bankrupt_feature(self, bank):
        enabled = input('\tEnable [Y] or Disable [N] Bankrupt feature? [Y/N] : ').upper()
        if enabled == 'Y':
            bank.enable_bankrupt()
            print('\tBankrupt Feature Enabled.')
        elif enabled == 'N':
            bank.disable_bankrupt()
            print('\tBankrupt Feature Disabled.')
        else:
            print('\tInvalid input. Please Enter "Y" or "N" ')


class Bank:
    def __init__(self, name):
        self.name = name
        self.users = {}
        self._Bank__total_loan_amount = 0
        self.__loan_enabled = True
        self.__bankrupt = False

    def enable_loan(self):
        self.__loan_enabled = True

    def disable_loan(self):
        self.__loan_enabled = False

    def is_loan_enabled(self):
        return self.__loan_enabled
    
    def enable_bankrupt(self):
        self.__bankrupt = True
    
    def disable_bankrupt(self):
        self.__bankrupt = False
    
    def is_bankrupt_enabled(self):
        return self.__bankrupt

    def admin_interface(self):
        admin = Admin()
        while True:
            print('\n****** : Admin Menu : ******')
            print('\t1 : Create Account')
            print('\t2 : Delete Account')
            print('\t3 : View User Accounts')
            print('\t4 : View Total Bank Balance')
            print('\t5 : View Total Loan Amount')
            print('\t6 : Toggle Loan Feature')
            print('\t7 : Toggle Bankrupt Feature')
            print('\t8 : Exit Menu')

            choice = input('\n\tEnter Your Choice [1-8] : ')
            try:
                choice = int(choice)
            except ValueError as error:
                print(f'\tAlert!! Invalid Input Number!! Please Enter the valid Integer Number Choice [1-8] !')
                continue

            if choice == 1:
                print('\n-------- : Create New User Account : --------')
                admin.create_account(self)

            elif choice == 2:
                admin.delete_account(self)

            elif choice == 3:
                admin.get_user_accounts(self)

            elif choice == 4:
                admin.get_total_balance(self)
            
            elif choice == 5:
                admin.get_total_loan_amount(self)

            elif choice == 6:
                admin.toggle_loan_feature(self)
            
            elif choice == 7:
                admin.toggle_bankrupt_feature(self)

            elif choice == 8:
                print('\n\t*** Exiting Admin Interface! ***')
                break
            else:
                print('\n\tInvalid Choice. Please try again the correct choice!')

    def user_interface(self):
        print('\n-------- : Create New User Account : --------')
        name = input('\tEnter Your Name : ')
        email = input('\tEnter Your Email : ')
        address = input('\tEnter Your Address : ')
        account_type = input('\tEnter Account Type [Savings/Current] : ').capitalize()
        account_number = name.replace(' ','_') + '_00' + str(len(self.users) + 1)  # Generating account number 
        user = User(name, email, address, account_type, account_number)
        self.users[account_number] = user
        print(f'\n\tAccount created successfully! Account Number: [ {account_number} ]')
        self.user_interface_actions(user)

    def user_interface_actions(self, user):
        while True:
            print('\n****** : User Menu : ******')
            print('\t1 : Deposit')
            print('\t2 : Withdraw')
            print('\t3 : Transfer')
            print('\t4 : Check Balance')
            print('\t5 : View Transaction History')
            print('\t6 : Take Loan')
            print('\t7 : Exit Menu')

            choice = input('\n\tEnter Your Choice [1-7] : ')
            try:
                choice = int(choice)
            except ValueError as error:
                print(f'\tAlert!! Invalid Input Number!! Please Enter the valid Integer Number Choice [1-7] !')
                continue

            if choice == 1:
                amount = float(input('\tEnter Deposit Amount : '))
                try:
                    user.deposit(amount)
                except ValueError as error:
                    print(f'\n\tAlert!! {error}\n')

            elif choice == 2:
                amount = float(input('\tEnter Withdrawal Amount : '))
                try:
                    user.withdraw(amount)
                except ValueError as error:
                    print(f'\n\tAlert!! {error}\n')

            elif choice == 3:
                recipient_account_number = input('\tEnter Recipient Account Number : ')
                amount = float(input('\tEnter Transfer Amount : '))
                try:
                    user.transfer(recipient_account_number, amount, self)
                except ValueError as error:
                    print(f'\n\tAlert!! {error}\n')

            elif choice == 4:
                print(f'\tCurrent Balance : ${user.check_balance()}')

            elif choice == 5:
                print('\n****** : Transaction History : ******')
                for transaction in user.get_transaction_history():
                    print(transaction)

            elif choice == 6:
                user.take_loan(self)

            elif choice == 7:
                print('\n\t*** Exiting User Interface! ***')
                break
            else:
                print('\n\tInvalid Choice!! Please try again correct choice! ')


# Creating a Bank
bank = Bank('Baper Bank')

while True:
    print(f'\n****** Welcome to the Banking Management System for {bank.name} ******')
    print('\t1 : Admin Login')
    print('\t2 : User Login')
    print('\t3 : Create New Account')
    print('\t4 : Exit System!')

    choice = input('\n\tEnter Your Choice [1-4] : ')
    try:
        choice = int(choice)
    except ValueError as error:
        print(f'\tAlert!! Invalid Input Number!! Please Enter the valid Integer Number Choice [1-4] !')
        continue

    if choice == 1:
        print('\n-------- : Admin Login : --------')
        admin_user = input('\tEnter Admin User Name : ')
        admin_password = input('\tEnter Admin Password : ')
        if admin_user == 'admin' and admin_password == '123':
            print(f'\n\t Welcome {admin_user}!! ')
            bank.admin_interface()
        else:
            print(f'\n\tAlert!! Invalid ADMIN User or Password!! Please try again with correct ADMIN user and password!\n')

    elif choice == 2:
        account_number = input('\tEnter your Account Number : ')
        if account_number in bank.users:
            bank.user_interface_actions(bank.users[account_number])
        else:
            print('\n\tInvalid Account Number. Please try again!')

    elif choice == 3:
        bank.user_interface()

    elif choice == 4:
        print(f'\n $$$$$$ Thank you for using the Banking Management System of {bank.name} ! $$$$$$')
        break
    else:
        print('\tInvalid Choice!! Please try again the correct choice! ')


