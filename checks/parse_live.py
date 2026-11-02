"""The source page's 'Wall time against mibz2' table, independently of the presentation's JS:
the first <table> after <h2 id="wall-time-against-mibz2"> and before the next <h2>."""
import re, html, json, sys
s = open(sys.argv[1]).read()
a = re.search(r'<h2 id="wall-time-against-mibz2"', s).start()
b = s.find('<h2', a + 10)
sec = s[a:b]
text = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip()
t = sec[sec.index('<table'):sec.index('</table>')]
heads = [text(h) for h in re.findall(r'<th[^>]*>(.*?)</th>', t[:t.index('</thead>')], re.S)]
rows = [[text(c) for c in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)] for r in re.findall(r'<tr>(.*?)</tr>', t[t.index('<tbody'):], re.S)]
print('BEFORE TABLE:', text(sec[:sec.index('<table')])[:1200])
print('AFTER TABLE:', text(sec[sec.index('</table>'):])[:1500])
json.dump({'heads': heads, 'rows': rows}, open('data/live-wall.json', 'w'), ensure_ascii=False, indent=0)
print(heads); [print(' | '.join(r)) for r in rows]
