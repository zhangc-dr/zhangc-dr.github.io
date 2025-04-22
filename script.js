// 用于加载 txt 文件的函数
async function loadTextFile(url, containerId) {
    try {
        const response = await fetch(url);
        const text = await response.text();
        const lines = text.split('\n');
        const container = document.getElementById(containerId);
        
        // 遍历每一行，将内容添加到页面中
        lines.forEach(line => {
            if (line.trim()) {
                const parts = line.split('|');
                
                // 创建链接元素
                const a = document.createElement('a');
                a.href = parts[0];
                a.textContent = parts[1];
                a.target = '_blank';
                
                // 创建描述元素
                const p = document.createElement('p');
                p.textContent = parts[2];
                
                // 创建 div 容器
                const div = document.createElement('div');
                div.appendChild(a);
                div.appendChild(p);
                
                // 将内容添加到容器中
                container.appendChild(div);
            }
        });
    } catch (error) {
        console.error('Error loading file:', error);
    }
}

// 页面加载完成后加载博客和视频文件
window.onload = function () {
    loadTextFile('blogs.txt', 'blog-list');
    loadTextFile('videos.txt', 'video-list');
}
