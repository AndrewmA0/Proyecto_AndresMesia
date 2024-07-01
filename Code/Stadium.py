class Stadium:
    def __init__(self, name, city, capacity, restaurants, id) -> None:
        self.id = id
        self.name = name
        self.city = city
        self.capacity = capacity
        self.restaurants = restaurants

    def get_capacity(self):
        return self.capacity[0]
    
    def get_capacity_vip(self):
        return self.capacity[1]
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def destructor(self):
        return {"name": self.name,
                "city": self.city,
                "capacity": self.capacity,
                "restaurants": self.restaurants}
    
    def show_restaurants(self):
        i = 1
        for restaurant in self.restaurants:
            name = restaurant["name"]
            products = restaurant["products"]
            print(str(i) + " " + name)
            for product in products:
                print(product["name"] + " " + product["price"] + " " + product["adicional"])
            i += 1

    def show_items(self, index_restaurant):
        restaurant = self.restaurants[index_restaurant]
        i = 1
        for product in restaurant["products"]:
            print(str(i) + " " + product["name"] + " " + product["price"] + " " + product["adicional"])
            i += 1

    def show_product_by_type(self, index_restaurant, index_type):
        restaurant = self.restaurants[index_restaurant]
        if index_type == 1:
            type_item = "plate"
        elif index_type == 2:
            type_item = "package"
        elif index_type == 3:
            type_item = "alcoholic"
        elif index_type == 4:
            type_item = "non-alcoholic"

        for item in restaurant["products"]:
            if item["adicional"] == type_item:
                print(item["name"] + " " + item["price"] + " " + item["adicional"])

    def show_product_by_name(self, index_restaurant, name):
        restaurant = self.restaurants[index_restaurant]

        for item in restaurant["products"]:
            if item["name"] == name:
                print(item["name"] + " " + item["price"] + " " + item["adicional"])

    def show_product_by_price(self, index_restaurant, index_price_range):
        restaurant = self.restaurants[index_restaurant]
        if index_price_range == 1:
            price_range = 200
        elif index_price_range == 2:
            price_range = 500
        elif index_price_range == 3:
            price_range = 10000

        for item in restaurant["products"]:
            if float(item["price"]) < price_range:
                print(item["name"] + " " + item["price"] + " " + item["adicional"])

    def check_valid_restaurant(self, index):
        return index >= 0 and index < len(self.restaurants)
    
    def buy_item(self, index_restaurant, index_product, age):
        restaurant = self.restaurants[index_restaurant]
        if index_product < 0 or index_product >= len(restaurant["products"]):
            print("Producto inválido")
            return
        
        product = restaurant["products"][index_product]
        if product["adicional"] == "alcoholic" and age < 18:
            print("Este producto es alcohólico, y el usuario es menor de edad")
            return
        
        if product["stock"] < 1:
            print("No queda de este producto")
        product["stock"] -= 1
        return [product["name"], float(product["price"])]
    
    def return_item(self, index_restaurant, item):
        restaurant = self.restaurants[index_restaurant]
        for product in restaurant["products"]:
            if product["name"] == item[1]:
                product["stock"] += 1
                return
