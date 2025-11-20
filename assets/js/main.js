document.addEventListener('DOMContentLoaded', function() {
    // 移动端菜单切换
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
    
    // 搜索框显示/隐藏
    const searchToggle = document.getElementById('searchToggle');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchClose = document.getElementById('searchClose');
    
    if (searchToggle && searchOverlay) {
        searchToggle.addEventListener('click', function() {
            searchOverlay.classList.add('active');
        });
    }
    
    if (searchClose && searchOverlay) {
        searchClose.addEventListener('click', function() {
            searchOverlay.classList.remove('active');
        });
    }
    
    // 点击搜索框外部关闭搜索框
    if (searchOverlay) {
        searchOverlay.addEventListener('click', function(e) {
            if (e.target === searchOverlay) {
                searchOverlay.classList.remove('active');
            }
        });
    }
    
    // 导航栏滚动效果
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                // 向下滚动，隐藏导航栏
                navbar.classList.add('navbar-hidden');
            } else {
                // 向上滚动，显示导航栏
                navbar.classList.remove('navbar-hidden');
            }
            
            lastScrollTop = scrollTop;
        });
    }
    
    // 文章卡片悬停效果
    const articleCards = document.querySelectorAll('.article-card');
    
    articleCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('hovered');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('hovered');
        });
    });
    
    // 懒加载图片
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(function(img) {
            imageObserver.observe(img);
        });
    }
    
    // 分类按钮点击事件
    const categoryButtons = document.querySelectorAll('.category-btn');
    
    categoryButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 移除所有按钮的active类
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            
            // 为当前按钮添加active类
            this.classList.add('active');
            
            // 这里可以添加加载对应分类内容的逻辑
            // 例如AJAX请求或显示/隐藏对应的内容区域
        });
    });
    
    // 统计数字动画效果
    const statNumbers = document.querySelectorAll('.stat-number');
    
    function animateNumbers() {
        statNumbers.forEach(num => {
            const finalValue = num.innerText;
            let currentValue = 0;
            const increment = parseInt(finalValue) / 50;
            
            const timer = setInterval(() => {
                currentValue += increment;
                
                if (currentValue >= parseInt(finalValue)) {
                    num.innerText = finalValue;
                    clearInterval(timer);
                } else {
                    num.innerText = Math.floor(currentValue);
                }
            }, 30);
        });
    }
    
    // 当统计区域进入视口时触发动画
    if ('IntersectionObserver' in window && statNumbers.length > 0) {
        const statsSection = document.querySelector('.site-stats');
        
        if (statsSection) {
            const statsObserver = new IntersectionObserver(function(entries, observer) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        animateNumbers();
                        statsObserver.unobserve(entry.target);
                    }
                });
            });
            
            statsObserver.observe(statsSection);
        }
    }
    
    // 页脚显示控制
    updateFooterDisplay();
    window.addEventListener('resize', updateFooterDisplay);
    
    function updateFooterDisplay() {
        const width = window.innerWidth;
        const desktopFooter = document.getElementById('desktopFooter');
        const mobileFooter = document.getElementById('mobileFooter');
        const mobileCopyright = document.getElementById('mobileCopyright');
        
        if (width <= 768) {
            // 移动端：显示移动端元素
            if (desktopFooter) {
                desktopFooter.style.display = 'none';
            }
            if (mobileFooter) {
                mobileFooter.style.display = 'flex';
            }
            if (mobileCopyright) {
                mobileCopyright.style.display = 'block';
            }
        } else {
            // PC端：显示PC端元素
            if (desktopFooter) {
                desktopFooter.style.display = 'block';
            }
            if (mobileFooter) {
                mobileFooter.style.display = 'none';
            }
            if (mobileCopyright) {
                mobileCopyright.style.display = 'none';
            }
        }
    }
});