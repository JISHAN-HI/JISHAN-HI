"""Read the public GitHub calendar; fail without overwriting on invalid responses."""
from html.parser import HTMLParser
from pathlib import Path
import datetime
import json
import urllib.request
import time

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'data-date' in a and 'data-level' in a:
            date = datetime.date.fromisoformat(a['data-date']).isoformat()
            level = int(a['data-level'])
            if level not in range(5):
                raise ValueError('Unexpected contribution level')
            self.days[date] = {'date': date, 'level': level}

url = 'https://github.com/users/JISHAN-HI/contributions'
for attempt in range(3):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'JISHAN-HI-profile-art', 'Accept': 'text/html'})
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode('utf-8')
        parser = Calendar()
        parser.feed(raw)
        days = sorted(parser.days.values(), key=lambda d: d['date'])
        if not 350 <= len(days) <= 380:
            raise ValueError(f'Unexpected calendar length: {len(days)}. GitHub markup may have changed.')
        dates = [datetime.date.fromisoformat(d['date']) for d in days]
        if any((b-a).days != 1 for a,b in zip(dates,dates[1:])):
            raise ValueError('Calendar dates are not contiguous')
        now = datetime.datetime.now(datetime.timezone.utc)
        if abs((now.date()-dates[-1]).days)>2:
            raise ValueError('Calendar is stale')
        payload={'username':'JISHAN-HI','updated':now.strftime('%Y-%m-%d'),'days':days}
        out=Path(__file__).resolve().parents[1]/'data/contributions.json'
        out.parent.mkdir(exist_ok=True)
        temp=out.with_suffix('.tmp')
        temp.write_text(json.dumps(payload,indent=2)+'\n')
        temp.replace(out)
        print(f'Fetched {len(days)} contribution days.')
        break
    except Exception:
        if attempt==2:
            raise
        time.sleep(2 ** attempt)
