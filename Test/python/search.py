import os
import PyPDF2
from docx import Document
from flask import Flask, render_template, request

app = Flask(__name__)

# 选择目录并遍历文件
def traverse_directory(directory):
    indexed_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.pdf'):
                indexed_files.append({'path': file_path, 'extension': 'pdf'})
            elif file.endswith('.docx'):
                indexed_files.append({'path': file_path, 'extension': 'docx'})

    return indexed_files

# 提取PDF文件中的文本
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page in range(reader.numPages):
            text += reader.getPage(page).extractText()

    return text

# 提取Word文件中的文本
def extract_text_from_word(file_path):
    document = Document(file_path)
    paragraphs = [p.text for p in document.paragraphs]
    return '\n'.join(paragraphs)

# 构建文件索引
def build_index(directory):
    indexed_files = traverse_directory(directory)

    for file_info in indexed_files:
        if file_info['extension'] == 'pdf':
            text = extract_text_from_pdf(file_info['path'])
        elif file_info['extension'] == 'docx':
            text = extract_text_from_word(file_info['path'])

        # 建立索引，存储path、extension和text内容等信息
        # 可以使用数据库或其他数据结构进行存储

    return indexed_files

# 查询关键字
def search_keyword(keyword, indexed_files):
    results = []

    for file_info in indexed_files:
        if keyword in file_info['text']:
            # 添加匹配结果的文件路径和包含关键字的内容行
            results.append({'path': file_info['path'], 'lines': get_matching_lines(file_info['text'], keyword)})

    return results

# 获取包含关键字的行号和内容
def get_matching_lines(text, keyword):
    lines = text.split('\n')
    matching_lines = []

    for i, line in enumerate(lines):
        if keyword in line:
            matching_lines.append({'line_number': i+1, 'line_content': line})

    return matching_lines

# 主页路由
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = search_keyword(keyword, indexed_files)
        return render_template('results.html', keyword=keyword, results=results)
    else:
        return render_template('index.html')

# 选择目录并建立索引
search_directory = '/path/to/your/directory'
indexed_files = build_index(search_directory)

if __name__ == '__main__':
    app.run()
