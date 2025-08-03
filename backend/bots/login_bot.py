import pymysql
from pymysql.err import MySQLError as Error
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
import bcrypt
import os

load_dotenv()

def login_signup(email: str, password: str):
    conn = None
    print(email, password)
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="shopbuddy",
            cursorclass=DictCursor,
            autocommit=True
        )
        cursor = conn.cursor()
        print(f"🔐 Attempting to sign in or sign up with email: {email}")
        cursor.execute("SELECT user_id, password FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            user_id, stored_hash = result['user_id'], result['password']
            if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                print(f"✅ Logged in as {email}")
                return {
                    "status": "signed_in",
                    "message": "User authenticated successfully.",
                    "user_id": user_id
                }
            else:
                return {
                    "status": "error",
                    "message": "Incorrect password."
                }

        else:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(f"🔐 Signing up new user: {email}")
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed))
            cursor.execute("SELECT LAST_INSERT_ID()")
            user_id = cursor.fetchone()['LAST_INSERT_ID()']
            print(f"🆕 User signed up with email: {email}")
            return {
                "status": "signed_up",
                "message": "New user created and signed up.",
                "user_id": user_id
            }

    except Error as e:
        print("❌ Database error:", e)
        return {"status": "error", "message": str(e)}

    finally:
        if conn and conn.open:
            cursor.close()
            conn.close()



