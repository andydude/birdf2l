import sys
import json
from pandas import read_csv, DataFrame
from jinja2 import Environment, PackageLoader

ALG = read_csv("fixtures/alg.csv", dtype=str, keep_default_na=False)
PAT = read_csv("fixtures/pat.csv", dtype=str, keep_default_na=False)

ENV = Environment(
    loader=PackageLoader('birdf2l', 'templates'),
)


def render_pattern(pat):
    algtable = ALG[ALG.myposid == pat['shortid']].to_html()
    algtable = algtable.replace(
        'dataframe', 'dataframe table table-bordered table-hover')
    infotable = DataFrame([
        ('F2L', '<b>{}</b>'.format(pat['num'])),
        ('CubeFreak', '<samp>{}</samp>'.format(pat['cubefreak'])),
    ], dtype=str).to_html()
    infotable = infotable.replace(
        'dataframe', 'table table-small')
    infotable = infotable.replace(
        '&lt;', '<')
    infotable = infotable.replace(
        '&gt;', '>')
    template = ENV.get_template('pattern.html')
    s = template.render(
        algtable=algtable,
        infotable=infotable, **pat)
    return s
    
def main():
    pats = list(PAT.transpose().to_dict().values())
    content = ''
    for pat in pats:
        try:
            content += render_pattern(pat)
        except Exception as exc:
            print(repr(exc))
            
    template = ENV.get_template('base.html')
    page = template.render(content=content)
    print(page)


if __name__ == '__main__':
    main()
