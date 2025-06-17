from fastapi import FastAPI, Body
import requests
import re
import pymysql
from fastapi import Query, HTTPException, File, UploadFile, Depends
from tkinter import *
import tkinter.ttk as ttk
import pandas as pd
from pandas import json_normalize

app = FastAPI()


@app.get("/")
def read_root():
    print("TEMP")


#== Registration START ===
@app.post("/login-check")
async def login_check(username=Body("user_id"), password=Body("user_pw")):
    try:
        connection = pymysql.connect(
            host='192.168.0.13',
            user='root',
            password='1234',
            db='test_data',
            charset='utf8',
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM personal_info WHERE user_id=%s AND user_pw=%s", (username, password))
        user = cursor.fetchone()

        if user:
            return {"status": "success", "message": "Login successful"}
        else:
            return {"status": "error", "message": "Invalid credentials"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        connection.close()
        

@app.post("/sign-up")
async def sign_up(user_id=Body("user_id"), user_pw=Body("user_pw"), name=Body("name"), age=Body("age"), intended_major=Body("intended_major"), email=Body("email")):
    # Validate input formats
    if not re.match(r"^[\w\s]{2,20}$", name):
        return {"status": "error", "message": "Invalid name format"}
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return {"status": "error", "message": "Invalid email format"}
    
    try:
        connection = pymysql.connect(
            host='192.168.0.13',
            user='root',
            password='1234',
            db='test_data',
            charset='utf8',
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM personal_info WHERE user_id=%s", (user_id))
        user = cursor.fetchone()

        if not user:
            cursor.execute("INSERT INTO personal_info (user_id, user_pw, name, age, intended_major, email) VALUES (%s, %s, %s, %s, %s, %s)", 
                           (user_id, user_pw, name, age, intended_major, email))
            connection.commit()
            return {"status": "success", "message": "Account created successfully!"}
        else:
            return {"status": "error", "message": "Denied: Account already exists with this username."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        connection.close()
#== Registration END ===


#== Post START ===
@app.post("/post-upload")
async def post_upload(time=Body("upload_time"), content=Body("content"), author=Body("author"),aunonymous=Body("anonymous")):
    try:
        connection = pymysql.connect(
            host='192.168.0.13',
            user='root',
            password='1234',
            db='test_data',
            charset='utf8',
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO post (upload_time, content, author, anonymous) VALUES (%s, %s, %s, %s)", (time, content, author, aunonymous))
        connection.commit()
        return {"status": "success", "message": "Post uploaded successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        connection.close()


@app.get("/post-list")
async def post_list():
    try:
        connection = pymysql.connect(
            host='192.168.0.13',
            user='root',
            password='1234',
            db='test_data',
            charset='utf8',
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM post")
        posts = cursor.fetchall()
        post_list = []
        for post in posts:
            post_list.append({
                "post_id": post[0],
                "upload_time": post[1],
                "content": post[2]
            })
        return {"status": "success", "posts": post_list}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        connection.close()

@app.post("/my-post-list")
async def my_post_list(author=Body("author")):
    try:
        connection = pymysql.connect(
            host='192.168.0.13',
            user='root',
            password='1234',
            db='test_data',
            charset='utf8',
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM post WHERE author=%s", (author))
        my_posts = cursor.fetchall()

        my_post_list = []
        for post in my_posts:
            my_post_list.append({
                "post_id": post[0],
                "upload_time": post[1],
                "content": post[2]
            })
        return {"status": "success", "posts": my_post_list}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        connection.close()


