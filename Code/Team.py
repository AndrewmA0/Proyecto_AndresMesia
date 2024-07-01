class Team:
    def __init__(self, code, name, group, id) -> None:
        self.id = id
        self.code = code
        self.name = name
        self.group = group

    def get_id(self):
        return self.id
    
    def destructor(self):
        return {"name": self.name,
                "code": self.code,
                "group": self.group}
    
    def get_name(self):
        return self.name
    
    def get_group(self):
        return self.group