from flask import Flask, request, render_template
import re
import PyPDF2
import os
from docx import Document
import win32com.client as win32
import os
from flask import send_file

document_path = 'C:\\Users\\DELL\\Desktop\\课程文件\\短学期测试\\2-327.docx'
output_path = 'out.txt'
kw = '是'

#............pdf转txt
#......................................
def pdf_txt(document_path,output_path):
#打开PDF文件
    pdf_file = open(document_path, 'rb')

# 创建PDF文件阅读器对象
    pdf_reader = PyPDF2.PdfReader(pdf_file)

# 获取PDF文档的页数
    pages_num = len(pdf_reader.pages)

# 将PDF文档转换为TXT格式
    with open(output_path, 'w') as txt_file:
        for page_index in range(pages_num):
            page_content = pdf_reader.pages[page_index].extract_text()
            txt_file.write(page_content)

# 关闭PDF文件
    pdf_file.close()
    return output_path


#.........txt中检索关键字
def txt_search(output_path):    
    f = open(output_path,'r')
    key_word = kw
    i = 1
    lines = f.readlines()
    for line in lines:
        if re.search(key_word,line):
            print(i,' ',line)
        i = i+1        


#.........word转txt
def word_txt(document_path,output_path):
# 打开DOCX文件
    doc_path = document_path
    doc = Document(doc_path)

# 保存为临时的DOC文件
    temp_doc_path = 'temp.doc'
    doc.save(temp_doc_path)

# 指定输出PDF文件路径
    pdf_path = document_path.replace('.docx','.pdf')

# 创建Word应用程序实例
    word = win32.gencache.EnsureDispatch('Word.Application')

    try:
    # 打开临时的DOC文件
        doc_word = word.Documents.Open(os.path.abspath(temp_doc_path))

    # 将DOC文件另存为PDF
        doc_word.SaveAs(os.path.abspath(pdf_path), FileFormat=17)

    finally:
    # 关闭Word应用程序并退出
        if doc_word:
            doc_word.Close()
        word.Quit()

# 删除临时的DOC文件
    os.remove(temp_doc_path)

    print(f"DOCX文件已成功转换为PDF：{pdf_path}")
    pdf_txt(pdf_path,output_path)
    return output_path


index = document_path.find('.pdf')
if index != -1:
    txt_search(pdf_txt(document_path,output_path))
index2 = document_path.find('.docx')
if index2 != -1:
    txt_search(word_txt(document_path,output_path))
@app.route('/download')
def download():
    # 获取需要保存的数据（document_path、i和line）并进行处理
    data = ""  # 将需要保存的数据拼接成一个字符串
    file_name = "search_results.txt"  # 下载的文件名

    # 将数据保存到文件中
    with open(file_name, "w") as file:
        file.write(data)

    # 返回文件给用户下载
    return send_file(file_name, as_attachment=True)





if __name__ == '__main__':
    app.run()


