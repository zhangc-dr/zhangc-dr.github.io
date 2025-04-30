// log.js
document.addEventListener('DOMContentLoaded', () => {
  fetch('data/logs.json')
    .then(response => response.json())
    .then(data => {
      const logContent = document.getElementById('log-content');

      data.logs.forEach((log, index) => {
        const logItem = document.createElement('div');
        logItem.classList.add('log-item');
        
        // 根据奇偶索引，设置左右交错的卡片布局
        if (index % 2 === 0) {
          logItem.classList.add('left-card'); // 左侧卡片
        } else {
          logItem.classList.add('right-card'); // 右侧卡片
        }

        // 主体内容：日期 + 类型 + 标题 + 内容
        const logHeader = document.createElement('div');
        logHeader.classList.add('log-header');

        const logDate = document.createElement('h3');
        logDate.textContent = `📅 ${log.date}`;
        logHeader.appendChild(logDate);

        const logTypeTitle = document.createElement('p');
        logTypeTitle.innerHTML = `<strong>${log.type}：</strong><a href="${log.link}" target="_blank">${log.title}</a>`;
        logHeader.appendChild(logTypeTitle);

        const logContentText = document.createElement('p');
        logContentText.textContent = log.content;
        logHeader.appendChild(logContentText);

        logItem.appendChild(logHeader);

        // 添加点击事件跳转到独立页面
        logItem.addEventListener('click', () => {
          // 使用日志的唯一ID生成链接
          window.location.href = `logDetail.html?id=${log.id}`;
        });

        logContent.appendChild(logItem);
      });
    })
    .catch(error => {
      console.error('获取日志数据失败：', error);
    });
});
