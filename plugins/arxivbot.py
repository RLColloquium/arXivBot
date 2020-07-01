import re
from pprint import PrettyPrinter
from slackbot.bot import listen_to
from arxiv import query

FIELDS = ['id', 'title', 'authors', 'date_tags_comment', 'summary']

pp = PrettyPrinter(indent=4)

@listen_to('https?://arxiv.org/abs/([0-9v\.]+)')
def arxiv_abs(message, arxiv_id):
    results = query(id_list=[arxiv_id])
    pp.pprint(results)
    if results and len(results) > 0:
        r = results[0]
        # r['id'] = re.sub('^http://', 'https://', r['id'])
        r['id'] = 'https://arxiv.org/abs/' + arxiv_id
        r['title'] = re.sub('\n', ' ', r['title'])
        r['authors'] = ', '.join(r['authors'])
        tags = ' | '.join([t['term'] for t in r['tags']])
        u = r['updated_parsed']
        p = r['published_parsed']
        date = '{}/{}/{}, {}/{}/{}'.format(p.tm_year, p.tm_mon, p.tm_mday, u.tm_year, u.tm_mon, u.tm_mday)
        comment = r['arxiv_comment']
        r['date_tags_comment'] = date + ', ' + tags + ', ' + comment
        r['summary'] = re.sub('\n', ' ', r['summary'])
        message.send('\n'.join([str(r[field]) for field in FIELDS]))
    else:
        message.send('No results found: ' + arxiv_id)
