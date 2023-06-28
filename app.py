#codeing utf-8
import os
import sqlite3
from flask import Flask, render_template, request, redirect, send_file

app = Flask(__name__)

DB_NAME = 'file_index.db'

#创建数据库表
def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filepath TEXT,
                  filetype TEXT,
                  content TEXT)''')
    conn.commit()
    conn.close()