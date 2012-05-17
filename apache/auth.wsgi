def check_password(environ, user, password):
    if user == 'username':
        if password == 'password':
            return True
        return False
    return None

