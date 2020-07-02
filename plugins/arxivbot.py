import re
from pprint import PrettyPrinter
from slackbot.bot import listen_to
from arxiv import query

FIELDS = ['id', 'title', 'authors', 'date_tags_comment', 'summary']

pp = PrettyPrinter(indent=4)


def generate_message(r):
    tags = ' | '.join(['{}'.format(t['term']) for t in r['tags']])
    u = r['updated_parsed']
    p = r['published_parsed']
    date = '{:04d}/{:02d}/{:02d}, {:04d}/{:02d}/{:02d}'.format(p.tm_year, p.tm_mon, p.tm_mday, u.tm_year, u.tm_mon, u.tm_mday)
    comment = r['arxiv_comment'] or ''
    arxiv_id = re.sub(r'https?://arxiv.org/abs/([0-9v\.]+)', r'\1', r['id'])
    arxiv_id_no_v = re.sub(r'v[0-9]+$', r'', arxiv_id)
    vanity = '<https://www.arxiv-vanity.com/papers/{}/|vanity>'.format(arxiv_id_no_v)
    img = '<http://www.arxiv-sanity.com/static/thumbs/{}.pdf.jpg|img>'.format(arxiv_id)
    lines = [
        # r['id'],
        re.sub(r'\n', r' ', r['title']),
        ', '.join(r['authors']),
        ', '.join([date, vanity, img, tags, comment]),
        re.sub(r'\n', r' ', r['summary']),
    ]
    return '\n'.join(lines)

@listen_to('https?://arxiv.org/abs/([0-9v\.]+)')
def arxiv_abs(message, arxiv_id):
    rs = query(id_list=[arxiv_id])
    # pp.pprint(rs)
    if rs and len(rs) > 0:
        # message.send(generate_message(rs[0]))
        message.reply_webapi(generate_message(rs[0]), in_thread=True)
    else:
        message.send('No results found: ' + arxiv_id)
