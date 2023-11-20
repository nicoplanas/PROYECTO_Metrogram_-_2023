class User:
    def __init__(self, id, firstName, lastName, email, username, following):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.username = username
        self.following = following
        self.follow_requests = []
        self.strikes = []
        self.cont_interactions = 0
        self.cont_posts_taken_down = 0
        self.cont_offensive_comments = 0

    def show(self):
        return f"""ID: {self.id}
Nombre: {self.firstName}
Apellido: {self.lastName}
Email: {self.email}
Nombre de usuario: {self.username}
Seguidos: {len(self.following)}"""

class Student(User):
    def __init__(self, id, firstName, lastName, email, username, following, major):
        super().__init__(id, firstName, lastName, email, username, following)
        self.major = major

    def show(self):
        return f"""Nombre: {self.firstName}
Apellido: {self.lastName}
Email: {self.email}
Nombre de usuario: {self.username}
Carrera: {self.major}
Seguidos: {len(self.following)}"""

class Professor(User):
    def __init__(self, id, firstName, lastName, email, username, following, department):
        super().__init__(id, firstName, lastName, email, username,  following)
        self.department = department

    def show(self):
        return f"""Nombre: {self.firstName}
Apellido: {self.lastName}
Email: {self.email}
Nombre de usuario: {self.username}
Departamento: {self.department}
Seguidos: {len(self.following)}"""

class Admin(User):
    def __init__(self, id, firstName, lastName, email, username, following, password):
        super().__init__(id, firstName, lastName, email, username, following)
        self.password = password
    
    def show(self):
        return f"""Nombre: {self.firstName}
Apellido: {self.lastName}
Email: {self.email}
Nombre de usuario: {self.username}
Seguidos: {len(self.following)}"""