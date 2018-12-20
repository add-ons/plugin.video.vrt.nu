class MockKodiWrapper:

    def __init__(self):
        self.index = 0

    def get_setting(self, t):
        
        if self.index == 0:
            self.index += 1
            return '*****@gmail.com'
        else:
            self.index += 1
            return '***'

    def get_userdata_path(self):
        return "vrttest"

    def check_if_path_exists(self, path):
        return False
    
    def make_dir(self, path):
        return None

    def open_path(self, path):
        return False

    def check_inputstream_adaptive(self):
        return False

