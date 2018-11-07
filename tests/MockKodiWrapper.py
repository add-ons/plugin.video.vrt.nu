class MockKodiWrapper:

    def __init__(self):
        self.index = 0

    def get_setting(self, t):
        
        if self.index == 0:
            self.index += 1
            return '-------@gmail.com'
        else:
            self.index += 1
            return '*****'
