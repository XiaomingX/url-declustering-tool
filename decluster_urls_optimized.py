from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
import re

def decluster_urls(input_urls):
    declustered_urls = []
    seen_paths = set()

    for url in input_urls:
        parsed_url = urlparse(url)
        
        # 强制将协议设为https，统一处理URL
        scheme = 'https'

        # 删除路径中多余的斜杠
        url_path = re.sub(r'/+', '/', parsed_url.path)

        # 跳过图片、JS、CSS等"无关"文件
        if url_path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.js', '.css', '.svg', '.ico')):
            continue

        # 跳过博客文章等人类写作的内容
        if re.search(r'/posts/|/blog/', url_path):
            continue

        # 跳过递增的页面URL，如 /page/1/ 和 /page/2/
        if re.search(r'/page/\d+/', url_path):
            continue

        # 标准化路径中带有可变数字ID的部分，例如 /cat/9/details.html
        url_path = re.sub(r'/cat/\d+/details\.html', '/cat/id/details.html', url_path)

        # 标准化日期格式，例如 /2021/08/01/ -> /yyyy/mm/dd/
        url_path = re.sub(r'/\d{4}/\d{2}/\d{2}/', '/yyyy/mm/dd/', url_path)

        # 标准化查询参数中的数字ID，例如 id=1
        query_params = parse_qs(parsed_url.query)
        if 'id' in query_params:
            query_params['id'] = ['id']  # 将id替换为通用标识符'id'

        # 删除不必要的查询参数，如跟踪参数
        unnecessary_params = ['utm_source', 'utm_medium', 'utm_campaign', 'ref', 'session_id', 'lang', 'sort', 'order']
        for param in unnecessary_params:
            query_params.pop(param, None)

        # 标准化分页参数，例如 page=2 -> page=page
        if 'page' in query_params:
            query_params['page'] = ['page']

        # 对查询参数按字母顺序排序，以减少不同顺序导致的重复
        sorted_query_params = {k: query_params[k] for k in sorted(query_params)}
        normalized_query = urlencode(sorted_query_params, doseq=True)

        # 标准化域名为小写
        netloc = parsed_url.netloc.lower()

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
        "http://example.com/?sort=asc&order=desc"
    ]

    declustered_urls = decluster_urls(input_urls)
    for url in declustered_urls:
        print(url)

if __name__ == "__main__":
    main()