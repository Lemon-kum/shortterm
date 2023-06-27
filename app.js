let indexedFiles = [];
let selectedResults = [];

// 建立索引
function indexFiles(files) {
    indexedFiles = [];
    //对pdf和word文档建立索引
    for (let i = 0; i < files.length; i++) {
    const file = files[i];
    if (file.name.endsWith('.pdf') || file.name.endsWith('.doc') || file.name.endsWith('.docx')) {
        indexedFiles.push(file);
    }
    }
    
    console.log('已建立索引的文件：', indexedFiles);
}

// 搜索文件
function searchFiles() {
    const keyword = document.getElementById('keyword').value;
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';
    
    if (keyword.trim().length === 0) {
    alert("请输入要查询的关键字！")
    return;
    }
    
    //在文件名索引中搜索包含关键字的文件名
    const matchedFiles = indexedFiles.filter(file => file.name.toLowerCase().includes(keyword.toLowerCase()));
    
    //将符合条件的文件生成可选项
    for (let i = 0; i < matchedFiles.length; i++) {
    const li = document.createElement('li');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.value = matchedFiles[i].name;
    checkbox.addEventListener('change', function() {
        if (this.checked) {
        selectedResults.push(this.value);
        } else {
        const index = selectedResults.indexOf(this.value);
        if (index > -1) {
            selectedResults.splice(index, 1);
        }
        }
    });
    
    li.appendChild(checkbox);
    li.appendChild(document.createTextNode(matchedFiles[i].name));
    resultsContainer.appendChild(li);
    }
}

// 保存选中结果到文本并下载
function saveSelectedResults() {

    //如果未选择下载文件则输出提示
    if (selectedResults.length === 0) {
    alert("请选择下载内容！");
    return;
    }

    //定义保存下载文件的TXT文件
    const filename = 'selected_results.txt';
    let content = '';
    
    for (let i = 0; i < selectedResults.length; i++) {
    content += selectedResults[i] + '\n';
    }
    
    const element = document.createElement('a');
    element.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(content);
    element.download = filename;
    element.style.display = 'none';
    document.body.appendChild(element);
    
    element.click();
    
    document.body.removeChild(element);
}

//将查询目录下的文件存入数组files
const folderInput = document.getElementById('folder');
folderInput.addEventListener('change', function() {
    const files = Array.from(folderInput.files);
    indexFiles(files);
});