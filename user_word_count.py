import optparse
parser = optparse.OptionParser()

parser.add_option("-u", action="store", type="string", dest="u")
parser.set_defaults(u="twitter")
opts, args = parser.parse_args()

if len(args)<1:
    print("Usage: user_word_count <config_file> [options]")
    raise SystemExit(1)

import twitter
import yaml

username = opts.u
configfile = args[0]

config = yaml.safe_load(open(configfile,'r'))

auth = twitter.oauth.OAuth(config['oauth_token'], \
                           config['oauth_token_secret'], \
                           config['consumer_key'], \
                           config['consumer_secret'])

twitter_api = twitter.Twitter(auth=auth)

kw = { 'count': 200, 'since_id':1, 'screen_name':username}

results = []
page_num = 1
max_page = 11
while page_num < max_page:
    tweets = twitter_api.statuses.user_timeline(**kw)
    if len(tweets) == 0:
        break
    results += tweets
    page_num += 1
    kw['max_id'] = min([tweet['id'] for tweet in tweets]) - 1

counts = {}
for tweet in results:
    text = tweet['text']
    words = text.split()
    for word in words:
        try:
            counts[word] += 1
        except KeyError:
            counts[word] = 1

sorted_counts = []
for word in counts:
    sorted_counts.append([word, counts[word]])

def compare_by_count(item):
    return item[1]

sorted_counts.sort(key=compare_by_count,reverse=True)

for item in sorted_counts:
    print(item[0], ":", item[1])

