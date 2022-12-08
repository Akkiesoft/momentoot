import urllib.request
import json
import sys
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

if len(sys.argv) < 1:
    print("usage: %s [opts] <URL list>"%sys.argv[0])
    sys.exit(1)

def generate_html(j):
    # ここでJSONをパースしてHTMLにする
    icon = j['account']['avatar']
    name_display = j['account']['display_name']
    name_acct = j['account']['acct']
    url_user = j['account']['url']
    url_status = j['url']
    created_at = j['created_at']
    content = j['content']
    # と思ったけど、jsonをそのままjinja2にぶんなげたら良いんじゃねってちょっと思った。
    # domainだけ追加してやりたいかも
    print(content)
    return content

html_body = ""

list_file = sys.argv[-1]
with open(list_file, 'r') as f:
    toot_urls = f.readlines()
for url in toot_urls:
    toot_url = url.replace("\n", "").split('/')
    json_url = "%s//%s/api/v1/statuses/%s" % (toot_url[0],toot_url[2],toot_url[4])
    with urllib.request.urlopen(json_url) as r:
        json_data = json.loads(r.read())
    html_body += generate_html(json_data)