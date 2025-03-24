'''this file will include all functions relating to session management'''
import json
import os


def on_close():
    '''
    erases session data and fully exits.
    '''
    logout()
    print("shutting down...")
    exit()

def logout():
    '''
    deletes previously created session file
    '''
    if os.path.exists("./assets/session.json"):
        os.remove("./assets/session.json")
    print("you have been logged out")

##TODO add hash password to create_session
def create_session(email):
    '''will create session file in the current directory if it does not exist'''
    session_data= {"email": email}
    with open("./assets/session.json", "w") as session_file:
        json.dump(session_data, session_file)


def verify_session():
    '''verifies the existence of a valid session file, will exit if file does not exist or is invalid'''
    try:
        session_file="./assets/session.json"
        with open(session_file, "r") as file:
            session_data=json.load(file)
        user_email= session_data.get("email")
    except FileNotFoundError:
        print("invalid session")
        exit()

    if not user_email:
        print("invalid session.")
        exit()

