from flask import Flask, render_template, request, jsonify
import os
import mysql.connector
import pdfplumber
from docx import Document

app = Flask(__name__)

# 连接MySQL数据库
cnx = mysql.connector.connect(user='sa', password='123456', host='127.0.0.1', database='ST')
cursor = cnx.cursor()

# 设置查询目录，默认为空
query_directory = ""

# 建立文件索引
def build_index(directory):
    # 清空数据库表
    cursor.execute("TRUNCATE TABLE file_index")
    
    # 遍历目录，将pdf和word文件插入数据库
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                file_name = file
                file_path = os.path.join(root, file)
                
                # 提取PDF文件内容
                with pdfplumber.open(file_path) as pdf:
                    content = ""
                    for page in pdf.pages:
                        content += page.extract_text()
                
                cursor.execute("INSERT INTO file_index (file_name, file_path, content) VALUES (%s, %s, %s)",
                               (file_name, file_path, content))
            
            elif file.endswith(".doc") or file.endswith(".docx"):
                file_name = file
                file_path = os.path.join(root, file)
                
                # 提取Word文件内容
                doc = Document(file_path)
                content = ""
                for paragraph in doc.paragraphs:
                    content += paragraph.text
                
                cursor.execute("INSERT INTO file_index (file_name, file_path, content) VALUES (%s, %s, %s)",
                               (file_name, file_path, content))
    
    cnx.commit()

# 执行查询
def run_query(keyword):
    cursor.execute("SELECT * FROM file_index WHERE content LIKE %s", ("%" + keyword + "%",))
    result = cursor.fetchall()
    return result

# 保存为文本文件
def save_text_file(file_ids):
    content = ""
    
    for file_id in file_ids:
        cursor.execute("SELECT * FROM file_index WHERE file_id = %s", (file_id,))
        result = cursor.fetchone()
        content += "路径" + result[2] + "\\" + result[1] + "\n"
        # 处理包含关键字的内容行
        
    # 保存为文本文件
    with open("result.txt", "w") as f:
        f.write(content)
    
    return "result.txt"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"]
    result = run_query(keyword)
    return jsonify(result)

@app.route("/save", methods=["POST"])
def save():
    file_ids = request.form.getlist("file_ids[]")
    saved_file = save_text_file(file_ids)
    return jsonify({"file": saved_file})

@app.route("/set_directory", methods=["POST"])
def set_directory():
    global query_directory
    query_directory = request.form["directory"]
    build_index(query_directory)  # 根据新选择的目录建立索引
    return jsonify({"message": "Directory set successfully!"})

if __name__ == "__main__":
    app.run()
