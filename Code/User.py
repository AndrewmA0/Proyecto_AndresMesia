import itertools as iter

class User:
    def __init__(self, name, cedula, age, ticket: list=None, bought_items: list=None) -> None:
        self.name = name
        self.cedula = cedula
        self.age = age
        if ticket is None:
            self.ticket = []
        else:
            self.ticket = ticket
        if bought_items is None:
            self.bought_items = []
        else:
            self.bought_items = bought_items

    def add_ticket(self, game_id, cedula, isVip):
        self.ticket.append([game_id, cedula, isVip])

    def add_item(self, item):
        self.bought_items.append(item)

    def destructor(self):
        return {"name": self.name,
                "cedula": self.cedula,
                "age": self.age,
                "ticket": self.ticket,
                "bought_items": self.bought_items}
    
    def vampire_discount(self):
        aux = str(self.cedula)
        if len(aux) % 2 != 0:
            return False
        permutations = iter.permutations(aux, len(aux))
        for permutation in permutations:
            first_half = permutation[:len(aux)//2]
            second_half = permutation[len(aux)//2:]
            first_half = "".join(first_half)
            second_half = "".join(second_half)

            if first_half[-1] == "0" and second_half[-1] == 0:
                continue

            if int(first_half) * int(second_half) == int(aux):
                return True
        return False
    
    def perfect_discount(self):
        divisors_list = []
        for i in range(1, self.cedula):
            if self.cedula % i == 0:
                divisors_list.append(i)
        
        return sum(divisors_list) == self.cedula
    
    def use_ticket(self, index):
        if index >= 0 and index < len(self.ticket):
            return self.ticket.pop(index)

    def get_cedula(self):
        return self.cedula
    
    def get_ticket(self):
        return self.ticket
    
    def get_bought_items(self):
        return self.bought_items
