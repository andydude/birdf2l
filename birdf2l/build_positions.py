import sys
import json
from pandas import read_csv, DataFrame
from jinja2 import Environment, PackageLoader
from .oll import ollid

ALG = read_csv("fixtures/alg.csv", dtype=str, keep_default_na=False)
PAT = read_csv("fixtures/pat.csv", dtype=str, keep_default_na=False)

ENV = Environment(
    loader=PackageLoader('birdf2l', 'templates'),
)


def render_position(pat, oll, pos):
    algtable = ALG[ALG.posid.map(lambda x: ollid(x) == oll['ollid'])].to_html()
    algtable = algtable.replace(
        'dataframe', 'dataframe table table-bordered table-hover')
    infotable = DataFrame([
        ('Orientation', '<samp>{}</samp>'.format(oll['ollid'])),
        ('Pattern', '<samp>{}</samp>'.format(pat['patid'])),
    ], dtype=str).to_html()
    infotable = infotable.replace(
        'dataframe', 'table table-small')
    infotable = infotable.replace(
        '&lt;', '<')
    infotable = infotable.replace(
        '&gt;', '>')
    template = ENV.get_template('position.html')
    context = {'stage': 'll'}
    context.update(pat)
    context.update(oll)
    #context.update(pos)
    s = template.render(
        algtable=algtable,
        infotable=infotable,
        **context)
    return s


def render_pattern(pat):
    content = ''
    poss = {}
    algs = list(ALG[ALG.patid == pat['patid']].transpose().to_dict().values())
    for alg in algs:
        posid = alg['posid']
        oll = ollid(posid)
        if oll not in poss:
            poss[oll] = {}
        poss[oll]['ollid'] = oll
        if not 'positions' in poss[oll]:
            poss[oll]['positions'] = []
        poss[oll]['positions'].append(posid)
    for oll, olld in sorted(poss.items()):
        try:
            content += render_position(pat, olld, olld['positions'][0])
        except Exception as exc:
            print(repr(exc))
            raise
    return content


def main():
    pat = {'patid': sys.argv[1]}
    content = render_pattern(pat)
    template = ENV.get_template('basevar.html')
    page = template.render(content=content)
    print(page)


if __name__ == '__main__':
    main()
