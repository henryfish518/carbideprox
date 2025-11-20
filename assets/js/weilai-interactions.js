// Weilai主题交互效果
document.addEventListener('DOMContentLoaded', function() {
    
    // 导航栏滚动效果
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        lastScrollTop = scrollTop;
    });
    
    // 搜索框功能
    const searchToggle = document.getElementById('searchToggle');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchClose = document.getElementById('searchClose');
    const searchInput = document.querySelector('.search-input');
    
    if (searchToggle && searchOverlay) {
        searchToggle.addEventListener('click', function() {
            searchOverlay.classList.add('active');
            setTimeout(() => {
                searchInput.focus();
            }, 300);
        });
        
        searchClose.addEventListener('click', function() {
            searchOverlay.classList.remove('active');
        });
        
        // 点击遮罩层关闭搜索框
        searchOverlay.addEventListener('click', function(e) {
            if (e.target === searchOverlay) {
                searchOverlay.classList.remove('active');
            }
        });
        
        // ESC键关闭搜索框
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
                searchOverlay.classList.remove('active');
            }
        });
    }
    
    // 移动端菜单切换
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            
            // 汉堡菜单动画
            const spans = this.querySelectorAll('span');
            if (mobileMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
        
        // 点击菜单链接关闭菜单
        const mobileNavLinks = mobileMenu.querySelectorAll('a');
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.remove('active');
                const spans = mobileMenuToggle.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });
    }
    
    // Hero区域数字动画
    const statNumbers = document.querySelectorAll('.stat-number');
    
    function animateNumbers() {
        statNumbers.forEach(stat => {
            const target = parseInt(stat.getAttribute('data-target'));
            const increment = target / 100;
            let current = 0;
            
            const updateNumber = () => {
                if (current < target) {
                    current += increment;
                    stat.textContent = Math.ceil(current);
                    requestAnimationFrame(updateNumber);
                } else {
                    stat.textContent = target;
                    
                    // 如果是百分比数字，添加%
                    if (target === 99) {
                        stat.textContent = target + '%';
                    } else if (target === 75) {
                        stat.textContent = target + '%';
                    } else if (target === 60) {
                        stat.textContent = target + '%';
                    } else if (target === 45) {
                        stat.textContent = target + '%';
                    }
                }
            };
            
            updateNumber();
        });
    }
    
    // 使用Intersection Observer触发数字动画
    const heroStats = document.querySelector('.hero-stats');
    if (heroStats) {
        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateNumbers();
                    statsObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        statsObserver.observe(heroStats);
    }
    
    // 进度条动画
    const progressBars = document.querySelectorAll('.progress-bar');
    
    function animateProgressBars() {
        progressBars.forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0';
            
            setTimeout(() => {
                bar.style.width = width;
            }, 200);
        });
    }
    
    // 使用Intersection Observer触发进度条动画
    const trendsContainer = document.querySelector('.trends-container');
    if (trendsContainer) {
        const trendsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateProgressBars();
                    trendsObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });
        
        trendsObserver.observe(trendsContainer);
    }
    
    // 标签切换功能
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // 移除所有活动状态
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            // 添加当前活动状态
            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // 滚动显示动画
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // 为需要动画的元素添加观察
    const animatedElements = document.querySelectorAll('.category-card, .resource-card, .trend-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    // Hero搜索框建议功能
    const heroSearch = document.getElementById('hero-search');
    const suggestions = [
        '人工智能', '机器学习', '元宇宙', '区块链', 
        '量子计算', '自动驾驶', '生物科技', '云计算'
    ];
    
    if (heroSearch) {
        // 创建建议下拉框
        const suggestionsBox = document.createElement('div');
        suggestionsBox.className = 'search-suggestions-box';
        suggestionsBox.style.position = 'absolute';
        suggestionsBox.style.top = '100%';
        suggestionsBox.style.left = '0';
        suggestionsBox.style.width = '100%';
        suggestionsBox.style.maxHeight = '200px';
        suggestionsBox.style.overflowY = 'auto';
        suggestionsBox.style.background = 'var(--bg-secondary)';
        suggestionsBox.style.borderRadius = '0 0 20px 20px';
        suggestionsBox.style.zIndex = '100';
        suggestionsBox.style.display = 'none';
        
        heroSearch.parentNode.appendChild(suggestionsBox);
        
        heroSearch.addEventListener('input', function() {
            const value = this.value.toLowerCase();
            
            if (value.length > 0) {
                const filteredSuggestions = suggestions.filter(s => 
                    s.toLowerCase().includes(value)
                );
                
                if (filteredSuggestions.length > 0) {
                    suggestionsBox.innerHTML = '';
                    
                    filteredSuggestions.forEach(suggestion => {
                        const item = document.createElement('div');
                        item.textContent = suggestion;
                        item.style.padding = '10px 20px';
                        item.style.cursor = 'pointer';
                        item.style.transition = 'background 0.2s';
                        
                        item.addEventListener('mouseenter', function() {
                            this.style.background = 'rgba(122, 92, 255, 0.1)';
                        });
                        
                        item.addEventListener('mouseleave', function() {
                            this.style.background = 'transparent';
                        });
                        
                        item.addEventListener('click', function() {
                            heroSearch.value = suggestion;
                            suggestionsBox.style.display = 'none';
                        });
                        
                        suggestionsBox.appendChild(item);
                    });
                    
                    suggestionsBox.style.display = 'block';
                } else {
                    suggestionsBox.style.display = 'none';
                }
            } else {
                suggestionsBox.style.display = 'none';
            }
        });
        
        // 点击外部关闭建议框
        document.addEventListener('click', function(e) {
            if (!heroSearch.contains(e.target) && !suggestionsBox.contains(e.target)) {
                suggestionsBox.style.display = 'none';
            }
        });
    }
    
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const navbarHeight = navbar.offsetHeight;
                const targetPosition = targetElement.offsetTop - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // 粒子背景效果（使用简单的CSS动画代替particles.js）
    const heroParticles = document.querySelector('.hero-particles');
    if (heroParticles) {
        // 创建粒子
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.style.position = 'absolute';
            particle.style.width = Math.random() * 4 + 'px';
            particle.style.height = particle.style.width;
            particle.style.background = 'rgba(122, 92, 255, 0.6)';
            particle.style.borderRadius = '50%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.opacity = Math.random() * 0.5 + 0.2;
            
            // 随机动画
            const duration = Math.random() * 50 + 20;
            const delay = Math.random() * 5;
            
            particle.style.animation = `float ${duration}s ${delay}s infinite alternate ease-in-out`;
            
            heroParticles.appendChild(particle);
        }
        
        // 添加浮动动画
        const style = document.createElement('style');
        style.textContent = `
            @keyframes float {
                0% { transform: translateY(0) translateX(0); }
                33% { transform: translateY(-20px) translateX(10px); }
                66% { transform: translateY(10px) translateX(-10px); }
                100% { transform: translateY(-10px) translateX(5px); }
            }
        `;
        document.head.appendChild(style);
    }
});