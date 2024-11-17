from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
import re

def decluster_urls(input_urls):
    declustered_urls = []
    seen_paths = set()

    for url in input_urls:
        parsed_url = urlparse(url)
        
        # 强制将协议设为https，统一处理URL
        scheme = 'https'

        # 删除路径中多余的斜杠，并标准化index.html为根路径
        url_path = re.sub(r'/+', '/', parsed_url.path).rstrip('/')
        if url_path.endswith('/index.html'):
            url_path = url_path[:-11]  # 移除 /index.html，保留根路径

        # 跳过图片、JS、CSS等"无关"文件
        if url_path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.js', '.css', '.svg', '.ico', '.webp', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.avi', '.mp3')):
            continue

        # 跳过博客文章等人类写作的内容
        if re.search(r'/posts/|/blog/', url_path):
            continue

        # 跳过递增的页面URL，如 /page/1/ 和 /page/2/
        if re.search(r'/page/\d+/', url_path):
            continue

        # 标准化路径中带有可变数字ID的部分，例如 /cat/9/details.html 或 /item/123/details
        url_path = re.sub(r'/(cat|item|user)/\d+/(details|profile)\.html?', r'/\1/id/\2.html', url_path)

        # 标准化日期格式，例如 /2021/08/01/ 或 /2021-08-01/
        url_path = re.sub(r'/\d{4}/\d{2}/\d{2}/', '/yyyy/mm/dd/', url_path)
        url_path = re.sub(r'/\d{4}-\d{2}-\d{2}/', '/yyyy-mm-dd/', url_path)
        url_path = re.sub(r'/\d{4}-\d{2}-\d{2}_to_\d{4}-\d{2}-\d{2}/', '/yyyy-mm-dd_to_yyyy-mm-dd/', url_path)

        # 标准化路径中的语言标识，例如 /en/ 或 /zh/
        url_path = re.sub(r'^/(en|zh|fr|de|es|ru)/', '/lang/', url_path)

        # 删除路径中的版本号，例如 /v1.0.0/ 或 /v2/
        url_path = re.sub(r'/v\d+(\.\d+)*', '/version', url_path)

        # 标准化 UUID 或 GUID，例如 /user/123e4567-e89b-12d3-a456-426614174000/
        url_path = re.sub(r'/[a-f0-9\-]{36}/', '/uuid/', url_path)

        # 标准化路径中的文件名扩展后缀
        url_path = re.sub(r'\.(php|asp|aspx)$', '.html', url_path)

        # 标准化路径中的类别标识等信息
        url_path = re.sub(r'/category/[^/]+/', '/category/category/', url_path)

        # 标准化产品SKU，例如 /product/sku/abc123/
        url_path = re.sub(r'/product/sku/[^/]+/', '/product/sku/sku/', url_path)

        # 删除重复的子路径，例如 /path/path/
        url_path = re.sub(r'(/\w+)/\1/', r'\1/', url_path)

        # 标准化 IP 地址为通用标识符，例如 /192.168.1.1/ -> /ip-address/
        url_path = re.sub(r'/\d{1,3}(\.\d{1,3}){3}/', '/ip-address/', url_path)

        # 标准化电子邮件标识符，例如 /user/email@example.com/ -> /user/email/
        url_path = re.sub(r'/[\w\.-]+@[\w\.-]+\.[a-z]{2,}/', '/email/', url_path)

        # 标准化查询参数中的数字ID，例如 id=1
        query_params = parse_qs(parsed_url.query)
        if 'id' in query_params:
            query_params['id'] = ['id']  # 将id替换为通用标识符'id'

        # 删除不必要的查询参数，如跟踪参数
        unnecessary_params = ['utm_source', 'utm_medium', 'utm_campaign', 'ref', 'session_id', 'lang', 'sort', 'order', 'fbclid', 'gclid', 'tracking_id', 'version', 'token', 'session']
        for param in unnecessary_params:
            query_params.pop(param, None)

        # 标准化分页参数，例如 page=2 -> page=page
        if 'page' in query_params:
            query_params['page'] = ['page']

        # 标准化 offset 和 limit 参数
        if 'offset' in query_params:
            query_params['offset'] = ['offset']
        if 'limit' in query_params:
            query_params['limit'] = ['limit']

        # 标准化带有布尔值的查询参数值
        for key, value in query_params.items():
            if value == ['true'] or value == ['false']:
                query_params[key] = ['bool']

        # 标准化时间戳参数，例如 timestamp=1622470400 -> timestamp=ts
        if 'timestamp' in query_params:
            query_params['timestamp'] = ['ts']

        # 删除空查询参数
        query_params = {k: v for k, v in query_params.items() if v != ['']}

        # 对查询参数按字母顺序排序，以减少不同顺序导致的重复
        sorted_query_params = {k: query_params[k] for k in sorted(query_params)}
        normalized_query = urlencode(sorted_query_params, doseq=True)

        # 标准化域名为小写并移除www前缀
        netloc = parsed_url.netloc.lower()
        if netloc.startswith('www.'):
            netloc = netloc[4:]

        # 删除URL中的fragment（#部分）
        fragment = ''

        # 组合协议、域名、路径和规范化后的查询参数生成标准化URL
        normalized_url = urlunparse((
            scheme,
            netloc,
            url_path,
            parsed_url.params,
            normalized_query,
            fragment
        ))

        # 如果此标准化路径已记录，跳过该URL
        if normalized_url not in seen_paths:
            seen_paths.add(normalized_url)
            declustered_urls.append(url)

    return declustered_urls

def main():
    input_urls = [
        "http://example.com/page.php?id=1",
        "https://example.com/page.php?id=1",
        "http://example.com//page.php?id=2",
        "http://example.com/page.php?id=3&page=2",
        "http://example.com/cat/9/details.html",
        "http://example.com/cat/11/details.html",
        "http://example.com/blog/why-people-suck-a-study",
        "http://example.com/blog/how-to-lick-your-own-toes",
        "http://example.com/banner.jpg",
        "http://example.com/assets/background.jpg",
        "http://example.com/page/1/",
        "http://example.com/page/2/",
        "http://example.com/posts/a-brief-history-of-time",
        "http://example.com/?utm_source=google&utm_medium=cpc",
        "http://example.com/?ref=affiliate",
        "http://example.com/page.php?id=1&session_id=12345",
        "http://example.com/2021/08/01/article-title",
        "http://example.com/2021-08-01/article-title",
        "http://example.com/?sort=asc&order=desc",
        "http://example.com/?fbclid=XYZ123",
        "http://example.com/user/456/profile.html",
        "http://www.example.com/lang/en/page.php",
        "http://example.com/v1.0.0/resource",
        "http://example.com/user/123e4567-e89b-12d3-a456-426614174000/profile.html",
        "http://example.com/192.168.1.1/details",
        "http://example.com/user/email@example.com"
    ]

    declustered_urls = decluster_urls(input_urls)
    for url in declustered_urls:
        print(url)

if __name__ == "__main__":
    main()
