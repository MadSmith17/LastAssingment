class UserManager:
    def __init__(self):
        self.user_list = []
        self.counter = 0

    def generate_id(self):
        self.counter += 1
        return self.counter
    
    def create_a_user(self, name, password, user_type):
        if not name or not password or not user_type:
            raise ValueError("Name, password, and user type cannot be empty.")

        if user_type not in ['student', 'teacher', 'admin']:
            raise ValueError("Invalid user type. User type should be 'student', 'teacher', or 'admin'.")

        new_user_id = self.generate_id()
        new_user = User(new_user_id, name, password, user_type)
        self.user_list.append(new_user)

    def find_users(self, ids):
        if not isinstance(ids, list):
            raise TypeError("IDs should be provided in a list.")

        users_found = []
        for user in self.user_list:
            if user.user_id in ids:
                users_found.append(user)
        
        return users_found

class User:
    def __init__(self, user_id: int, name: str, password: str, user_type: str):
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("User ID should be a positive integer.")

        if not name or not password or not user_type:
            raise ValueError("Name, password, and user type cannot be empty.")

        if user_type not in ['student', 'teacher', 'admin']:
            raise ValueError("Invalid user type. User type should be 'student', 'teacher', or 'admin'.")

        self.user_id = user_id
        self.name = name
        self.password = password
        self.type = user_type
    
    def __str__(self):
        return f"ID: {self.user_id}, name: {self.name}, type: {self.type}"