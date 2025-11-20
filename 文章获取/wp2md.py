import requests
import html2text
import os
import re
import uuid
from datetime import datetime
from urllib.parse import urlparse, urljoin
import shutil

# -------------------------- 所有可配置参数（集中在此处修改） --------------------------
CONFIG = {
    # WordPress域名（如https://blog.example.com）
    "WP_DOMAIN": "https://www.radiancecn.com/",
    # Markdown文件保存目录（如"wp_articles_md"）
    "SAVE_DIR": "wp_articles_md",
    # 图片保存目录（与SAVE_DIR同级，如"images"）
    "IMAGE_DIR": "images",
    # API相关配置（基于WP_DOMAIN自动生成，一般无需修改）
    "API_POSTS_URL": "",  # 自动生成：WP_DOMAIN + "/wp-json/wp/v2/posts"
    "API_BASE_URL": ""    # 自动生成：WP_DOMAIN + "/wp-json/wp/v2"
}
# ----------------------------------------------------------------------------------


def clean_filename(name):
    """处理文件名中的特殊字符，避免创建文件失败"""
    return re.sub(r'[\/:*?"<>|]', '_', name)


def extract_first_image(html_content, base_url):
    """从HTML内容中提取第一张图片的完整URL"""
    img_pattern = re.compile(r'<img[^>]+src=["\'](.*?)["\']', re.IGNORECASE)
    match = img_pattern.search(html_content)
    if match:
        img_url = match.group(1)
        # 处理相对路径图片
        return urljoin(base_url, img_url)
    return ""


