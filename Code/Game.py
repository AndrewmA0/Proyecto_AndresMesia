import Team
import Stadium

class Game:
    def __init__(self, number, home_team: Team.Team, away_team: Team.Team, date, group, stadium: Stadium.Stadium, id, ticket_list=None, used_ticket_list=None) -> None:
        self.number = number
        self.home_team = home_team
        self.away_team = away_team
        self.date = date
        self.group = group
        self.stadium = stadium
        self.id = id
        self.attendance = []
        self.attendance_vip = []
        if ticket_list is None:
            self.ticket_list = []
        else:
            self.ticket_list = ticket_list
        if used_ticket_list is None:
            self.used_ticket_list = []
        else:
            self.used_ticket_list = used_ticket_list

    def create_attendance(self, isVip=False):
        if isVip is False:
            attendance = self.stadium.get_capacity()
            attendance_list = self.attendance
        else:
            attendance = self.stadium.get_capacity_vip()
            attendance_list = self.attendance_vip
        i = 0
        j = 0
        while i < attendance:
            if j == 0:
                attendance_list.append([])
        
            attendance_list[-1].append(False)
            j += 1
            i += 1
            if j >= 10:
                j = 0
                    
    def set_attendance(self, attendance):
        self.attendance = attendance

    def set_attendance_vip(self, attendance):
        self.attendance_vip = attendance

    def check_seat(self, file: int, seat: int, isVip=False):
        if isVip is False:
            attendance_list = self.attendance
        else:
            attendance_list = self.attendance_vip

        if file >= len(attendance_list):
            return False
        
        if seat >= len(attendance_list[file]):
            return False

        return attendance_list[file][seat]
    
    def show_seats(self, isVip=False):
        fila = 1
        if isVip is False:
            attendance_list = self.attendance
        else:
            attendance_list = self.attendance_vip

        for row in attendance_list:
            seats = []
            for seat in row:
                if seat is False:
                    seats.append("Disponible")
                else:
                    seats.append("Ocupado")
            print(str(fila) + " " + str(seats))
            fila += 1

    def destructor(self):
        return {"number": self.number,
                "home": self.home_team.get_id(),
                "away": self.away_team.get_id(),
                "date": self.date,
                "group": self.group,
                "stadium_id": self.stadium.get_id(),
                "ticket_list": self.ticket_list,
                "used_ticket_list": self.used_ticket_list}
    
    def show(self):
        return "Juego número {}, entre {} y {}, en el estadio {}, fecha {}".format(self.number, self.away_team.get_name(), self.home_team.get_name(), self.stadium.get_name(), self.date)
    
    def add_ticket(self, game_id, cedula, isVip):
        self.ticket_list.append([game_id, cedula, isVip])

    def use_ticket(self, ticket):
        self.ticket_list.remove(ticket)
        self.used_ticket_list.append(ticket)

    def get_restaurant(self) -> Stadium.Stadium:
        return self.stadium
    
    def get_attendance(self):
        return self.attendance
    
    def get_attendance_vip(self):
        return self.attendance_vip
    
    def get_home_team(self):
        return self.home_team
    
    def get_away_team(self):
        return self.away_team
    
    def get_stadium(self):
        return self.stadium
    
    def get_date(self):
        return self.date
    
    def get_id(self):
        return self.id
    
    def get_ticket(self):
        return self.ticket_list
    
    def get_ticket_used(self):
        return self.used_ticket_list


