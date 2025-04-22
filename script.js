// 用于加载 txt 文件的函数
async function loadTextFile(url, blogContainerId, videoContainerId) {
    try {
        const response = await fetch(url);
        const text = await response.text();
        const lines = text.split('\n');
        
        const blogContainer = document.getElementById(blogContainerId);
        const videoContainer = document.getElementById(videoContainerId);
        
        // 遍历每一行，将内容添加到页面中
        lines.forEach(line => {
            if (line.trim()) {
                const parts = line.split('|');
                
                // 确保每行包含至少3部分
                if (parts.length >= 3) {
                    const type = parts[0].trim();  // "blog" 或 "video"
                    const url = parts[1].trim();
                    const title = parts[2].trim();
                    const description = parts.slice(3).join('|').trim();  // 处理描述部分
                    
                    // 创建链接元素
                    const a = document.createElement('a');
                    a.href = url;
                    a.textContent = title;
                    a.target = '_blank';
                    
                    // 创建描述元素
                    const p = document.createElement('p');
                    p.textContent = description;
                    
                    // 创建 div 容器
                    const div = document.createElement('div');
                    div.appendChild(a);
                    div.appendChild(p);
                    
                    // 根据类型添加到相应的容器
                    if (type === 'blog') {
                        blogContainer.appendChild(div);
                    } else if (type === 'video') {
                        videoContainer.appendChild(div);
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error loading file:', error);
    }
}

// 页面加载完成后加载博客和视频文件
window.onload = function () {
    loadTextFile('content.txt', 'blog-list', 'video-list');
}
