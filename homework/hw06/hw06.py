
passphrase = 'CC74EB'


def survey(p):
    """
    You do not need to understand this code.
    >>> survey(passphrase)
    '3d2eea56786a3d9e503a4c07dd667867ef3d92bfccd68b2aa0900ead'
    """
    import hashlib
    return hashlib.sha224(p.encode('utf-8')).hexdigest()


# Object Oriented Programming

class Fib():
    """A Fibonacci number.

    >>> start = Fib()
    >>> start
    Fib object, value 0
    >>> start.next()
    Fib object, value 1
    >>> start.next().next()
    Fib object, value 1
    >>> start.next().next().next()
    Fib object, value 2
    >>> start.next().next().next().next()
    Fib object, value 3
    >>> start.next().next().next().next().next()
    Fib object, value 5
    >>> start.next().next().next().next().next().next()
    Fib object, value 8
    >>> start.next().next().next().next().next().next() # Ensure start isn't changed
    Fib object, value 8
    """

    def __init__(self, value=0):
        self.value = value

    def next(self):
        "*** YOUR CODE HERE ***"
        if self.value == 0:
            fib = Fib(self.value)
            fib.prev = self.value
            fib.value = 1

        else:
            fib = Fib(self.value + self.prev)
            fib.prev = self.value
        return fib

    def __repr__(self):
        return "Fib object, value " + str(self.value)


class VendingMachine:
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Machine is out of stock.'
    >>> v.deposit(15)
    'Machine is out of stock. Here is your $15.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'You must deposit $10 more.'
    >>> v.deposit(7)
    'Current balance: $7'
    >>> v.vend()
    'You must deposit $3 more.'
    >>> v.deposit(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.deposit(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.deposit(15)
    'Machine is out of stock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.restock(3)
    'Current soda stock: 6'
    >>> w.deposit(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """
    "*** YOUR CODE HERE ***"

    def __init__(self, name, price, current_deposit=0):
        self.good_name = name  # the name of the good this machine is selling
        self.stock = 0  # initialize stock to be 0
        self.price = price  # how much money you need to pay for 1 good
        self.current_deposit = current_deposit  # how much money you have in the machine

    def vend(self):
        if self.stock == 0:
            return 'Machine is out of stock.'
        elif self.current_deposit < self.price:
            return 'You must deposit $' + str(self.price - self.current_deposit) + ' more.'
        elif self.current_deposit > self.price:
            self.stock -= 1
            change = self.current_deposit - self.price
            self.current_deposit = 0
            return 'Here is your ' + str(self.good_name) + ' and $' + str(change) + ' change.'
        else:
            self.stock -= 1
            self.current_deposit = 0
            return 'Here is your ' + str(self.good_name) + '.'

    def deposit(self, howmuch):
        if self.stock == 0:
            return 'Machine is out of stock. Here is your $' + str(howmuch) + '.'
        else:
            self.current_deposit = self.current_deposit + howmuch
            return 'Current balance: $' + str(self.current_deposit)

    def restock(self, amount):
        self.stock += amount
        return "Current " + str(self.good_name) + " stock: " + str(self.stock)
