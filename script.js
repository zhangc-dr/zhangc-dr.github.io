<script>
    async function loadTextFile(url, blogContainerId, videoContainerId) {
        try {
            const response = await fetch(url);
            const text = await response.text();
            const lines = text.split('\n');

            const blogContainer = document.getElementById(blogContainerId);
            const videoContainer = document.getElementById(videoContainerId);

            lines.forEach(line => {
                if (line.trim()) {
                    const parts = line.split('|');
                    if (parts.length >= 3) {
                        const type = parts[0].trim();
                        const url = parts[1].trim();
                        const title = parts[2].trim();
                        const description = parts.slice(3).join('|').trim();

                        const a = document.createElement('a');
                        a.href = url;
                        a.textContent = title;
                        a.target = '_blank';

                        const p = document.createElement('p');
                        p.textContent = description;

                        const div = document.createElement('div');
                        div.className = 'post';
                        div.appendChild(a);
                        div.appendChild(p);

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

    function showTab(tabId) {
        const tabs = document.querySelectorAll('.tab-content');
        tabs.forEach(tab => {
            tab.style.display = 'none';
        });
        document.getElementById(tabId).style.display = 'block';
    }

    window.onload = function () {
        loadTextFile('content.txt', 'blog-list', 'video-list');
        showTab('blog-list');
    };
</script>
