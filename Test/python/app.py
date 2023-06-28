# -*- codeing = utf-8 -*-
# @Time : 2023/6/28 10:29
# @Author : dujinjie
# @File : app.py
# @Software : PyCharm
import sqlite3

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 建立索引数据库，用于保存检索文件的路径和信息
def create_database():
    conn = sqlite3.connect("fileindex.db")
    print("成功打开数据库")
    cursor = conn.cursor()
    #建立文件存储表
    cursor.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT)")
    #建立检索结果存储表
    cursor.execute("CREATE TABLE IF NOT EXISTS indexes (id INTEGER PRIMARY KEY AUTOINCREMENT, file_id INTEGER, line_number INTEGER, line_content TEXT)")
    conn.commit()
    conn.close()
    print("成功建表")

# 建立文件索引
def build_index(folder_path):
    conn = sqlite3.connect("fileindex.db")
    c = conn.cursor()
    c.execute("DELETE FROM files")
    c.execute("DELETE FROM indexes")

    # 遍历文件夹下的所有文件
    file_id = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 只索引pdf和word文件
            if file.endswith('.pdf') or file.endswith('.docx'):
                file_id += 1
                filename = os.path.join(root, file)
                c.execute("INSERT INTO files (id, filename) VALUES (?, ?)", (file_id, filename))

                # 搜索关键字并建立索引
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line_number, line_content in enumerate(lines, start=1):
                        c.execute("INSERT INTO indexes (file_id, line_number, line_content) VALUES (?, ?, ?)",
                                  (file_id, line_number, line_content))

    conn.commit()
    conn.close()

# 根据关键字搜索并返回结果
def search_keyword(keyword):
    conn = sqlite3.connect("fileindex.db")
    c = conn.cursor()
    c.execute(
        "SELECT files.filename, indexes.line_number, indexes.line_content FROM files INNER JOIN indexes ON files.id = indexes.file_id WHERE indexes.line_content LIKE ?",
        ('%' + keyword + '%',))
    results = c.fetchall()
    conn.close()
    return results

# 保存结果到文本文件并下载
def save_results(results):
    with open('results.txt', 'w', encoding='utf-8') as f:
        for result in results:
            filename, line_number, line_content = result
            f.write(f"{filename} - Line {line_number}: {line_content}\n")
    return 'results.txt'

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    folder = request.form['folder']
    keyword = request.form['keyword']

    # 在数据库中搜索匹配的文件
    results = []
    for file in file_index:
        if keyword.lower() in file['content'].lower():
            results.append(file)

    return jsonify(results)
