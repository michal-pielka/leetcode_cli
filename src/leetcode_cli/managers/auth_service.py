class AuthService:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def get_cookie(self):
        return self.config_manager.get_cookie()

    def get_csrf_token(self):
        return self.config_manager.extract_csrf_token()
