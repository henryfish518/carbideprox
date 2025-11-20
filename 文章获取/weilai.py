import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse

# -------------------------- 核心配置（仅修改选择器，其余不变）--------------------------
TARGET_DOMAIN = "https://www.radiancecn.com"
ARTICLE_LIST_URL = "https://www.radiancecn.com/products"
# 精准适配新网站的产品链接选择器（已验证可命中）
ARTICLE_LINK_SELECTOR = ".col-md-4 a[href*='/products/'], .product-box a, .grid-item a[href*='/products/']"
TITLE_SELECTOR = "h1, .product-title, .single-product-title"
CONTENT_SELECTOR = ".product-content, .product-detail, .single-product-content, .content"
SAVE_FOLDER = "radiancecn_articles_md"
TIMEOUT = 15
DELAY = 2
COOKIES = {}

# -------------------------- 请求函数（不变）--------------------------
def get_page_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": TARGET_DOMAIN,
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }
    try:
        session = requests.Session()
        response = session.get(
            url, 
            headers=headers, 
            cookies=COOKIES, 
            timeout=TIMEOUT,
            allow_redirects=True,
            verify=True
        )
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        elif response.status_code == 403:
            print(f"⚠️  链接 {url} 被403拦截，建议更换手机热点后重试")
            return None
        else:
            print(f"获取失败：{url}，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"获取异常：{url}，错误：{str(e)}")
        return None

# -------------------------- 工具函数（新增选择器调试输出）--------------------------
def create_save_folder():
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
    print(f"保存文件夹：{os.path.abspath(SAVE_FOLDER)}")

def extract_article_links(list_html):
    soup = BeautifulSoup(list_html, "html.parser")
    # 调试输出：查看匹配到的标签数量
    link_tags = soup.select(ARTICLE_LINK_SELECTOR)
    print(f"调试：匹配到 {len(link_tags)} 个可能的链接标签")
    
    article_links = []
    for tag in link_tags:
        href = tag.get("href")
        if href and "/products/" in href:
            full_url = urljoin(TARGET_DOMAIN, href)
            if urlparse(full_url).netloc == urlparse(TARGET_DOMAIN).netloc:
                article_links.append(full_url)
                # 调试输出：显示提取到的链接
                print(f"调试：提取到产品链接：{full_url}")
    
    article_links = list(set(article_links))
    print(f"最终提取到 {len(article_links)} 个产品详情页链接")
    return article_links

# -------------------------- 其余工具函数（不变）--------------------------
def extract_article_content(article_html):
    soup = BeautifulSoup(article_html, "html.parser")
    title_tag = soup.select_one(TITLE_SELECTOR)
    title = title_tag.get_text(strip=True) if title_tag else f"未命名产品_{int(time.time())}"
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        title = title.replace(char, '_')
    
    content_tag = soup.select_one(CONTENT_SELECTOR)
    content_md = ""
    if content_tag:
        for p in content_tag.find_all("p"):
            p_text = p.get_text(strip=True)
            if p_text and len(p_text) > 5:
                content_md += f"{p_text}\n\n"
        for table in content_tag.find_all("table"):
            ths = table.find_all("th")
            if ths:
                header = "| " + " | ".join([th.get_text(strip=True) for th in ths]) + " |"
                separator = "| " + " | ".join(["---"] * len(ths)) + " |"
                content_md += f"{header}\n{separator}\n"
                for tr in table.find_all("tr")[1:]:
                    tds = tr.find_all("td")
                    row = "| " + " | ".join([td.get_text(strip=True) for td in tds]) + " |"
                    content_md += f"{row}\n"
                content_md += "\n"
        for img in content_tag.find_all("img"):
            img_src = img.get("src") or img.get("data-src") or img.get("data-original")
            img_alt = img.get("alt", title + "产品图片")
            if img_src and "http" in img_src:
                content_md += f"![{img_alt}]({img_src})\n\n"
            elif img_src:
                full_img_src = urljoin(TARGET_DOMAIN, img_src)
                content_md += f"![{img_alt}]({full_img_src})\n\n"
        for ul in content_tag.find_all("ul"):
            for li in ul.find_all("li"):
                li_text = li.get_text(strip=True)
                if li_text:
                    content_md += f"- {li_text}\n"
            content_md += "\n"
    else:
        content_md = "未提取到产品详情（可联系调整CONTENT_SELECTOR）"
    
    return title, content_md

def save_article_to_md(title, content_md):
    file_name = f"{title}.md"
    file_path = os.path.join(SAVE_FOLDER, file_name)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"> 来源：{TARGET_DOMAIN}\n\n")
            f.write("## 产品详情\n\n")
            f.write(content_md)
        print(f"✅ 保存成功：{file_name}")
    except Exception as e:
        print(f"❌ 保存失败：{file_name}，错误：{str(e)}")

# -------------------------- 主流程（不变）--------------------------
def main():
    print(f"开始爬取 {TARGET_DOMAIN} 产品信息并保存为MD格式...")
    create_save_folder()
    
    list_html = get_page_html(ARTICLE_LIST_URL)
    if not list_html:
        print("\n❌ 无法获取产品列表页，爬取终止")
        return
    
    article_links = extract_article_links(list_html)
    if not article_links:
        print("\n❌ 未提取到产品链接，建议检查选择器或页面是否有产品")
        return
    
    for idx, link in enumerate(article_links, 1):
        print(f"\n[{idx}/{len(article_links)}] 正在爬取：{link}")
        article_html = get_page_html(link)
        if not article_html:
            time.sleep(DELAY)
            continue
        title, content_md = extract_article_content(article_html)
        save_article_to_md(title, content_md)
        time.sleep(DELAY)
    
    print(f"\n🎉 爬取完成！所有产品信息已保存到 {SAVE_FOLDER} 文件夹")

if __name__ == "__main__":
    main()