import Stadium
import Team
import Game
import FileReader
import User
import os

class DataManager:
    def __init__(self) -> None:
        self.filepaths = ["Json Api/teams.txt", "Json Api/stadiums.txt", "Json Api/matches.txt", "Json Api/attendance.txt", "Json Api/attendance_vip.txt", "Json Api/Users.txt"]
        self.stadium_dict = {}
        self.team_dict = {}
        self.game_dict = {}
        self.user_dict = {}

    def load_data_local(self):
        try:
            file = FileReader.FileReader()
            info_to_parse = None
            #cargar equipos
            file.read_document_local(self.filepaths[0])
            info_to_parse = file.get_info() 
            for id in info_to_parse:
                self.team_dict[id] = Team.Team(info_to_parse[id]["code"], info_to_parse[id]["name"], info_to_parse[id]["group"], id)
            #cargar estadios
            file.read_document_local(self.filepaths[1])
            info_to_parse = file.get_info()
            for id in info_to_parse:
                self.stadium_dict[id] = Stadium.Stadium(info_to_parse[id]["name"], info_to_parse[id]["city"], info_to_parse[id]["capacity"], info_to_parse[id]["restaurants"], id)
            #cargar juegos
            file.read_document_local(self.filepaths[2])
            info_to_parse = file.get_info()
            for id in info_to_parse:
                self.game_dict[id] = Game.Game(info_to_parse[id]["number"], self.team_dict[info_to_parse[id]["home"]], self.team_dict[info_to_parse[id]["away"]], info_to_parse[id]["date"], info_to_parse[id]["group"], self.stadium_dict[info_to_parse[id]["stadium_id"]], id, info_to_parse[id]["ticket_list"], info_to_parse[id]["used_ticket_list"])
            #añadir asistencia normal
            file.read_document_local(self.filepaths[3])
            info_to_parse = file.get_info()
            for id in info_to_parse:
                self.game_dict[id].set_attendance(info_to_parse[id])
            #añadir asistencia vip
            file.read_document_local(self.filepaths[4])
            info_to_parse = file.get_info()
            for id in info_to_parse:
                self.game_dict[id].set_attendance_vip(info_to_parse[id])
            #añadir jugadores
            file.read_document_local(self.filepaths[5])
            info_to_parse = file.get_info()
            for id in info_to_parse:
                self.user_dict[int(id)] = User.User(info_to_parse[id]["name"], info_to_parse[id]["cedula"], info_to_parse[id]["age"], info_to_parse[id]["ticket"], info_to_parse[id]["bought_items"])
        except:
            self.load_data_online()

    def load_data_online(self):
        self.stadium_dict = {}
        self.team_dict = {}
        self.game_dict = {}
        info_to_parse = None
        file = FileReader.FileReader()
        # Creacion de equipos
        file.read_document_online("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json")
        info_to_parse = file.get_info() 
        for team in info_to_parse:
            self.team_dict[team["id"]] = Team.Team(team["code"], team["name"], team["group"], team["id"])
        # Creacion de estadios
        file.read_document_online("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json")
        info_to_parse = file.get_info()
        for stadium in info_to_parse:
            self.stadium_dict[stadium["id"]] = Stadium.Stadium(stadium["name"], stadium["city"], stadium["capacity"], stadium["restaurants"], stadium["id"])
        # Creacion de juegos
        file.read_document_online("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json")
        info_to_parse = file.get_info()
        for match in info_to_parse:
            self.game_dict[match["id"]] = Game.Game(match["number"], self.team_dict[match["home"]["id"]], self.team_dict[match["away"]["id"]], match["date"], match["group"], self.stadium_dict[match["stadium_id"]], match["id"])
            self.game_dict[match["id"]].create_attendance()
            self.game_dict[match["id"]].create_attendance(True)
        
    def load_data(self):
        for path in self.filepaths:
            if os.path.isfile(path) is False:
                self.load_data_online()
                return
        self.load_data_local()

    def upload_data(self):
        file = FileReader.FileReader()
        info_to_upload = {}
        #Subir equipos
        for id in self.team_dict:
            info_to_upload[id] = self.team_dict[id].destructor()
        file.set_info(info_to_upload)
        file.upload_document(self.filepaths[0])
        #Subir estadios
        info_to_upload = {}
        for id in self.stadium_dict:
            info_to_upload[id] = self.stadium_dict[id].destructor()
        file.set_info(info_to_upload)
        file.upload_document(self.filepaths[1])
        #Subir juegos
        info_to_upload = {}
        attendance = {}
        attendance_vip = {}
        for id in self.game_dict:
            info_to_upload[id] = self.game_dict[id].destructor()
            attendance[id] = self.game_dict[id].get_attendance()
            attendance_vip[id] = self.game_dict[id].get_attendance_vip()
        file.set_info(info_to_upload)
        file.upload_document(self.filepaths[2])
        file.set_info(attendance)
        file.upload_document(self.filepaths[3])
        file.set_info(attendance_vip)
        file.upload_document(self.filepaths[4])
        #Subir usuarios
        info_to_upload = {}
        for id in self.user_dict:
            info_to_upload[id] = self.user_dict[id].destructor()
        file.set_info(info_to_upload)
        file.upload_document(self.filepaths[5])

    def search_team_name(self, my_string):
        for team in self.team_dict.values():
            if my_string == team.get_name() or my_string == team.get_group():
                return team
            
    def search_by_team(self, team: Team.Team):
        list_of_games = []
        for game in self.game_dict.values():
            if game.get_home_team() == team or game.get_away_team() == team:
                list_of_games.append(game)
        return self.show_game(list_of_games)

    def search_stadium_name(self, my_string):
        for stadium in self.stadium_dict.values():
            if my_string == stadium.get_name():
                return stadium
            
    def search_by_stadium(self, stadium: Stadium.Stadium):
        list_of_games = []
        for game in self.game_dict.values():
            if stadium == game.get_stadium():
                list_of_games.append(game)
        return self.show_game(list_of_games)
    
    def search_by_date(self, my_string):
        list_of_games = []
        for game in self.game_dict.values():
            if my_string == game.get_date():
                list_of_games.append(game)
        return self.show_game(list_of_games)


    def show_game(self, game_list: list):
        for game in game_list:
            print(game.show())

    def show_all_games(self):
        i = 1
        for game in self.game_dict.values():
            print(str(i) + " " + game.show())
            i += 1

    def get_games_from_ticket(self, user: User.User):
        i = 1
        for ticket in user.get_ticket():
            print(str(i) + self.game_dict[ticket[0]].show())
            if ticket[-1] is False:
                print("Entrada regular")
            else:
                print("Entrada Vip")
            i += 1

    def get_game(self, index):
        i = 1
        for game in self.game_dict.values():
            if index == i:
                return game
            i += 1

    def get_game_from_ticket(self, ticket):
        self.game_dict[ticket[0]].use_ticket(ticket)
        return self.game_dict[ticket[0]]

    def get_user(self, cedula):
        return self.user_dict.get(cedula)

    def add_user(self, cedula, user):
        self.user_dict[cedula] = user

    def medium_spending(self):
        ticket_list = []
        spending = 0
        cedula_seen = []
        for game in self.game_dict.values():
            for ticket in game.get_ticket():
                if ticket[-1] is True:
                    ticket_list.append(ticket)
            for ticket in game.get_ticket_used():
                if ticket[-1] is True:
                    ticket_list.append(ticket)

        for ticket in ticket_list:
            if ticket[1] not in cedula_seen:
                cedula_seen.append(ticket[1])
            for item in self.user_dict[ticket[1]].get_bought_items():
                spending += item[1]
        if len(cedula_seen) == 0:
            return 0
        return (spending + (75 * len(ticket_list))) / len(cedula_seen)
    
    def asistance(self):
        game_asistance = []
        for game in self.game_dict.values():
            game_asistance.append([game.show(), len(game.get_ticket_used())])

        return game_asistance
    
    def max_asistance(self):
        game_asistance = self.asistance()
        max_asist = game_asistance[0]
        for game in game_asistance:
            if game[1] > max_asist[1]:
                max_asist = game
        return max_asist
    
    def most_ticket_solds(self):
        most_tickets = 0
        max_game = None
        for game in self.game_dict.values():
            ticket_solds = len(game.get_ticket()) + len(game.get_ticket_used())
            if ticket_solds > most_tickets:
                max_game = [game.show(), ticket_solds]
                most_tickets = ticket_solds
        return max_game
    
    def most_sold_products(self):
        seen_item = []
        for user in self.user_dict.values():
            seen = False
            for item in user.get_bought_items():
                for second_item in seen_item:
                    if second_item[0] == item[0]:
                        item[1] += 1
                        seen = True
                        break
                if seen is not True:
                    seen_item.append([item[0], 1])
        top_3 = [["Nada", 0], ["Nada", 0], ["Nada", 0]]
        for item in seen_item:
            if item[1] > top_3[0][1]:
                top_3[0], top_3[1], top_3[2] = item, top_3[0], top_3[1]
            elif item[1] > top_3[1][1]:
                top_3[1], top_3[2] = item, top_3[1]
            elif item[1] > top_3[2][1]:
                top_3[2] = item
        return top_3
                    
    def most_sold_client(self):
        ticket_list = []
        cedula_seen = {}
        for game in self.game_dict.values():
            for ticket in game.get_ticket():
                ticket_list.append(ticket)
            for ticket in game.get_ticket_used():
                ticket_list.append(ticket)

        for ticket in ticket_list:
            if cedula_seen.get(ticket[1]) is None:
                cedula_seen[ticket[1]] = 1
            else:
                cedula_seen[ticket[1]] += 1

        top_3 = [["Nada", 0], ["Nada", 0], ["Nada", 0]]

        for cedula in cedula_seen:
            if cedula_seen[cedula] > top_3[0][1]:
                top_3[0], top_3[1], top_3[2] = [cedula, cedula_seen[cedula]], top_3[0], top_3[1]
            elif cedula_seen[cedula] > top_3[1][1]:
                top_3[1], top_3[2] = [cedula, cedula_seen[cedula]], top_3[1]
            elif cedula_seen[cedula] > top_3[2][1]:
                top_3[2] = [cedula, cedula_seen[cedula]]
        return top_3
    
    def add_user(self, user: User.User):
        self.user_dict[user.get_cedula()] = user
