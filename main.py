from functions import *

data = pd.read_csv('user_data.csv', delimiter=',')

group = data.groupby('ip', as_index=False).groups

prev = -1
session_id = 0
output = {}
for ip in group:
    prev = -1
    if (len(group[ip]) > 1):
        for idx in group[ip]:
            if (prev != -1):
                if (data.iloc[idx]['time'] - data.iloc[prev]['time'] < 1800):
                    output[session_id].append(data.iloc[idx])
                    prev = idx

                else:
                    session_id += 1
                    output[session_id] = [data.iloc[idx]]
                    prev = idx

            else:
                output[session_id] = [data.iloc[idx]]
                prev = idx
        session_id += 1


print(ua_category("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"))

print(ip_info('77.88.5.246'))

def sessions(group):
    prev = -1
    get_amount = 0
    session_id = 0
    output = {}
    if (len(group) > 1):
        for idx in group:
            if (prev != -1):
                if (data.iloc[idx]['time'] - data.iloc[prev]['time'] < 1800):
                    output[session_id].append(data.iloc[idx])
                    prev = idx

                else:
                    session_id += 1
                    output[session_id] = [data.iloc[idx]]
                    prev = idx

            else:
                output[session_id] = [data.iloc[idx]]
                prev = idx
        session_id += 1

    session_amount = len(output)
    avg_time = 0
    total_time = 0
    queries_amount = 0

    mean_time_gap = []
    avg_time_gap = []

    for key in output:
        arr = []
        for item in output[key]:
            arr.append(item['time'])

        time_gaps = []
        for n, x in enumerate(arr):
            time_gaps.append(arr[n] - arr[n - 1])

        time_gaps = time_gaps[1:]
        if (len(time_gaps) > 3):
            mean_time_gap.append(avg_ceil(time_gaps))
            temp = moving_avg(time_gaps, 3)
            avg_time_gap.append(avg_ceil(temp))
        else:
            mean_time_gap.append(0)
            avg_time_gap.append(0)
        # return time_gaps

    return [avg_ceil(mean_time_gap), avg_ceil(avg_time_gap), session_amount]

def analys(group):
    get = 0
    post = 0
    blocked = 0
    cookie = 0
    ua = ''
    ua_changed = -1
    ua_anal = 0
    lang = 0
    ru_lang = 0

    for idx in group:
        if (data.iloc[idx]['method'] == 'GET'):
            get += 1

        if (data.iloc[idx]['method'] == 'POST'):
            post += 1

        if (data.iloc[idx]['uri'] == '/.env'):
            blocked += 1

        if (data.iloc[idx]['cookie'] != 'NaN' and cookie == 0):
            cookie = 1

        if (data.iloc[idx]['lang'] != 'NaN' and lang == 0):
            lang = 1
            if isinstance(data.iloc[idx]['lang'], str):
                word = data.iloc[idx]['lang'].lower()
                regexp = re.compile('ru')
                if regexp.search(word):
                    ru_lang = 1

        if (ua != data.iloc[idx]['user-agent']):
            ua = data.iloc[idx]['user-agent']
            ua_changed += 1

    ua_anal = ua_category(ua)

    return [get, post, blocked, cookie, lang, ru_lang, ua_changed, ua_anal]

ip_data = [['ip', 'latitude', 'longitude', 'asn', 'proxy', 'queries_amount', 'mean_time_gap', 'avg_time_gap', 'session_amount', 'get', 'post', 'blocked', 'cookie', 'lang', 'ru_lang', 'ua_changed', 'ua_anal']]

for ip in group:
  if(len(group[ip]) > 1):
    [latitude, longitude, asn, proxy] = ip_info(ip)
    queries_amount = len(group[ip])
    [mean_time_gap, avg_time_gap, session_amount] = sessions(group[ip])
    [get, post, blocked, cookie, lang, ru_lang, ua_changed, ua_anal] = analys(group[ip])

    ip_data.append([ip, latitude, longitude, asn, proxy, queries_amount, mean_time_gap, avg_time_gap, session_amount, get, post, blocked, cookie, lang, ru_lang, ua_changed, ua_anal])

ip_df = pd.DataFrame(ip_data)

ip_df.to_csv('output.csv', header=False, index=False)