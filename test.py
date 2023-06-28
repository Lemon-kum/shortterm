# -*- codeing = utf-8 -*-
# @Time : 2023/6/28 9:07
# @Author : dujinjie
# @File : test.py
# @Software : PyCharm

# coding: utf-8
import os
import sqlite3
from flask import Flask, render_template, request, redirect, send_file

app = Flask(__name__)

DB_NAME = 'file_index.db'
INDEX_DIR = ''


def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT,
                  filepath TEXT,
                  filetype TEXT,
                  content TEXT)''')
    conn.commit()
    conn.close()


def index_files(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.pdf') or file_name.endswith('.docx'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'rb') as file:
                    content = file.read()
                    insert_file(file_name, file_path, content)


def insert_file(filename, filepath, content):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO files (filename, filepath, filetype, content) VALUES (?, ?, ?, ?)',
              (filename, filepath, filename.split('.')[-1], content))
    conn.commit()
    conn.close()


def search_files(keyword):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM files WHERE content LIKE ?", ('%' + keyword + '%',))
    results = c.fetchall()
    conn.close()
    return results


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    global INDEX_DIR
    INDEX_DIR = request.form['directory']
    create_table()
    index_files(INDEX_DIR)
    return redirect('/search')


@app.route('/search')
def search():
    keyword = request.args.get('keyword', '')
    results = search_files(keyword)
    return render_template('search.html', keyword=keyword, results=results)


@app.route('/save', methods=['POST'])
def save_results():
    selected_results = request.form.getlist('result')
    if len(selected_results) == 0:
        return redirect('/search')

    with open('result.txt', 'w') as file:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT content FROM files WHERE id IN ({seq})".format(seq=','.join(['?'] * len(selected_results))),
                  selected_results)
        contents = c.fetchall()
        for content in contents:
            file.write(content[0].decode('utf-8'))
            file.write('\n' + '-' * 50 + '\n')
        conn.close()

    return send_file('result.txt', as_attachment=True, attachment_filename='result.txt')


if __name__ == '__main__':
    app.run(debug=True)

