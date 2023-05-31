from environs import Env

class Config:
    def __init__(self):
        self.env = Env()
        self.env.read_env(recurse=True)

    def get(self, name):
        return self.env(name)
