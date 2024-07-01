class InputValidator:
    def __init__(self) -> None:
        self.data = None

    def ValidNumber(self):
        while True:
            try:
                self.data = int(input())
                break
            except:
                print("Valor inválido, por favor escoja otro")

    def ValidString(self):
        self.data = input()

    def get_data(self):
        return self.data