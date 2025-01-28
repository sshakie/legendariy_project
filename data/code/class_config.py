class Config:
    def __init__(self):
        self.file = open('data/config')
        self.money = ''.join([i for i in self.file.readlines() if 'money' in i])

    def update(self):
        pass