def download_image(image_url, save_dir):
    """下载图片到本地images目录并返回本地文件名（确保不重复）"""
    if not image_url:
        return ""
    
    try:
        # 解析URL获取文件名和扩展名
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        
        # 如果没有扩展名，添加默认扩展名
        if not os.path.splitext(filename)[1]:
            filename += ".jpg"
        
        # 生成唯一文件名，避免重复
        unique_id = str(uuid.uuid4())[:8]
        name, ext = os.path.splitext(filename)
        unique_filename = f"{clean_filename(name)}_{unique_id}{ext}"
        file_path = os.path.join(save_dir, unique_filename)
        
        # 下载图片
        response = requests.get(image_url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            return unique_filename
        else:
            print(f"图片下载失败: {image_url}, 状态码: {response.status_code}")
            return ""
    except Exception as e:
        print(f"下载图片时出错: {str(e)}")
        return ""


def replace_image_links(html_content, original_url, local_filename, base_url, image_dir_relative):
    """替换HTML中的图片链接为相对路径（相对于Markdown文件）"""
    if not original_url or not local_filename:
        return html_content
    
    # 处理可能的URL变体（绝对路径和相对路径）
    absolute_url = urljoin(base_url, original_url)
    parsed_original = urlparse(absolute_url)
    variants = [
        original_url,
        absolute_url,
        f"{parsed_original.path}",
        f"{parsed_original.netloc}{parsed_original.path}"
    ]
    
    # 图片在Markdown中的相对路径（如"../images/xxx.jpg"）
    local_image_path = os.path.join(image_dir_relative, local_filename)
    for variant in variants:
        html_content = html_content.replace(variant, local_image_path)
    
    return html_content


def get_post_keywords(post_id, api_url):
    """获取文章的关键词（标签）"""
    try:
        tags_url = f"{api_url}/tags?post={post_id}"
        response = requests.get(tags_url)
        if response.status_code == 200:
            tags = response.json()
            return [tag['name'] for tag in tags]
    except Exception as e:
        print(f"获取关键词失败: {str(e)}")
    return []


def get_all_posts(api_url):
    """通过API获取所有文章（包含slug字段）"""
    all_posts = []
    page = 1
    
    while True:
        params = {
            "page": page,
            "per_page": 100,
            "status": "publish",
            "_fields": "id,title,content,published,link,excerpt,slug"  # 保留id用于获取标签（不显示）
        }
        response = requests.get(api_url, params=params)
        
        if response.status_code != 200:
            print(f"获取第{page}页失败，停止获取")
            break
        
        posts = response.json()
        if not posts:
            print("所有文章已获取完毕")
            break
        
        all_posts.extend(posts)
        print(f"已获取第{page}页，共{len(all_posts)}篇文章")
        page += 1
    
    return all_posts


def save_as_markdown(post, save_dir, image_dir, image_dir_relative, api_base, wp_domain, h):
    """将单篇文章转为Markdown并保存（移除id相关内容）"""
    # 提取文章基本信息（保留id用于获取标签，不显示）
    post_id = post.get("id")  # 仅用于内部获取标签，不对外显示
    title = post.get("title", {}).get("rendered", f"未命名文章")
    content_html = post.get("content", {}).get("rendered", "")
    publish_date = post.get("published", datetime.now().isoformat())
    link = post.get("link", "")
    post_slug = post.get("slug", "")  # 文章别名（用于url字段和文件名）
    
    # 提取描述（从摘要中获取）
    description = post.get("excerpt", {}).get("rendered", "")
    description = re.sub(r'<[^>]+>', '', description).strip()  # 去除HTML标签
    
    # 获取关键词（仍需post_id，仅内部使用）
    keywords = get_post_keywords(post_id, api_base) if post_id else []
    
    # 提取并下载第一张图片
    first_image_url = extract_first_image(content_html, wp_domain)
    local_image = download_image(first_image_url, image_dir)
    
    # 替换内容中的图片链接为相对路径
    if local_image:
        content_html = replace_image_links(
            html_content=content_html,
            original_url=first_image_url,
            local_filename=local_image,
            base_url=wp_domain,
            image_dir_relative=image_dir_relative
        )
    
    # HTML转Markdown
    content_md = h.handle(content_html)
    
    # 生成Markdown头部信息（已移除id字段）
    front_matter = f"""---
title: "{title}"
date: {publish_date}
keywords: {keywords if keywords else '[]'}
description: "{description}"
image: "{os.path.join(image_dir_relative, local_image) if local_image else ''}"
url: "{post_slug}"
draft: false
source: {link}
---

"""
    # 完整内容 = 头部信息 + 正文
    full_content = front_matter + content_md
    
    # 生成文件名（使用标题+slug确保唯一性，移除id）
    # 若slug为空，用uuid补充避免重复
    slug_suffix = clean_filename(post_slug) if post_slug else str(uuid.uuid4())[:8]
    filename = f"{clean_filename(title)}_{slug_suffix}.md"
    file_path = os.path.join(save_dir, filename)
    
    # 保存文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(full_content)
    print(f"已保存：{filename}")


if __name__ == "__main__":
    # 初始化配置（自动生成API地址）
    CONFIG["API_POSTS_URL"] = f"{CONFIG['WP_DOMAIN']}/wp-json/wp/v2/posts"
    CONFIG["API_BASE_URL"] = f"{CONFIG['WP_DOMAIN']}/wp-json/wp/v2"
    
    # 计算图片目录相对路径
    image_dir_relative = os.path.relpath(CONFIG["IMAGE_DIR"], CONFIG["SAVE_DIR"])
    
    # 初始化HTML转Markdown工具
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.images_to_alt = False
    h.body_width = 0
    h.skip_internal_links = True
    
    # 创建保存目录
    os.makedirs(CONFIG["SAVE_DIR"], exist_ok=True)
    os.makedirs(CONFIG["IMAGE_DIR"], exist_ok=True)
    print(f"Markdown保存目录：{os.path.abspath(CONFIG['SAVE_DIR'])}")
    print(f"图片保存目录：{os.path.abspath(CONFIG['IMAGE_DIR'])}")
    
    # 执行转换流程
    print("开始获取文章...")
    posts = get_all_posts(CONFIG["API_POSTS_URL"])
    print(f"共获取到{len(posts)}篇文章，开始转换为Markdown...")
    for post in posts:
        save_as_markdown(
            post=post,
            save_dir=CONFIG["SAVE_DIR"],
            image_dir=CONFIG["IMAGE_DIR"],
            image_dir_relative=image_dir_relative,
            api_base=CONFIG["API_BASE_URL"],
            wp_domain=CONFIG["WP_DOMAIN"],
            h=h
        )
    print(f"全部转换完成！Markdown文件在：{os.path.abspath(CONFIG['SAVE_DIR'])}")
    print(f"图片文件在：{os.path.abspath(CONFIG['IMAGE_DIR'])}")