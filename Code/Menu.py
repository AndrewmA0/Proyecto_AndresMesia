import InputValidator
import DataManager
import Team
import Game
import Stadium
import User

class Menu:
    def __init__(self) -> None:
        self.data = DataManager.DataManager()
        self.data.load_data()
        self.answer = InputValidator.InputValidator()
        self.user: User.User = None
        self.game: Game.Game = None

    def first_menu(self):
        while True:
            print("""Bienvenido a la EuroCopa 2024
1. Realizar una búsqueda de juegos
2. Comprar una entrada
3. Asistir a un partido
4. Estadística
5. Salir""")
            self.answer.ValidNumber()
            num = self.answer.get_data()
            if num == 1:
                ## Funcion de busqueda aqui
                self.search_menu()
            elif num == 2:
                ## Funcion de comprar entrada aqui
                self.buying_ticket()
            elif num == 3:
                ## Funcion de asistir a partido aqui
                self.asistance_to_game()
            elif num == 4:
                ## Funcion de estadistica aquí
                self.statistics()
            elif num == 5:
                print("Gracias por elegir nuestros servicios, hasta pronto.")
                self.data.upload_data()
                break
            else:
                print("Opción no reconocida.")
    
    def search_menu(self):
        while True:
            print("""Bienvenido al sistema de busqueda, como desea buscar su partido:
1. Búsqueda por país
2. Búsqueda por estadio
3. Búsqueda por fecha""")
            self.answer.ValidNumber()
            num = self.answer.get_data()
            if num == 1:
                print("Ingrese el nombre (Inglés) o código del equipo que desee buscar")
                self.answer.ValidString()
                team = self.data.search_team_name(self.answer.get_data())
                if team is None:
                    print("Equipo no encontrado.")
                else:
                    self.data.search_by_team(team)
                break
            elif num == 2:
                print("Ingrese el nombre del estadio que desee buscar")
                self.answer.ValidString()
                stadium = self.data.search_stadium_name(self.answer.get_data())
                if stadium is None:
                    print("Estadio no encontrado.")
                else:
                    self.data.search_by_stadium(team)
                break
            elif num == 3:
                print("Ingrese el mes sobre que desea realizar su búsqueda (fórmato MM, mes de dos digitos)")
                self.answer.ValidString()
                month = self.answer.get_data()
                print("Ingrese el día (fórmato DD, diás de dos digitos)")
                day = self.answer.get_data()
                full_date = "2024-" + month + "-" + day
                self.data.search_by_date(full_date)
                break
            else:
                print("Opción no reconocida.")
    
    def buying_ticket(self):
        self.create_user()
        while True:
            self.data.show_all_games()
            print("Indique a cual juego quiere asistir (por su indice): ")
            self.answer.ValidNumber()
            self.game = self.data.get_game(self.answer.get_data())
            if self.game is None:
                print("Juego no encontrado.")
                continue
            else:
                break
        
        print("Juego seleccionado: {}".format(self.game.show()))

        while True:
            print("""¿Desea un asiento Vip, o uno normal?
1. Normal
2. Vip""")
            self.answer.ValidNumber()
            num = self.answer.get_data()
            if num == 1:
                isVip = False
                break
            elif num == 2:
                isVip = True
                break
            else:
                print("Valor no reconocido")
        
        while True:
            self.game.show_seats()
            print("Elija su fila")
            self.answer.ValidNumber()
            file = self.answer.get_data()
            print("Elija su asiento")
            self.answer.ValidNumber()
            seat = self.answer.get_data()
            Availability = self.game.check_seat(file - 1, seat - 1, isVip)
            if Availability is False:
                print("Asiento disponible")
                break
            else:
                print("Asiento no disponible")

        if self.user.vampire_discount() is True:
            print("Su cédula es un número vampiro! Tiene un descuento del 50%")
            discount = 50
        else:
            discount = 0

        if isVip == True:
            price = 75
        else:
            price = 35

        discount = (discount / price) * 100
        IVA = (16 / price) * 100
        full_price = price - discount + IVA

        print("Entrada para la fila {} y el asiento {}, Precio de la entrada: {}, Descuento: {}, IVA: {}, Completo: {}".format(file, seat, price, discount, IVA, full_price))

        while True:
            print("""¿Desea proceder con la compra?
1. Sí
2. No""")
            self.answer.ValidNumber()
            num = self.answer.get_data()
            if num == 1:
                print("¡Gracias por su compra!")
                self.user.add_ticket(self.game.get_id(), self.user.get_cedula(), isVip)
                self.game.add_ticket(self.game.get_id(), self.user.get_cedula(), isVip)
                break
            elif num == 2:
                break
            else:
                print("Opción no reconocida")

    def create_user(self):
        while True:
            print("""¿Desea crear un usuario nuevo o entrar a un usuario existente?
    1. Usuario nuevo
    2. Usuario existente""")
            self.answer.ValidNumber()
            num = self.answer.get_data()
            if num == 1:
                print("Primero, ingrese su cédula: ")
                self.answer.ValidNumber()
                cedula = self.answer.get_data()
                print("Ahora ingrese su nombre: ")
                self.answer.ValidString()
                nombre = self.answer.get_data()
                print("Ingrese su edad")
                self.answer.ValidNumber()
                edad = self.answer.get_data()

                self.user = User.User(nombre, cedula, edad)
                self.data.add_user(self.user)
                break
            elif num == 2:
                print("Por favor, ingrese su cédula:")
                self.answer.ValidNumber()
                cedula = self.answer.get_data()
                self.user = self.data.get_user(cedula)
                if self.user is not None:
                    break
                print("Usuario no encontrado")
            else:
                print("Opción no reconocida.")

    def asistance_to_game(self):
        self.create_user()

        while True:
            print("Estos son sus tickets disponibles (0 para salir):")
            self.data.get_games_from_ticket(self.user)

            self.answer.ValidNumber()
            num = self.answer.get_data()
            ticket = self.user.use_ticket(num - 1)
            if ticket is not None:
                print("Ha seleccionado correctamente su ticket")
                break
            if num == 0:
                return None
            else:
                print("Opción no válida")
        
        self.game = self.data.get_game_from_ticket(ticket)

        while True:
            print("""Se encuentra en el partido: {}, ¿Qué desea hacer?
1. Ir a un restaurante (Solo Vip)
2. Salir""".format(self.game.show()))
            self.answer.ValidNumber()
            num = self.answer.get_data()
            if num == 1:
                if ticket[-1] == True:
                    self.buying_restaurant()
                else:
                    print("Usted no es un usuario Vip")
            elif num == 2:
                print("Se ha ido")
                break
            else:
                print("Opción inválida")


    def buying_restaurant(self):
        while True:
            print("""¿Desea ir a un restaurante?
1. Sí
2. No""")
            self.answer.ValidNumber()
            num = self.answer.get_data()
            if num == 1:
                print("¿A que restaurante desea ir?")
                self.game.get_stadium().show_restaurants()
                self.answer.ValidNumber()
                num = self.answer.get_data()
                if self.game.get_stadium().check_valid_restaurant(num) is False:
                    print("Restaurante inválido")
                    continue
                else:
                    index_restaurant = num
                    print("""¿Que objetos desea ver?
1. Por nombre
2. Por rango de precio
3. Por tipo
4. Realizar una compra (Buscar por nombre)""")
                    self.answer.ValidNumber()
                    num = self.answer.get_data()
                    if num == 1:
                        self.answer.ValidString()
                        name = self.answer.get_data()
                        self.game.get_stadium().show_product_by_name(index_restaurant, name)
                    elif num == 2:
                        print("""¿Que rango desea ver?
1. Menos de 200
2. Menos de 500
3. Más de 500""")
                        self.answer.ValidNumber()
                        num = self.answer.get_data()
                        if num > 3 or num < 1:
                            print("Opción inválida")
                            continue
                        self.game.get_stadium().show_product_by_price(index_restaurant, num)
                    elif num == 3:
                        print("""¿Qué tipo de objetos quiere?
1. Plato
2. Paquete
3. Alcohólico
4. No alcohólico""")
                        self.answer.ValidNumber()
                        num = self.answer.get_data()
                        if num > 4 or num < 1:
                            print("Opción inválida")
                            continue
                        self.game.get_stadium().show_product_by_type(index_restaurant, num)
                    elif num == 4:
                        print("Elija su producto")
                        self.game.get_stadium().show_items(index_restaurant)
                        self.answer.ValidNumber()
                        num = self.answer.get_data()
                        item = self.game.get_stadium().buy_item(index_restaurant, num - 1, self.user.age)
                        if item is not None:
                            if self.user.perfect_discount() is True:
                                print("Felicidades, su cédula es un número perfecto, tiene un descuento del 15%")
                                Discount = 15
                            else:
                                Discount = 0
                            Discount = (Discount / item[1]) * 100
                            IVA = (16 / item[1]) * 100
                            full_price = item[1] - Discount + IVA
                            print("""Ha decidido comprar el objeto {}, costará {}, desea proseguir con la compra:
1. Sí
2. No""".format(item[0], full_price))
                            while True:
                                self.answer.ValidNumber()
                                num = self.answer.get_data()
                                if num == 1:
                                    print("Se ha realizado exitosamente la compra")
                                    print("Objeto: {}, Subtotal: {}, Descuento: {}, IVA: {}")
                                    self.user.add_item(item)
                                    break
                                elif num == 2:
                                    print("Se ha devuelto el objeto")
                                    self.game.get_stadium().return_item(index_restaurant, item)
                                    break
                                else:
                                    print("Opción inválida")
                    else:
                        print("Opción inválida")
                    

            elif num == 2:
                break
            else:
                print("Opción no válida")

    def statistics(self):
        while True:
            print("""¿Qué estadísticas desea ver?
1. Promedio de gasto de un cliente Vip
2. Tabla de asistencias a partido
3. Partido con mayor asistencias
4. Partido con mayores boletos vendidos
5. Top 3 productos más vendidos
6. Top 3 de clientes
7. Salir""")
            self.answer.ValidNumber()
            num = self.answer.get_data()
            if num == 1:
                print("El usuario Vip promedio ha gastado {}".format(self.data.medium_spending()))
            elif num == 2:
                asistance = self.data.asistance()
                for game in asistance:
                    print("El juego {} tuvo una asistencia de {} personas".format(game[0], game[1]))
            elif num == 3:
                max_asist = self.data.max_asistance()
                print("El juego con la mayor asistencia fue {} con {}".format(max_asist[0], max_asist[1]))
            elif num == 4:
                max_game = self.data.most_ticket_solds()
                print("El juego con más entradas vendidas fue {} con {}".format(max_game[0], max_game[1]))
            elif num == 5:
                most_sold = self.data.most_sold_products()
                print("Los 3 productos mas vendidos son {}, con {}, {}, con {}, y {}, con {}".format(most_sold[0][0], most_sold[0][1], most_sold[1][0], most_sold[1][1], most_sold[2][0], most_sold[2][1]))
            elif num == 6:
                most_sold = self.data.most_sold_client()
                print("Los 3 clientes que mas entradas compraron son {}, con {}, {}, con {}, y {}, con {}".format(most_sold[0][0], most_sold[0][1], most_sold[1][0], most_sold[1][1], most_sold[2][0], most_sold[2][1]))
            elif num == 7:
                break
            else:
                print("Opción inválida")
        