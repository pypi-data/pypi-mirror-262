class copyright:

    def __init__(self, copy):
        self.copy=copy
    @property
    def cp(self):
        print(f"{self.copy}")
    def cp_name(self, name):
        print(f"[{self.copy} made by {name}]")
    def cp_date(self, date):
        print(f"[{self.copy} made in {date}]")
    def cp_date_name(self, date, name):
        print(f"[{self.copy} made in {date} by {name}]")
    @property
    def cp_number(self):
        import random
        number = random.randint(1000000, 9999999)
        print(f"[{self.copy} {number}]")

copy_right=copyright("Ⓒ")
