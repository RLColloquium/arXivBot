import os
import re
from functools import lru_cache
# from pprint import PrettyPrinter
import requests
from slackbot.bot import listen_to
from arxiv import query


TRANSLATE_DEEPL_CACHE_MAXSIZE = 128 # TODO: optimize memory vs hits rate


# pp = PrettyPrinter(indent=4)

def is_valid_slack_user_id(user_id):
    # https://github.com/slackapi/slack-api-specs/blob/master/web-api/slack_web_openapi_v2.json
    # "defs_user_id": {
    #     "pattern": "^[UW][A-Z0-9]{2,}$",
    #     "title": "User ID",
    #     "type": "string"
    # },
    return re.match(r'^[UW][A-Z0-9]{2,20}$', user_id) # TODO: upper limit seeems like 10 but set it 20 for safety.

def get_deepl_auth_key(user_id):
    if is_valid_slack_user_id(user_id) and os.getenv('DEEPL_AUTH_KEY_'+user_id):
        # print('Found a user specific deepl auth key: {}'.format(user_id))
        return os.getenv('DEEPL_AUTH_KEY_'+user_id) # user specific auth key
    else:
        return os.getenv('DEEPL_AUTH_KEY') # default auth key
        # return None # or just reject

@lru_cache(maxsize=TRANSLATE_DEEPL_CACHE_MAXSIZE)
def translate_deepl(text, source_lang='EN', target_lang='JA', auth_key=None):
    # https://www.deepl.com/docs-api/translating-text/
    params = {
        'auth_key': auth_key,
        'text': text,
        'source_lang': source_lang,
        'target_lang': target_lang
    }
    r = requests.post('https://api.deepl.com/v2/translate', data=params)
    if r.status_code == requests.codes.ok: # TODO: only 200?
        j = r.json()
        # pp.pprint(j)
        params['auth_key'] = '*auth_key*' # hide auth_key in log
        print('DeepL API called: {}'.format([params, r.text]))
        return j['translations'][0]['text'] if 'translations' in j else None
    else:
        print('Failed to translate: {}'.format(r.text))
        return None

def generate_message(r, user_id):
    tags = ' | '.join(['{}'.format(t['term']) for t in r['tags']])
    u = r['updated_parsed']
    p = r['published_parsed']
    date = '{:04d}/{:02d}/{:02d}, {:04d}/{:02d}/{:02d}'.format(p.tm_year, p.tm_mon, p.tm_mday, u.tm_year, u.tm_mon, u.tm_mday)
    comment = r['arxiv_comment'] or ''
    arxiv_id = re.sub(r'https?://arxiv.org/abs/([0-9v\.]+)', r'\1', r['id'])
    arxiv_id_no_v = re.sub(r'v[0-9]+$', r'', arxiv_id)
    vanity = '<https://www.arxiv-vanity.com/papers/{}/|vanity>'.format(arxiv_id_no_v)
    img = '<http://www.arxiv-sanity.com/static/thumbs/{}.pdf.jpg|img>'.format(arxiv_id)
    summary = re.sub(r'\n', r' ', r['summary'])
    deepl_auth_key = get_deepl_auth_key(user_id)
    if deepl_auth_key:
        try:
            translation = translate_deepl(summary, auth_key=deepl_auth_key)
            summary = translation or summary
        except:
            print('Failed to translate: {}'.format(deepl_auth_key))
            pass
    lines = [
        # r['id'],
        re.sub(r'\n', r' ', r['title']),
        ', '.join(r['authors']),
        ', '.join([date, vanity, img, tags, comment]),
        summary,
    ]
    return '\n'.join(lines)


@listen_to('https?://arxiv.org/abs/([0-9v\.]+)')
def arxiv_abs(message, arxiv_id):
    rs = query(id_list=[arxiv_id])
    # pp.pprint(rs)
    if rs and len(rs) > 0:
        # message.send(generate_message(rs[0], user_id=message.user['id']))
        message.reply_webapi(generate_message(rs[0], user_id=message.user['id']), in_thread=True)
    else:
        message.send('No results found: ' + arxiv_id)
