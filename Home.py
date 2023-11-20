#IMPORTAMOS LA LIBRERIA "REQUESTS" Y LAS CLASES

import json
import uuid
import requests
import time
from user import *
from multimedia import Multimedia

#CREAMOS LA CLASE PRINCIPAL DEL PROGRAMA

class Home:

    def __init__(self):
        self.current_sesion = []
        self.users = []
        self.multimedias = []
        self.deleted_users = []

    #MÉTODOS PARA LAS API

    def get_users(self, users):

        for unimetano in users:
            if unimetano["type"] == "student":
                student = Student(unimetano["id"], unimetano["firstName"], unimetano["lastName"], unimetano["email"], unimetano["username"], unimetano["following"], unimetano["major"])
                self.users.append(student)
            elif unimetano["type"] == "professor":
                professor = Professor(unimetano["id"], unimetano["firstName"], unimetano["lastName"], unimetano["email"], unimetano["username"], unimetano["following"], unimetano["department"])
                self.users.append(professor)
            elif unimetano["type"] == "admin":
                student = Admin(unimetano["id"], unimetano["firstName"], unimetano["lastName"], unimetano["email"], unimetano["username"], unimetano["following"], unimetano["password"])
                self.users.append(student)

    def get_multimedias(self ,posts):

        for post in posts:
            multimedia = Multimedia(post["publisher"], post["type"], post["multimedia"]["url"], post["caption"], post["date"], post["tags"], [], [], 0, 0, 0)
            self.multimedias.append(multimedia)

    def get_multi(self, posts):

        for post in posts:
            multimedia = Multimedia(post["publisher"], post["type"], post["multimedia"]["url"], post["caption"], post["date"], post["tags"], post["comments"], post["likes"], post["cont_likes"], post["cont_comments"], post["cont_interactions"])
            self.multimedias.append(multimedia)

    #MÓDULO DE GESTIÓN DE PERFIL

    def create_user(self):

        print("\n== CREACIÓN DE CUENTA ==\n")

        following = []

        id = uuid.uuid4()

        for user in self.users:
            while user.id == id:
                id = uuid.uuid4()

        firstName = input("Ingrese su nombre: ").lower()
        while not firstName.isalpha() or len(firstName) < 1:
            firstName = input("Ingrese un nombre válido: ").lower()

        lastName = input("Ingrese su apellido: ").lower()
        while not lastName.isalpha() or len(lastName) < 1:
            lastName = input("Ingrese un apellido válido: ").lower()

        email = input("Ingrese su correo electrónico: ").lower()
        email_id = "correo.unimet.edu.ve"
        cont_email = 0

        for x in range(len(email)):
            if email[x] == "@":
                cont_email += 1
            while cont_email > 1 or " " in email:
                email = input(f"Ingrese un correo válido: ")
            if cont_email == 1:
                email_user = slice(x + 1)
                email_type = slice(x + 1, 50)
                while email[email_type] != email_id:
                    email = email[email_user] + email_id
                break
            elif "@" not in email:
                email += "@correo.unimet.edu.ve"
        
        for metro_user in self.users:
            if metro_user.email.lower() == email.lower():
                print("\nESTE CORREO YA ESTA REGISTRADO!")
                return "FINALIZADO"

        username = input("Ingrese su nombre de usuario: ")
        for metro_user in self.users:
            while username.lower() == metro_user.username.lower() or " " in username or "@" in username or len(username) < 3:
                username = input("Ups! Ese nombre de usuario no está disponible, pruebe con otro: ")
        username = username

        type = input("""
Tipo de usuario:
                        
1. Estudiante.
2. Profesor.

>> """)
        
        while not type.isnumeric() or int(type) not in range(1,3) or len(type) != 1:
            type = input("""
Error! Ingrese un tipo de usuario válido:
                        
1. Estudiante.
2. Profesor.

>> """)

        if type == "1":
            major = input("Ingrese su carrera: ")
            user = Student(str(id), firstName.capitalize(), lastName.capitalize(), email, username, following, major)

        elif type == "2":
            department = input("Ingrese su departamento: ")
            user = Professor(str(id), firstName.capitalize(), lastName.capitalize(), email, username, following, department)

        self.users.append(user)
        self.current_sesion.append(user)

        self.save_changes()()

    def search_user(self):
        
        filter = input("""
ELIJA UN FILTRO DE BÚSQUEDA:
            
1. Username.
2. Carrera o departamento.

[PRESIONE "0" PARA SALIR]

>> """)
                       
        while not filter.isnumeric() or int(filter) not in range(0, 3) or len(filter) != 1:
                filter = input("""
ERROR! ELIJA UN FILTRO DE BÚSQUEDA VÁLIDO:
            
1. Username.
2. Carrera o departamento.

[PRESIONE "0" PARA SALIR]

>> """)

        if filter == "1":

            aux = True

            while aux:

                exact_match = 0
                total_matches = 0
                matches = []

                search = input("\nIngrese el nombre de usuario del perfil que busca\n\n[PRESIONE '0' PARA SALIR]\n\n>> ")

                if search == "0":
                    aux = False

                elif " " in search or len(search) == 0:
                    print("\nNO SE ENCONTRÓ NINGÚN PERFIL CON ESE NOMBRE DE USUARIO!\n========================================================")

                else:
                    for user in self.users:
                        if user.username.lower() == search.lower():
                            print(f"\n@{user.username} - Following {len(user.following)}")
                            self.access_others(user)
                            exact_match += 1
                        else:
                            x = slice(0, len(search))
                            if search.lower() == user.username[x].lower():
                                matches.append(user)
                                total_matches += 1
                            
                    if total_matches > 0:

                        print("\nRESULTADOS DE BÚSQUEDA...\n")

                        for idx, match in enumerate(matches):
                            print(f"{idx + 1}. @{match.username.lower()} | Following {len(match.following)}")

                        select = input("\nIngrese el indice del perfil al que desea ingresar: ")

                        while not select.isnumeric() or int(select) not in range(1,len(matches) + 1):   
                            select = input("Error! Ingrese un indice de perfil válido al que ingresar: ")
        
                        for idx, match in enumerate(matches):
                            if select == str(idx + 1):
                                self.access_others(match)
                                total_matches += 1

                    if exact_match == 0 and total_matches == 0: 
                        print("\nNO SE ENCONTRÓ NINGÚN PERFIL CON ESE NOMBRE DE USUARIO!\n========================================================")

        elif filter == "2":

            aux = True

            while aux:

                user_index = 0
                total_matches = 0
                exact_matches = []
                matches = []

                search = input("\nIngrese la carrera o el departamento del usuario\n\n[PRESIONE '0' PARA SALIR]\n\n>> ")

                if search == "0":
                    aux = False

                else:
                    for user in self.users:
                        if isinstance(user, Student):
                            if user.major.lower() == search.lower():
                                user_index += 1
                                exact_matches.append(user)
                            else:
                                x = slice(0, len(search))
                                if search.lower() == user.major[x].lower():
                                    matches.append(user)
                                    total_matches += 1
                        elif isinstance(user, Professor):
                            if user.department.lower() == search.lower():
                                user_index += 1
                                exact_matches.append(user)
                            else:
                                x = slice(0, len(search))
                                if search.lower() == user.department[x].lower():
                                    matches.append(user)
                                    total_matches += 1

                    if len(exact_matches) > 0:

                        print(f"\n== USUARIOS DE '{search.upper()}' ==\n")

                        for idx, exact_match in enumerate(exact_matches):
                            if isinstance(exact_match, Student):
                                print(f"{idx + 1}. Carrera: {exact_match.major} | @{exact_match.username.lower()}")
                            elif isinstance(exact_match, Professor):
                                print(f"{idx + 1}. Departamento: {exact_match.department} | @{exact_match.username.lower()}")

                        select = input("\nIngrese el indice del perfil al que desea ingresar\n\n[PRESIONE '0' PARA SALIR]\n\n>> ")

                        while not select.isnumeric() or int(select) not in range(0,len(exact_matches) + 1):   
                            select = input("Error! Ingrese un indice de perfil válido al que ingresar\n\n[PRESIONE '0' PARA SALIR]\n\n>> ")

                        if select == "0":
                            return "FINALIZADO"
        
                        for idx, exact_match in enumerate(exact_matches):
                            if select == str(idx + 1):
                                self.access_others(exact_match)

                    elif total_matches > 0:

                            print("\nRESULTADOS DE BÚSQUEDA...\n")

                            for idx, match in enumerate(matches):
                                if isinstance(match, Student):
                                    print(f"{idx + 1}. Carrera: {match.major} | @{match.username.lower()}")
                                elif isinstance(match, Professor):
                                    print(f"{idx + 1}. Departamento: {match.department} | @{match.username.lower()}")

                            select = input("\nIngrese el indice del perfil al que desea ingresar\n\n[PRESIONE '0' PARA SALIR]\n\n>> ")

                            while not select.isnumeric() or int(select) not in range(0,len(matches) + 1):   
                                select = input("Error! Ingrese un indice de perfil válido al que ingresar\n\n[PRESIONE '0' PARA SALIR]\n\n>> ")

                            if select == "0":
                                return "FINALIZADO"
            
                            for idx, match in enumerate(matches):
                                if select == str(idx + 1):
                                    self.access_others(match)
                                    total_matches += 1

                if user_index == 0 and total_matches == 0:
                    print("\nNO SE ENCONTRÓ NINGÚN PERFIL DE ESTA CARRERA/DEPARTAMENTO!\n========================================================")

        elif filter == "0":
            return "FINALIZADO"

        self.save_changes()

    def edit_user(self):

        for user in self.users:
            if user.username == self.current_sesion[0].username:
                option = input("""
ELIJA QUE DESEA MODIFICAR:

1. Nombre.
2. Apellido.
3. Correo electronico.
4. Nombre de usuario.
5. Carrera o departamento.

[PRESIONE "0" PARA SALIR]

>> """)
                
                while not option.isnumeric() or int(option) not in range(0,6) or len(option) != 1:
                    option = input("""
ERROR! ELIJA QUE DESEA MODIFICAR:

1. Nombre.
2. Apellido.
3. Correo electronico.
4. Nombre de usuario.
5. Carrera o departamento.

[PRESIONE "0" PARA SALIR]

>> """)

                if option == "1":
                    print(f"\nNombre actual: {user.firstName}")
                    firstName = input("Ingrese su nombre: ").lower()
                    while not firstName.isalpha() or len(firstName) < 1:
                        firstName = input("Ingrese un nombre válido: ").lower()
                    user.firstName = firstName

                elif option == "2":
                    print(f"\nApellido actual: {user.lastName}")
                    lastName = input("Ingrese su apellido: ").lower()
                    while not lastName.isalpha() or len(lastName) < 1:
                        lastName = input("Ingrese un apellido válido: ").lower()
                    user.lastName = lastName

                elif option == "3":
                    print(f"\nCorreo actual: {user.email}")
                    email = input("Ingrese su correo electrónico: ").lower()
                    email_id = "correo.unimet.edu.ve"
                    cont_email = 0

                    for metro_user in self.users:
                        if metro_user.email.lower() == email.lower() and metro_user.username.lower() != user.username.lower():
                            print("\nESTE CORREO YA ESTA REGISTRADO!")
                            return "FINALIZADO"

                    for x in range(len(email)):
                        if email[x] == "@":
                            cont_email += 1
                        if cont_email > 1 or " " in email:
                            user.email = "No tienes correo."
                            print("\nESTE CORREO ES INVÁLIDO!")
                            return "FINALIZADO"
                        if cont_email == 1:
                            if email[x] == "@":
                                email_user = slice(x + 1)
                                email_type = slice(x + 1, 50)
                            if email[email_type] != email_id:
                                user.email = email[email_user] + email_id
                        elif "@" not in email:
                            user.email = email + "@correo.unimet.edu.ve"

                    for metro_user in self.users:
                        if metro_user.email.lower() == user.email.lower() and metro_user.username.lower() != user.username.lower():
                            user.email = "No tienes correo."
                            print("\nESTE CORREO YA ESTA REGISTRADO!")

                elif option == "4":
                    print(f"\nNombre de usuario actual: {user.username}")
                    username = input("Ingrese su nuevo nombre de usuario: ")
                    if username.lower() == self.current_sesion[0].username.lower():
                        return "FINALIZADO"
                    for metro_user in self.users:
                        while username.lower() == metro_user.username.lower() or " " in username.lower():
                            username = input("Ups! Ese nombre de usuario no está disponible, pruebe con otro: ")
                        else:
                            user.username = username

                elif option == "5":
                    if isinstance(user, Student):
                        print(f"\nCarrera actual: {user.major}")
                        major = input("Ingrese la nueva carrera: ").capitalize()
                        user.major = major
                    elif isinstance(user, Professor):
                        print(f"\nDepartamento actual: {user.department}")
                        department = input("Ingrese el nuevo departamento: ").capitalize()
                        user.department = department

                elif option == "0":
                    return "FINALIZADO"

        self.save_changes()

    def delete_data(self):

        verification = input("""
UNA VEZ SUS DATOS SEAN ELIMINADOS NO PODRAN SER RECUPERADOS! ESTÁ SEGURO DE QUE DESEA CONTINUAR?
        
1. Continuar.
2. Cancelar.

>> """)
        
        while not verification.isnumeric() or int(verification) not in range(1,3) or len(verification) != 1:
            verification = input("""
ERROR! ESTÁ SEGURO DE QUE DESEA CONTINUAR?

1. Continuar.
2. Cancelar.

>> """)

        if verification == "1":
            for user in self.users:
                if user.username == self.current_sesion[0].username:
                    self.users.remove(user)
                    print(f"\nLos datos de '{user.firstName.upper()} {user.lastName.upper()}' han sido eliminados con exito.")
        
        elif verification == "2":
            return "FINALIZADO"

        self.save_changes()

    def access_others(self, user):

        index = 1
        user_posts = {}
        username = ""

        if user == self.current_sesion[0]:
            access = "1"

        elif user.id in self.current_sesion[0].following:
            access = "1"

        elif isinstance(self.current_sesion[0], Admin):
            access = input("""
==================

Escoja una opción:

1. Ingresar al perfil.
2. Seguir a este usuario.
3. Eliminar a este usuario.

[PRESIONE "0" PARA SALIR]

>> """)

            #VALIDAMOS EL INPUT DE LA INTERACCIÓN PARA LOS USARIOS ADMINISTRADORES
            while not access.isnumeric() or int(access) not in range(0,4) or len(access) != 1:
                access = input("""
================================

Error! Escoja una opción válida:

1. Ingresar al perfil.
2. Seguir a este usuario.
3. Eliminar a este usuario.

[PRESIONE "0" PARA SALIR]

>> """)

        else:
            access = input("""
==================

Escoja una opción:

1. Ingresar al perfil.
2. Seguir a este usuario.

[PRESIONE "0" PARA SALIR]

>> """)

            #VALIDAMOS EL INPUT DE LA INTERACCIÓN PARA LOS USARIOS ESTUDIANTES Y PROFESORES
            while not access.isnumeric() or int(access) not in range(0,3) or len(access) != 1:
                access = input("""
================================

Error! Escoja una opción válida:

1. Ingresar al perfil.
2. Seguir a este usuario.

[PRESIONE "0" PARA SALIR]

>> """)

        if access == "1":
            if user.id in self.current_sesion[0].following or user.id == self.current_sesion[0].id or isinstance(self.current_sesion[0], Admin):
                username = user.username.lower()
                id = user.id
                print(f"\n{user.firstName} {user.lastName}\n@{user.username}\nPUBLICACIONES:")
                for user_post in self.multimedias:
                    if user_post.publisher == id:
                        user_posts[index] = user_post
                        print(f"\n==== POST #{index} ====\n{user_post.show_attr(username)}")
                        index += 1

                interact = input("\n=====================\n\nPRESIONE '0' PARA SALIR!\nIngrese el indice del post con el que desea interactuar\n\n>> ")

                #VALIDAMOS EL INPUT DE INTERACTUAR
                while not interact.isnumeric() or int(interact) not in range(0, len(user_posts) + 1):
                    interact = input("  =====================\n\nPRESIONE '0' PARA SALIR!\nError! Ingrese un indice válido\n\n>> ")

                #CONDICIÓN PARA FINALIZAR LA ACCIÓN
                if interact == "0":
                    return "FINALIZADO"
                
                for aux_index, post in user_posts.items():
                    if int(interact) == aux_index:
                        print(post.show_attr(username))
                        for media in self.multimedias:
                            if media == post:
                                if isinstance(self.current_sesion[0], Admin) or user == self.current_sesion[0]:
                                    interaction = input("\n=====================\n\n1. Dar like.\n2. Comentar\n3. Ver likes.\n4. Gestionar comentarios.\n5. Eliminar post.\n\n>> ")
                                    #VALIDAMOS EL INPUT DE LA INTERACCIÓN PARA LOS USARIOS ADMINISTRADORES
                                    while not interaction.isnumeric() or int(interaction) not in range(1,6) or len(interaction) != 1:
                                        interaction = input("\n=====================\n\nError! Selecciones una de las opciones:\n\n1. Dar like.\n2. Comentar\n3. Ver likes.\n4. Ver comentarios.\n5. Eliminar post.\n\n>> ")
                                else:
                                    interaction = input("\n=====================\n\n1. Dar like.\n2. Comentar\n3. Ver likes.\n4. Ver comentarios.\n\n>> ")
                                    #VALIDAMOS EL INPUT DE LA INTERACCIÓN PARA LOS USARIOS ESTUDIANTES Y PROFESORES
                                    while not interaction.isnumeric() or int(interaction) not in range(1,5) or len(interaction) != 1:
                                        interaction = input("\n=======================\n\nError! Selecciones una de las opciones:\n\n1. Dar like.\n2. Comentar\n3. Ver likes.\n4. Ver comentarios.\n\n>> ")
                                if interaction == "1":
                                    media.give_like(self.current_sesion[0], user)
                                    self.save_changes()
                                elif interaction == "2":
                                    comment = input("\nAgregue un comentario: ")
                                    seconds = time.time()
                                    date = time.ctime(seconds)
                                    media.add_comment(self.current_sesion[0], user, comment, date)
                                    self.save_changes()
                                elif interaction == "3":
                                    self.view_likes(media)
                                    self.save_changes()
                                elif interaction == "4":
                                    if isinstance(self.current_sesion[0], Admin) or user == self.current_sesion[0]:
                                        self.delete_offensive_comments(media)
                                        self.save_changes()
                                    else:
                                        self.view_comments(media)
                                        self.save_changes()
                                elif interaction == "5":
                                    self.delete_post(media, user)
                                    self.save_changes()

            else:
                follow = input("""\nUsted no sigue a este usuario, por lo tanto no puede acceder a su pefil:
                
1. Seguir.
2. Salir

>> """)

                while not follow.isnumeric() or int(follow) not in range(1,3) or len(follow) != 1:
                    follow = input("""Usted no sigue a este usuario, por lo tanto no puede acceder a su pefil:
                
1. Seguir.
2. Salir

>> """)

                if follow == "1":
                    self.follow_user(user)
                    self.save_changes()

                elif follow == "2":
                    return "FINALIZADO"

        elif access == "2":
            self.follow_user(user)
            self.save_changes()
        
        elif access == "3":
            self.delete_user(user)

        elif access == "0":
            return "FINALIZADO"

    #MÓDULO DE GESTIÓN DE MULTIMEDIA

    def upload_post(self):

        publisher = self.current_sesion[0].id
        type = input("""
ESCOJA EL TIPO DE MULTIMEDIA:

1. Foto.
2. Video.

>> """)
                     
        #VALIDAMOS EL INPUT DEL TIPO
        while not type.isnumeric() or int(type) not in range(1,3):
            type = input("""
ERROR! ESCOJA UN TIPO DE MULTIMEDIA VÁLIDO:

1. Foto.
2. Video.

>> """)

        if type == "1":
            type = "foto"

        elif type == "2":
            type = "video"

        url = input("\nIngrese el url del post: ")

        caption = input("Descripción del post: ")

        seconds = time.time()
        date = time.ctime(seconds)

        tags = []
        tag = input("Ingrese los hashtags: ")
        tags.append(tag)
        while tag != "0":
            tag = input("""[PRESIONE "0" PARA FINALIZAR]
Ingrese otro hashtags: """)
            tags.append(tag)

        post = Multimedia(publisher, type, url, caption, date, tags, [], [], 0, 0, 0)
        self.multimedias.append(post)
        self.save_changes()

    def search_post(self):
    
        filter = input("""
ELIJA UN FILTRO DE BÚSQUEDA:
            
1. User.
2. Hashtags.

[PRESIONE '0' PARA SALIR]

>> """)
        
        #VALIDAMOS EL INPUT DEL FILTRO
        while not filter.isnumeric() or int(filter) not in range(0,3):
            filter = input("""
ERROR! ELIJA UN FILTRO DE BÚSQUEDA:

1. User.
2. Hashtags.

[PRESIONE '0' PARA SALIR]

>> """)
        
        if filter == "1":

            aux = True

            while aux:

                exact_match = 0
                total_matches = 0
                matches = []

                search = input("\nIngrese un nombre de usuario\n\n[PRESIONE '0' PARA SALIR]\n\n>> ")

                if " " in search or len(search) == 0:
                    print("\nNO SIGUES A NINGÚN PERFIL CON ESE NOMBRE DE USUARIO!\n\n====================================================")

                elif search == "0":
                    aux = False

                else:
                    for user in self.users:
                        if user.username.lower() == search.lower() and user.id in self.current_sesion[0].following:
                            print(f"\n@{user.username} - Following: {len(user.following)}")
                            self.access_others(user)
                            exact_match += 1
                        else:
                            x = slice(0, len(search))
                            if search.lower() == user.username[x].lower() and user.id in self.current_sesion[0].following:
                                matches.append(user)
                                total_matches += 1

                    if total_matches > 0:

                        print("\nRESULTADOS DE BÚSQUEDA...\n")

                        for idx, match in enumerate(matches):
                            cont = 0
                            for media in self.multimedias:
                                if match.id == media.publisher:
                                    cont += 1
                            print(f"{idx + 1}. @{match.username.lower()} | Posts: {cont}")

                        select = input("\nIngrese el indice del perfil al que desea ingresar: ")

                        while not select.isnumeric() or int(select) not in range(1,len(matches) + 1):   
                            select = input("Error! Ingrese un indice de perfil válido al que ingresar: ")
        
                        for idx, match in enumerate(matches):
                            if select == str(idx + 1):
                                self.access_others(match)
                                total_matches += 1

                    if exact_match == 0 and total_matches == 0: 
                        print("\nNO SIGUES A NINGÚN PERFIL CON ESE NOMBRE DE USUARIO!\n====================================================")

        elif filter == "2":

            index = 1
            posts_with_tags = {}
            hashtags = []
            search = input("\nIngrese un hashtag para la búsqueda: ")
            hashtags.append(search)
    
            while search != "0":
                search = input("\n========================\n\n[PRESIONE '0' PARA FINALIZAR]\n\nIngrese otro hashtag para la búsqueda\n\n>> ")
                hashtags.append(search)

            if search == "0":
                for post in self.multimedias:
                    if post.publisher in self.current_sesion[0].following:
                        for user in self.users:
                            if user.id == post.publisher:
                                for hashtag in hashtags:
                                    if hashtag in post.tags:
                                        posts_with_tags[index] = post
                                        print(f"\n== POST #{index} ==\n{post.show_attr(user.username.lower())}")
                                        index += 1

            if len(posts_with_tags) == 0:
                print("\nNINGUNO DE LOS USUARIOS QUE SIGUES HA USADO LOS HASHTAGS INGRESADOS!")

            else:
                interact = input("\n========================\n\nPRESIONE '0' PARA SALIR!\nIngrese el indice del post con el que desea interactuar\n\n>> ")

                #VALIDAMOS EL INPUT DE INTERACTUAR
                while not interact.isnumeric() or int(interact) not in range(0, len(posts_with_tags) + 1):
                    interact = input("\n========================\n\nPRESIONE '0' PARA SALIR!\nError! Ingrese un indice válido\n\n>> ")

                #CONDICIÓN PARA FINALIZAR LA ACCIÓN
                if interact == "0":
                    return "FINALIZADO"

                else:
                    for idx, post in posts_with_tags.items():
                        for user in self.users:
                            if interact == str(idx) and user.id == post.publisher:
                                if isinstance(self.current_sesion[0], Admin) or user == self.current_sesion[0]:
                                    interaction = input("\n1. Dar like.\n2. Comentar\n3. Ver likes.\n4. Gestionar comentarios.\n5. Eliminar post.\n\n>> ")
                                    #VALIDAMOS EL INPUT DE LA INTERACCIÓN PARA LOS USARIOS ADMINISTRADORES
                                    while not interaction.isnumeric() or int(interaction) not in range(1,6) or len(interaction) != 1:
                                        interaction = input("\nError! Selecciones una de las opciones:\n\n1. Dar like.\n2. Comentar\n3. Ver likes.\n4. Ver comentarios.\n5. Eliminar post.\n\n>> ")
                                else:
                                    interaction = input("\n1. Dar like.\n2. Comentar\n3. Ver likes.\n4. Ver comentarios.\n\n>> ")
                                    #VALIDAMOS EL INPUT DE LA INTERACCIÓN PARA LOS USARIOS ESTUDIANTES Y PROFESORES
                                    while not interaction.isnumeric() or int(interaction) not in range(1,5) or len(interaction) != 1:
                                        interaction = input("\nError! Selecciones una de las opciones:\n\n1. Dar like.\n2. Comentar\n3. Ver likes.\n4. Ver comentarios.\n\n>> ")
                                if interaction == "1":
                                    post.give_like(self.current_sesion[0], user)
                                elif interaction == "2":
                                    comment = input("\nAgregue un comentario: ")
                                    seconds = time.time()
                                    date = time.ctime(seconds)
                                    post.add_comment(self.current_sesion[0], user, comment, date)
                                elif interaction == "3":
                                    self.view_likes(post)
                                elif interaction == "4":
                                    if isinstance(self.current_sesion[0], Admin) or user == self.current_sesion[0]:
                                        self.delete_offensive_comments(post)
                                    else:
                                        self.view_comments(post)
                                elif interaction == "5":
                                    self.delete_post(post)

        elif filter == "0":
            return "FINALIZADO"

        self.save_changes()

    #MÓDULO DE GESTIÓN DE INTERACCIONES

    def view_likes(self, post):

        if post.cont_likes == 0:
            print("\nUPS! ESTE POST TODAVÍA NO TIENE LIKES...")

        elif post.cont_likes >= 1:

            likers = {}

            print("\n== PERSONAS QUE LE DIERON 'LIKE' A ESTE POST ==\n")
            for index, liker in enumerate(post.likes):
                likers[index + 1] = liker
                print(f"{index + 1}. @{liker.username.lower()}")

            option = input("\nPRESIONE '0' PARA SALIR!\nIngrese el indice del perfil al que desea ingresar: ")

            for indx, liker in likers.items():
                if option == str(indx):
                    self.access_others(liker)

        self.save_changes()

    def view_comments(self, post):

        if post.cont_comments == 0:
            print("\nUPS! ESTE POST TODAVÍA NO TIENE COMENTARIOS...")

        elif post.cont_comments > 0:

            if isinstance(self.current_sesion[0], Admin):
                self.delete_offensive_comments(post)

            else:
                post_comments = {}

                print("\n== COMENTARIOS DE ESTE POST ==\n")
                for index, commenter in enumerate(post.comments):
                    post_comments[index + 1] = commenter
                    print(f"{index + 1}. @{commenter.get('commenter').lower()} comentó '{commenter['comment']}'")

                option = input("\nPRESIONE '0' PARA SALIR!\nIngrese el indice del perfil al que desea ingresar: ")

                for indx, commenter in post_comments.items():
                    if option == str(indx):
                        for user in self.users:
                            if user.username.lower() == commenter["commenter"]:
                                self.access_others(user)

        self.save_changes()

    def follow_user(self, user):

        if user.id == self.current_sesion[0].id:
            print("\nNO TE PUEDES SEGUIR A TI MISMO!")

        elif user.id not in self.current_sesion[0].following:

            if isinstance(user, Student) and isinstance(self.current_sesion[0], Student):
                if user.major == self.current_sesion[0].major:
                    self.current_sesion[0].following.append(user.id)
                    print(f"\nAhora sigues al estudiante '@{user.username}'!")
                elif user.major != self.current_sesion[0].major:         
                    if self.current_sesion[0] in user.follow_requests:
                        option = input("\nYa usted envio una solicitud para seguir a este perfil, desea cancelarla?\n\n1. Si.\n2. No.\n\n>> ")
                        if option == "1":
                            user.follow_requests.remove(self.current_sesion[0])
                        elif option == "2":
                            return "FINALIZADO"
                    elif self.current_sesion[0] not in user.follow_requests:
                        user.follow_requests.append(self.current_sesion[0])
                        print(f"\nSe ha enviado tu solicitud, ahora espera a que '@{user.username}' la acepte!")

            elif isinstance(user, Professor) and isinstance(self.current_sesion[0], Professor):
                if user.department == self.current_sesion[0].department:
                    self.current_sesion[0].following.append(user.id)
                    print(f"\nAhora sigues al profesor '@{user.username}'!")
                elif user.department != self.current_sesion[0].department:
                    if self.current_sesion[0] in user.follow_requests:
                        option = input("\nYa usted envio una solicitud para seguir a este perfil, desea cancelarla?\n\n1. Si.\n2. No.\n\n>> ")
                        if option == "1":
                            user.follow_requests.remove(self.current_sesion[0])
                        elif option == "2":
                            return "FINALIZADO"
                    elif self.current_sesion[0] not in user.follow_requests:
                        user.follow_requests.append(self.current_sesion[0])
                        print(f"\nSe ha enviado tu solicitud, ahora espera a que '@{user.username}' la acepte!")

            else:
                if self.current_sesion[0] in user.follow_requests:
                    option = input("\nYa usted envio una solicitud para seguir a este perfil, desea cancelarla?\n\n1. Si.\n2. No.\n\n>> ")
                    if option == "1":
                        user.follow_requests.remove(self.current_sesion[0])
                    elif option == "2":
                        return "FINALIZADO"
                elif self.current_sesion[0] not in user.follow_requests:
                    user.follow_requests.append(self.current_sesion[0])
                    print(f"\nSe ha enviado tu solicitud, ahora espera a que '@{user.username}' la acepte!")

        else:
            option = input("""\nYa usted sigue a este usuario, desea dejar de seguirlo?

1. Si.
2. No.

>> """)
            
            while not option.isnumeric() or int(option) not in range(0, 3) or len(option) != 1:
                option = input("""\nError! Desea dejar de seguir al usuario?

1. Si.
2. No.

>> """)
            
            if option == "1":
                self.current_sesion[0].following.remove(user.id)
            elif option == "2":
                return "FINALIZADO"
            
        self.save_changes()

    def accept_follow_requests(self):

        user_requets = {}

        for index, request in enumerate(self.current_sesion[0].follow_requests):
            user_requets[index + 1] = request
        
        if len(user_requets) == 0:
            print("\nUSTED NO TIENE SOLICITUDES POR EL MOMENTO!")

        else:
            print("\n== SOLICITUDES DE SEGUIMIENTO ==\n")

            for x, y in user_requets.items():
                print(f"{x}. @{y.username.lower()}")

            option = input("\nIngrese el indice del usuario al que desea aceptar o eliminar: ")

            for index, requester in user_requets.items():
                if option == str(index):
                    accept = input("\n1. Aceptar solicitud.\n2. Eliminar solicitud.\n\n>> ")
                    if accept == "1":
                        self.current_sesion[0].follow_requests.remove(requester)
                        requester.following.append(self.current_sesion[0].id)
                        print(f"\nAhora @{requester.username.lower()} te sigue!")
                    elif accept == "2":
                        self.current_sesion[0].follow_requests.remove(requester)
                        print(f"\nHaz eliminado la solictud de @{requester.username.lower()}!")

        self.save_changes()

    def unfollow_user(self):

        if len(self.current_sesion[0].following) == 0:
            print("\nUPS! TODAVÍA NO SIGUES A NADIE!")

        elif len(self.current_sesion[0].following) >= 1:

            following = {}
    
            print("\n== USUARIOS SEGUIDOS ==\n")
            for index, follow in enumerate(self.current_sesion[0].following):
                following[index + 1] = follow
                for user in self.users:
                    if follow == user.id:
                        print(f"{index + 1}. @{user.username}")

            option = input("\nPRESIONE '0' PARA SALIR!\nIngrese el indice del usuario que desea dejar de seguir\n\n>> ")

            #VALIDAMOS EL INPUT DE LA VARIABLE 'OPTION'
            while not option.isnumeric() or int(option) not in range(0,len(following) + 1):
                option = input("\nPRESIONE '0' PARA SALIR!\nError! Ingrese el indice del usuario que desea dejar de seguir\n\n>> ")

            if option == "0":
                return "FINALIZADO"
            
            else:
                for idx, follow in following.items():
                    if option == str(idx):
                        self.current_sesion[0].following.remove(follow)
                        for user in self.users:
                            if follow == user.id:
                                print(f"Haz dejado de seguir a @{user.username} con exito!")

        self.save_changes()

    #MÓDULO DE GESTIÓN DE MODERACIÓN

    def delete_post(self, media, user):

        if isinstance(self.current_sesion[0], Admin):
            verification = input("\nSEGURO QUE ESTE POST INCUMPLIÓ CON LAS NORMATIVAS ESTABLECIDAS Y POR TANTO DEBE SER ELIMINADO?\n\n1. Si.\n2. No\n\n>> ")
        
            #VALIDAMOS EL INPUT DE LA VARIABLE 'VERIFICATION'
            while not verification.isnumeric() or int(verification) not in range(1,3) or len(verification) != 1:
                verification = input("\nERROR! SEGURO DE QUE ESTE POST INCUMPLIÓ CON LAS NORMATIVAS ESTABLECIDAS Y POR TANTO DEBE SER ELIMINADO?\n\n1. Si.\n2. No\n\n>> ")
            
            if verification == "1":
                print("\nAL ELIMINAR EL POST SE LE AGREGARÁ UNA INFRACCIÓN AL USUARIO!\n")
                type = "Post ofensivo."
                motive = input("Agregar algún comentario sobre la infracción: ")
                user.strikes.append({"type": type, "motive": motive})
                user.cont_posts_taken_down += 1
                self.multimedias.remove(media)
                print("\nEL POST HA SIDO ELIMINADO EXITOSAMENTE!")

        else:
            verification = input("\nSEGURO QUE QUIERES ELIMINAR TU POST?\n\n1. Si.\n2. No\n\n>> ")

            #VALIDAMOS EL INPUT DE LA VARIABLE 'DELETE'
            while not verification.isnumeric() or int(verification) not in range(1,3) or len(verification) != 1:
                verification = input("\nERROR! SEGURO QUE QUIERES ELIMINAR TU POST?\n\n1. Si.\n2. No\n\n>> ")

            if verification == "1":
                self.multimedias.remove(media)
                print("\nEL POST HA SIDO ELIMINADO EXITOSAMENTE!")

            elif verification == "2":
                return "FINALIZADO"
        
        self.save_changes()

    def delete_offensive_comments(self, post):
            
        if len(post.comments) == 0:
            print("\nUPS! ESTE POST TODAVÍA NO TIENE COMENTARIOS...")

        elif len(post.comments) > 0:

            offensive_comments = {}

            print(f"\n== COMENTARIOS DE ESTE POST ==\n")
            for index, offensive_comment in enumerate(post.comments):
                offensive_comments[index + 1] = offensive_comment
                print(f"{index + 1}. @{offensive_comment.get('commenter').lower()} comentó '{offensive_comment['comment']}'")

            delete = input("\nPRESIONES '0' PARA SALIR!\nIngrese el indice del comentario que desea eliminar: ")

            #VALIDAMOS EL INPUT DE LA VARIABLE 'DELETE'
            while not delete.isnumeric() or int(delete) not in range(0,len(offensive_comments) + 1):
                delete = input("\nERROR! PRESIONES '0' PARA SALIR!\nIngrese el indice del comentario que desea eliminar: ")

            if delete == '0':
                return "FINALIZADO"

            else:
                for indx, comment in offensive_comments.items():
                    if delete == str(indx):
                        post.comments.remove(comment)
                        post.cont_comments = len(post.comments)
                        post.cont_interactions -= 1
                        for user in self.users:
                            if user.username.lower() == comment["commenter"]:
                                user.cont_interactions -= 1
                                user.cont_offensive_comments += 1
                            elif post.publisher == user.id:
                                user.cont_interactions -= 1
            
        self.save_changes()

    def delete_user(self, user):

        if len(user.strikes) >= 3:
            verification = input(f"\nESTE USUARIO INCUMPLIÓ CON LAS NORMATIVAS ESTABLECIDAS UN TOTAL DE {len(user.strikes)} VECES Y POR TANTO PUEDE SER ELIMINADO\n\n1. Eliminar.\n2. Cancelar\n\n>> ")

            #VALIDAMOS EL INPUT DE LA VARIABLE 'VERIFICATION'
            while not verification.isnumeric() or int(verification) not in range(1,3) or len(verification) != 1:
                verification = input(f"\nERROR! ESTE USUARIO INCUMPLIÓ CON LAS NORMATIVAS ESTABLECIDAS UN TOTAL DE {len(user.strikes)} VECES Y POR TANTO PUEDE SER ELIMINADO\n\n1. Eliminar.\n2. Cancelar\n\n>> ")

            if verification == "1":
                self.users.remove(user)
                self.deleted_users.append(user)
                print(f"\nEl usuario @{user.username.lower()} ha sido eliminado con exito!")

            elif verification == "2":
                return "FINALIZADO"

        else:
            option = input(f"\nESTE USUARIO NO HA INCUMPLIDO CON LAS NORMATIVAS ESTABLECIDAS SUFICIENTES VECES 'STRIKES: {len(user.strikes)}' Y POR TANTO NO PUEDE SER ELIMINADO\n\n1. Reportar.\n2. Cancelar\n\n>> ")

            #VALIDAMOS EL INPUT DE LA VARIABLE 'OPTION'
            while not option.isnumeric() or int(option) not in range(1,3) or len(option) != 1:
                option = input(f"\nESTE USUARIO NO HA INCUMPLIDO CON LAS NORMATIVAS ESTABLECIDAS SUFICIENTES VECES 'STRIKES: {len(user.strikes)}' Y POR TANTO NO PUEDE SER ELIMINADO\n\n1. Reportar.\n2. Cancelar\n\n>> ")

            if option == "1":
                type = input("\nIngrese el tipo de denucia: ")
                motive = input("Ingrese el motivo de la denuncia: ")
                user.strikes.append({"type": type, "motive": motive})

            elif option == "2":
                return "FINALIZADO"
        
        self.save_changes()

    #MÓDULO DE ESTADÍSTICAS

    def generate_posts_reports(self):
        option = input("""
MAYOR CANTIDAD DE PUBLICACIONES SEGÚN...

1. Usuarios.
2. Carreras.

[PRESIONE "0" PARA SALIR]

>> """)
        
        #VALIDAMOS EL INPUT DE LA VARIABLE 'OPTION'
        while not option.isnumeric() or int(option) not in range(0,3) or len(option) != 1:
            option = input("""
MAYOR CANTIDAD DE PUBLICACIONES SEGÚN...

1. Usuarios.
2. Carreras.

[PRESIONE "0" PARA SALIR]

>> """)

        if option == "1":

            users = []

            for user in self.users:
                cont = 0
                for media in self.multimedias:
                    if user.id == media.publisher:
                        cont += 1
                users.append({"username": user.username, "posts_cont": cont})

            #ALGORITMO DE ORDENAMIENTO - SELECTION SORT

            for i in range(len(users)):
                min_idx = i
                for j in range(i + 1, len(users)):
                    if users[min_idx]["posts_cont"] < users[j]["posts_cont"]:
                        min_idx = j
                users[i], users[min_idx] = users[min_idx], users[i]

            most_posts = users[0]["posts_cont"]
            most_posts_group = []

            for user in users:
                x = (user["posts_cont"] * 100) / most_posts
                if x >= 65:
                    most_posts_group.append(user)

            print("\n== USUARIOS CON MAYOR CANTIDAD DE PUBLICACIONES ==\n")

            for user in most_posts_group:
                print(f"Usuario: @{user['username'].lower()} | Publicaciones: {user['posts_cont']}")

        elif option == "2":

            majors = []
            cont_posts = []
            users_majors = []

            for user in self.users:
                if isinstance(user, Student):
                    cont = 0
                    for media in self.multimedias:
                        if user.id == media.publisher:
                            cont += 1
                    users_majors.append({"major": user.major, "posts_cont": cont})
            
                    if user.major not in majors:
                        majors.append(user.major)

            for major in majors:
                cont_posts.append({"major": major, "posts_cont": 0})

            for career in users_majors:
                for major in cont_posts:
                    if career["major"] == major["major"]:
                        major["posts_cont"] += career["posts_cont"]

            #ALGORITMO DE ORDENAMIENTO - SELECTION SORT

            for i in range(len(cont_posts)):
                min_idx = i
                for j in range(i + 1, len(cont_posts)):
                    if cont_posts[min_idx]["posts_cont"] < cont_posts[j]["posts_cont"]:
                        min_idx = j
                cont_posts[i], cont_posts[min_idx] = cont_posts[min_idx], cont_posts[i]

            #CREAMOS UNA VARIABLE PARA GUARDAR LA CARRERA CON MAYOR CANTIDAD DE PUBLICACIONES

            most_posts = cont_posts[0]["posts_cont"]
            most_posts_group = []

            #UTILIZANDO UNA REGLA DE TRES CALCULAMOS LA CANTIDAD DE POSTS POR CARRERA QUE SE ENCUENTRAN EN UN RANGO DE ENTRE 100%-65%
            #USANDO LA VARIABLE CREADA PREVIAMENTE COMO REFERENCIA

            for major in cont_posts:
                x = (major["posts_cont"] * 100) / most_posts
                if x >= 65:
                    most_posts_group.append(major)

            print("\n== CARRERAS CON MAYOR CANTIDAD DE PUBLICACIONES ==\n")

            for major_posts in most_posts_group:
                print(f"Carrera: {major_posts['major']} | Publicaciones: {major_posts['posts_cont']}")

        elif option == "0":
            return "FINALIZADO"

    def generate_interaction_reports(self):

        option = input("""
MAYOR CANTIDAD DE INTERACCIONES SEGÚN...

1. Posts.
2. Usuarios.

[PRESIONE "0" PARA SALIR]

>> """)

        #VALIDAMOS EL INPUT DE LA VARIABLE 'OPTION'
        while not option.isnumeric() or int(option) not in range(0,3) or len(option) != 1:
            option = input("""
MAYOR CANTIDAD DE INTERACCIONES SEGÚN...

1. Posts.
2. Usuarios.

[PRESIONE "0" PARA SALIR]

>> """)

        if option == "1":

            posts_interacted_with = []

            for post in self.multimedias:
                if post.cont_interactions > 0:
                    posts_interacted_with.append(post)

            if len(posts_interacted_with) == 0:
                print("\nNO HAY POSTS CON INTERACCIONES!")

            else:
                for i in range(len(posts_interacted_with)):
                    min_idx = i
                    for j in range(i + 1, len(posts_interacted_with)):
                        if posts_interacted_with[min_idx].cont_interactions < posts_interacted_with[j].cont_interactions:
                            min_idx = j
                    posts_interacted_with[i], posts_interacted_with[min_idx] = posts_interacted_with[min_idx], posts_interacted_with[i]

            #CREAMOS UNA VARIABLE PARA GUARDAR EL POST CON MAYOR CANTIDAD DE INTERACCIONES

                most_interactions = posts_interacted_with[0].cont_interactions
                most_interactions_group = []

            #UTILIZANDO UNA REGLA DE TRES CALCULAMOS LA CANTIDAD DE INTERACCIONES POR POST QUE SE ENCUENTRAN EN UN RANGO DE ENTRE 100%-65%
            #USANDO LA VARIABLE CREADA PREVIAMENTE COMO REFERENCIA

                for post_interacted_with in posts_interacted_with:
                    x = (post_interacted_with.cont_interactions * 100) / most_interactions
                    if x >= 65:
                        most_interactions_group.append(post_interacted_with)

                print("\n== POSTS CON MAYOR CANTIDAD DE INTERACCIONES ==")

                for most_interacted in most_interactions_group:
                    print(f"\nINTERACCIONES: {most_interacted.cont_interactions}\n\n{most_interacted.show_attr(most_interacted.publisher)}")

        elif option == "2":

            users_with_interactions = []
            
            for user in self.users:
                if user.cont_interactions > 0:
                    users_with_interactions.append(user)

            if len(users_with_interactions) == 0:
                print("\nNO HAY USUARIOS CON INTERACCIONES!")

            else:
                for i in range(len(users_with_interactions)):
                    min_idx = i
                    for j in range(i + 1, len(users_with_interactions)):
                        if users_with_interactions[min_idx].cont_interactions < users_with_interactions[j].cont_interactions:
                            min_idx = j
                    users_with_interactions[i], users_with_interactions[min_idx] = users_with_interactions[min_idx], users_with_interactions[i]

            #CREAMOS UNA VARIABLE PARA GUARDAR EL USUARIO CON MAYOR CANTIDAD DE INTERACCIONES

                most_interactions = users_with_interactions[0].cont_interactions
                most_interactions_group = []

            #UTILIZANDO UNA REGLA DE TRES CALCULAMOS LA CANTIDAD DE INTERACCIONES POR USUARIO QUE SE ENCUENTRAN EN UN RANGO DE ENTRE 100%-65%
            #USANDO LA VARIABLE CREADA PREVIAMENTE COMO REFERENCIA

                for user_with_interactions in users_with_interactions:
                    x = (user_with_interactions.cont_interactions * 100) / most_interactions
                    if x >= 65:
                        most_interactions_group.append(user_with_interactions)

                print("\n== USUARIOS CON MAYOR CANTIDAD DE INTERACCIONES ==")

                for most_interacted in most_interactions_group:
                    print(f"\nINTERACCIONES: {most_interacted.cont_interactions}\n\n{most_interacted.show()}")

        elif option == "0":
            return "FINALIZADO"

    def generate_moderation_reports(self):

        option = input("""
MAYOR CANTIDAD DE INFRACCIONES SEGÚN...

1. Usuarios con la mayor cantidad de post tumbados.
2. Carreras con mayor comentarios inadecuados.
3. Usuarios eliminados por infracciones.

[PRESIONE "0" PARA SALIR]

>> """)

        #VALIDAMOS EL INPUT DE LA VARIABLE 'OPTION'
        while not option.isnumeric() or int(option) not in range(0,4) or len(option) != 1:
            option = input("""
MAYOR CANTIDAD DE INFRACCIONES SEGÚN...

1. Usuarios con la mayor cantidad de post tumbados.
2. Carreras con mayor comentarios inadecuados.
3. Usuarios eliminados por infracciones.

[PRESIONE "0" PARA SALIR]

>> """)

        if option == "1":
              
            users_with_taken_down_posts = []

            for user in self.users:
                if user.cont_posts_taken_down > 0:
                    users_with_taken_down_posts.append(user)

            if len(users_with_taken_down_posts) == 0:
                print("\nNO HAY USUARIOS CON POSTS TUMBADOS!")
    
            else:
                for i in range(len(users_with_taken_down_posts)):
                    min_idx = i
                    for j in range(i + 1, len(users_with_taken_down_posts)):
                        if users_with_taken_down_posts[min_idx].cont_posts_taken_down < users_with_taken_down_posts[j].cont_posts_taken_down:
                            min_idx = j
                    users_with_taken_down_posts[i], users_with_taken_down_posts[min_idx] = users_with_taken_down_posts[min_idx], users_with_taken_down_posts[i]

                #CREAMOS UNA VARIABLE PARA GUARDAR AL USUARIO CON MAYOR CANTIDAD DE POSTS TUMBADOS

                most_posts_taken_down = users_with_taken_down_posts[0].cont_posts_taken_down
                most_posts_taken_down_group = []

                #UTILIZANDO UNA REGLA DE TRES CALCULAMOS LA CANTIDAD DE POSTS TUMBADOS POR USUARIO QUE SE ENCUENTRAN EN UN RANGO DE ENTRE 100%-65%
                #USANDO LA VARIABLE CREADA PREVIAMENTE COMO REFERENCIA

                for user_with_taken_down_posts in users_with_taken_down_posts:
                    x = (user_with_taken_down_posts.cont_posts_taken_down * 100) / most_posts_taken_down
                    if x >= 65:
                        most_posts_taken_down_group.append(user_with_taken_down_posts)

                print("\n== USUARIOS CON MAYOR CANTIDAD DE POSTS TUMBADOS ==")

                for most_taken_down in most_posts_taken_down_group:
                    print(f"\nPOSTS TUMBADOS: {most_taken_down.cont_posts_taken_down}\n\n{most_taken_down.show()}")

        elif option == "2":

            majors = []

            for user in self.users:
                if isinstance(user, Student):
                    if len(majors) == 0:
                        majors.append({"major": user.major, "offensive_comments": 0})
                    elif len(majors) > 0:
                        cont = 0
                        for major in majors:
                            if major["major"] == user.major:
                                cont += 1
        
                        if cont == 0:
                            majors.append({"major": user.major, "offensive_comments": 0})

            for user in self.users:
                if isinstance(user, Student):
                    for major in majors:
                        if user.major == major["major"]:
                            major["offensive_comments"] += user.cont_offensive_comments

            cont = 0
            for major in majors:
                if major["offensive_comments"] > 0:
                    cont += 1

            if cont == 0:
                print("\nNO HAY CARRERAS CON COMENTARIOS INADECUADOS!")

            else:

                #ALGORITMO DE ORDENAMIENTO - SELECTION SORT

                for i in range(len(majors)):
                    min_idx = i
                    for j in range(i + 1, len(majors)):
                        if majors[min_idx]["offensive_comments"] < majors[j]["offensive_comments"]:
                            min_idx = j
                    majors[i], majors[min_idx] = majors[min_idx], majors[i]

                #CREAMOS UNA VARIABLE PARA GUARDAR LA CARRERA CON MAYOR CANTIDAD DE COMENTARIOS INADECUADOS

                most_offensive_comments = majors[0]["offensive_comments"]
                most_offensive_comments_group = []

                #UTILIZANDO UNA REGLA DE TRES CALCULAMOS LA CANTIDAD DE COMENTARIOS INADECUADOS POR CARRERA QUE SE ENCUENTRAN EN UN RANGO DE ENTRE 100%-65%
                #USANDO LA VARIABLE CREADA PREVIAMENTE COMO REFERENCIA

                for major in majors:
                    x = (major["offensive_comments"] * 100) / most_offensive_comments
                    if x >= 65:
                        most_offensive_comments_group.append(major)

                print("\n== CARRERAS CON MAYOR COMENTARIOS INADECUADOS ==")

                for major_offensive_comments in most_offensive_comments_group:
                    print(f"\nCARRERA: {major_offensive_comments['major']}\nCOMENTARIOS INADECUADOS: {major_offensive_comments['offensive_comments']}")

        elif option == "3":

            if len(self.deleted_users) == 0:
                print("\nNO HAY USUARIOS ELIMINADOS POR INFRACCIONES!")

            else:
                print("\n== USUARIOS ELIMINADOS POR INFRACCIONES ==")

                for user in self.deleted_users:
                    print(f"\nUSUARIO: @{user.username}\nINFRACCIONES: {len(user.strikes)}\n")
                    for strike in user.strikes:
                        print(f"- TIPO: {strike['type']} - MOTIVO {strike['motive']}")

        elif option == "0":
            return "FINALIZADO"

    def save_changes(self):

        users = []
        posts = []
        saved_deleted_users = []

        for u in self.users:
            if isinstance(u, Student):
                student_saved = {
"id": u.id,
"firstName": u.firstName,
"lastName": u.lastName,
"email": u.email,
"username": u.username,
"type": "student",
"major": u.major,
"following": u.following,
"follow_requests": u.follow_requests,
"strikes": u.strikes,
"cont_interactions": u.cont_interactions,
"cont_posts_taken_down": u.cont_posts_taken_down,
"cont_offensive_comments": u.cont_offensive_comments
}
                users.append(student_saved)
            elif isinstance(u, Professor):
                professor_saved = {
"id": u.id,
"firstName": u.firstName,
"lastName": u.lastName,
"email": u.email,
"username": u.username,
"type": "professor",
"department": u.department,
"following": u.following,
"follow_requests": u.follow_requests,
"strikes": u.strikes,
"cont_interactions": u.cont_interactions,
"cont_posts_taken_down": u.cont_posts_taken_down,
"cont_offensive_comments": u.cont_offensive_comments
}
                users.append(professor_saved)
              
            elif isinstance(u, Admin):
                admin_saved = {
"id": u.id,
"firstName": u.firstName,
"lastName": u.lastName,
"email": u.email,
"username": u.username,
"type": "admin",
"following": u.following,
"password": u.password,
"follow_requests": u.follow_requests,
"strikes": u.strikes,
"cont_interactions": u.cont_interactions,
"cont_posts_taken_down": u.cont_posts_taken_down,
"cont_offensive_comments": u.cont_offensive_comments
}

                users.append(admin_saved)

        with open("Metrogram_users.json", "w") as file:
            json.dump(users, file, indent = 4)
            file.close()

        for user in self.deleted_users:
                if isinstance(user, Student):
                    save_student = {
"id": user.id,
"firstName": user.firstName,
"lastName": user.lastName,
"email": user.email,
"username": user.username,
"type": "student",
"major": user.major,
"following": user.following,
"follow_requests": user.follow_requests,
"strikes": user.strikes,
"cont_interactions": user.cont_interactions,
"cont_posts_taken_down": user.cont_posts_taken_down,
"cont_offensive_comments": user.cont_offensive_comments
}
                    saved_deleted_users.append(save_student)

                elif isinstance(user, Professor):
                    save_professor = {
"id": user.id,
"firstName": user.firstName,
"lastName": user.lastName,
"email": user.email,
"username": user.username,
"type": "professor",
"department": user.department,
"following": user.following,
"follow_requests": user.follow_requests,
"strikes": user.strikes,
"cont_interactions": user.cont_interactions,
"cont_posts_taken_down": user.cont_posts_taken_down,
"cont_offensive_comments": user.cont_offensive_comments
}
                    saved_deleted_users.append(save_professor)

                elif isinstance(user, Admin):
                    save_admin = {
"id": user.id,
"firstName": user.firstName,
"lastName": user.lastName,
"email": user.email,
"username": user.username,
"type": "admin",
"following": user.following,
"password": user.password,
"follow_requests": user.follow_requests,
"strikes": user.strikes,
"cont_interactions": user.cont_interactions,
"cont_posts_taken_down": user.cont_posts_taken_down,
"cont_offensive_comments": user.cont_offensive_comments
}
                    saved_deleted_users.append(save_admin)

        with open("Metrogram_deleted_users.json", "w") as file:
            json.dump(saved_deleted_users, file, indent = 4)
            file.close()

        for post in self.multimedias:
            media_saved = {
"publisher": post.publisher,
"type": post.type,
"caption": post.caption,
"date": post.date,
"tags": post.tags,
"multimedia": post.multimedia,
"comments": post.comments,
"likes": post.likes,
"cont_likes": post.cont_likes,
"cont_comments": post.cont_comments,
"cont_interactions": post.cont_interactions
}
            posts.append(media_saved)

        with open("Metrogram_media.json", "w") as file:
            json.dump(posts, file, indent = 4)
            file.close()

    #MÉTODO PARA INICIAR EL PROGRAMA

    def start(self):

        url_1 = 'https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/08d4d2ce028692d71e9f8c32ea8c29ae24efe5b1/users.json'
        url_2 = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/main/posts.json"

        cont = 0

        while True:
  
            with open("Metrogram_users.json", "r") as file_1:
                if file_1.read() != '':
                    x = "1"
                else:
                    x = "2"

            if x == "1":
                with open("Metrogram_users.json", "r") as file:
                    users = json.load(file)
                with open("Metrogram_media.json", "r") as file:
                    posts = json.load(file)

                self.get_users(users)
                self.get_multi(posts)

                cont += 1
                break

            if x == "2":
                url_1 = requests.get(url_1)
                url_2 = requests.get(url_2)
                if url_1.status_code == 200 and url_2.status_code == 200:
                    users = url_1.json() 
                    posts = url_2.json()
                    break

        if cont == 0:
            self.get_users(users)
            self.get_multimedias(posts)
            self.users.append(Admin("293jffj-3f32wf3wkdl", "Nicolás", "Planas", "planas.nicolas@correounimet.edu.ve", "nikster420", [], "123"))

            saved_users = []
            saved_posts = []
            saved_deleted_users = []

            for user in self.users:
                if isinstance(user, Student):
                    save_student = {
"id": user.id,
"firstName": user.firstName,
"lastName": user.lastName,
"email": user.email,
"username": user.username,
"type": "student",
"major": user.major,
"following": user.following,
"follow_requests": user.follow_requests,
"strikes": user.strikes,
"cont_interactions": user.cont_interactions,
"cont_posts_taken_down": user.cont_posts_taken_down,
"cont_offensive_comments": user.cont_offensive_comments
}
                    saved_users.append(save_student)

                elif isinstance(user, Professor):
                    save_professor = {
"id": user.id,
"firstName": user.firstName,
"lastName": user.lastName,
"email": user.email,
"username": user.username,
"type": "professor",
"department": user.department,
"following": user.following,
"follow_requests": user.follow_requests,
"strikes": user.strikes,
"cont_interactions": user.cont_interactions,
"cont_posts_taken_down": user.cont_posts_taken_down,
"cont_offensive_comments": user.cont_offensive_comments
}
                    saved_users.append(save_professor)

                elif isinstance(user, Admin):
                    save_admin = {
"id": user.id,
"firstName": user.firstName,
"lastName": user.lastName,
"email": user.email,
"username": user.username,
"type": "admin",
"following": user.following,
"password": user.password,
"follow_requests": user.follow_requests,
"strikes": user.strikes,
"cont_interactions": user.cont_interactions,
"cont_posts_taken_down": user.cont_posts_taken_down,
"cont_offensive_comments": user.cont_offensive_comments
}
                    saved_users.append(save_admin)

            with open("Metrogram_users.json", "w") as file:
                json.dump(saved_users, file, indent = 4)
                file.close()

            for user in self.deleted_users:
                if isinstance(user, Student):
                    save_student = {
"id": user.id,
"firstName": user.firstName,
"lastName": user.lastName,
"email": user.email,
"username": user.username,
"type": "student",
"major": user.major,
"following": user.following,
"follow_requests": user.follow_requests,
"strikes": user.strikes,
"cont_interactions": user.cont_interactions,
"cont_posts_taken_down": user.cont_posts_taken_down,
"cont_offensive_comments": user.cont_offensive_comments
}
                    saved_deleted_users.append(save_student)

                elif isinstance(user, Professor):
                    save_professor = {
"id": user.id,
"firstName": user.firstName,
"lastName": user.lastName,
"email": user.email,
"username": user.username,
"type": "professor",
"department": user.department,
"following": user.following,
"follow_requests": user.follow_requests,
"strikes": user.strikes,
"cont_interactions": user.cont_interactions,
"cont_posts_taken_down": user.cont_posts_taken_down,
"cont_offensive_comments": user.cont_offensive_comments
}
                    saved_deleted_users.append(save_professor)

                elif isinstance(user, Admin):
                    save_admin = {
"id": user.id,
"firstName": user.firstName,
"lastName": user.lastName,
"email": user.email,
"username": user.username,
"type": "admin",
"following": user.following,
"password": user.password,
"follow_requests": user.follow_requests,
"strikes": user.strikes,
"cont_interactions": user.cont_interactions,
"cont_posts_taken_down": user.cont_posts_taken_down,
"cont_offensive_comments": user.cont_offensive_comments
}
                    saved_deleted_users.append(save_admin)

            with open("Metrogram_deleted_users.json", "w") as file:
                json.dump(saved_deleted_users, file, indent = 4)
                file.close()

            for post in self.multimedias:
                save_multimedia = {
"publisher": post.publisher,
"type": post.type,
"caption": post.caption,
"date": post.date,
"tags": post.tags,
"multimedia": post.multimedia,
"comments": post.comments,
"likes": post.likes,
"cont_likes": post.cont_likes,
"cont_comments": post.cont_comments,
"cont_interactions": post.cont_interactions
}
                saved_posts.append(save_multimedia)

            with open("Metrogram_media.json", "w") as file:
                json.dump(saved_posts, file, indent = 4)
                file.close()
        
        loop = "S"

        while loop == "S":

            start = input("""
¡BIENVENIDO A METROGRAM!
========================
1. Iniciar sesión.
2. Crear cuenta.

[PRESIONE "0" PARA SALIR]

>> """)

            #VALIDAMOS EL INPUT DE LA VARIABLE 'START'
            while not start.isnumeric() or int(start) not in range(0,3) or len(start) != 1:
                start = input("""
UPS, ESA OPCIÓN NO ES VÁLIDA...

¡BIENVENIDO A METROGRAM!
========================
1. Iniciar sesión.
2. Crear cuenta.

[PRESIONE "0" PARA SALIR]

>> """)

            if start == "1":

                print("\n== INICIO DE SESIÓN ==\n")

                login = input('[PRESIONE "0" PARA SALIR] | Ingrese su nombre de usuario: ').lower()

                if login == "0":
                    loop = "S"

                else:

                    cont = 0

                    for user in self.users:
                        if user.username.lower() == login:
                            self.current_sesion.append(user)
                            cont += 1
                            if isinstance(user, Admin):
                                password = input("Ingrese la contraseña de administrador: ").lower()
                                while password != user.password:
                                    password = input("Error! Ingrese la contraseña correcta: ").lower()

                    if cont == 0:
                        print("\nNO EXISTE NINGÚN USUARIO CON ESE NOMBRE DE PERFIL!")
                        loop = "S"
                    
                    elif cont > 0:
                        loop = "C"

            elif start == "2":
                self.create_user()
                loop = "S"

            elif start == "0":
                exit()

            while loop == "C":
                if len(self.current_sesion) >= 1:
                    print(f"\nSesión actual: {self.current_sesion[0].username}")
                menu = input("""
PÁGINA PRINCIPAL
================

1. Mi perfil.
2. Buscar perfil.
3. Subir post.
4. Buscar post.
5. Estadísticas.

[PRESIONE "0" PARA CERRAR SESIÓN]

>> """)

                #VALIDAMOS EL INPUT DE LA VARIABLE 'MENU'
                while not menu.isnumeric() or int(menu) not in range(0,6) or len(menu) != 1:
                    menu = input("""
PÁGINA PRINCIPAL
================

1. Mi perfil.
2. Buscar perfil.
3. Subir post.
4. Buscar post.
5. Estadísticas.

[PRESIONE "0" PARA CERRAR SESIÓN]

>> """)

                if menu == "1":
                    option = input(f"""
=== MI PERFIL ===

1. Editar perfil.
2. Borrar los datos de la cuenta.
3. Ver mis publicaciones.
4. Solicitudes de seguimiento ({len(self.current_sesion[0].follow_requests)}).
5. Ver seguidos.

[PRESIONE "0" PARA SALIR]

>> """)

                    #VALIDAMOS EL INPUT DE LA VARIABLE 'OPTION'
                    while not option.isnumeric() or int(option) not in range(0,6) or len(option) != 1:
                        option = input(f"""
=== MI PERFIL ===

1. Editar perfil.
2. Borrar los datos de la cuenta.
3. Ver mis publicaciones.
4. Solicitudes de seguimiento ({len(self.current_sesion[0].follow_requests)}).
5. Ver seguidos.

[PRESIONE "0" PARA SALIR]

>> """)

                    if option == "1":
                        self.edit_user()

                    elif option == "2":
                        self.delete_data()
                        self.current_sesion = []
                        loop = "S"

                    elif option == "3":
                        self.access_others(self.current_sesion[0])

                    elif option == "4":
                        self.accept_follow_requests()

                    elif option == "5":
                        self.unfollow_user()

                    elif option == "0":
                        loop == "C"
                    
                elif menu == "2":
                    self.search_user()

                elif menu == "3":
                    self.upload_post()

                elif menu == "4":
                    self.search_post()

                elif menu == "5":
                    option = input("""

== GENERAR INFORMES ==

1. Publicaciones.
2. Interacción.
3. Moderación.

[PRESIONE "0" PARA SALIR]

>> """)

                    #VALIDAMOS EL INPUT DE LA VARIABLE 'OPTION'
                    while not option.isnumeric() or int(option) not in range(0,4) or len(option) != 1:
                        option = input("""

== GENERAR INFORMES ==

1. Publicaciones.
2. Interacción.
3. Moderación.

[PRESIONE "0" PARA SALIR]

>> """)

                    if option == "1":
                        self.generate_posts_reports()

                    elif option == "2":
                        self.generate_interaction_reports()

                    elif option == "3":
                        self.generate_moderation_reports()

                    elif option == "0":
                        loop == "C"

                elif menu == "0":
                    self.current_sesion = []
                    loop = "S"