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

toots = []

list_file = sys.argv[-1]
with open(list_file, 'r') as f:
    toot_data = f.readlines()

info = {
    'title': toot_data[0].replace("\n", ""),
    'description': toot_data[1].replace("\n", ""),
    'author_icon': toot_data[2].replace("\n", ""),
    'author_url': toot_data[3].replace("\n", ""),
    'author': toot_data[4].replace("\n", ""),
    'last_update': toot_data[5].replace("\n", ""),
}

for url in toot_data[6:]:
    toot_url = url.replace("\n", "").split('/')
    json_url = "%s//%s/api/v1/statuses/%s" % (toot_url[0],toot_url[2],toot_url[4])
    with urllib.request.urlopen(json_url) as r:
        toots.append({"toot":json.loads(r.read()), "domain":toot_url[2]})

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
template = env.get_template("template.html")

ticket = template.render(info=info, toots=toots)
with open("out.html", "w") as f:
    f.write(ticket)

#from jinja2 import Environment, PackageLoader, select_autoescape
#env = Environment(
#    loader=PackageLoader("yourapp"),
#    autoescape=select_autoescape())
