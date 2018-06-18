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
    algtable = ALG[ALG.patid == pat['patid']].to_html()
    algtable = algtable.replace(
        'dataframe', 'dataframe table table-bordered table-hover')
    infotable = []
    if pat['num']:
        infotable += [('F2L', pat['num'])]
    if pat['cubefreak']:
        infotable += [('CubeFreak', pat['cubefreak'])]
    if pat['mirpatid']:
        infotable += [('Mirror',
            '<a href="{0}.html">{0}</a>'.format(pat['mirpatid']))]
    infotable = DataFrame(infotable, dtype=str).to_html()
    infotable = infotable.replace(
        'dataframe', 'table table-small')
    infotable = infotable.replace(
        '&lt;', '<')
    infotable = infotable.replace(
        '&gt;', '>')
    template = ENV.get_template('pattern.html')
    context = {'stage': 'f2l'}
    context.update(pat)
    s = template.render(
        algcol=10,
        algtable=algtable,
        infotable=infotable,
        **context)
    return s


def main():
    navbar = ENV.get_template('navbar.html').render()
    pats = list(PAT.transpose().to_dict().values())
    
    for pat in pats:
        with open("app/" + pat['patid'] + ".html", "w") as writer:
            try:
                content = render_pattern(pat)
                template = ENV.get_template('base.html')
                page = template.render(content=content, navbar=navbar)
                writer.write(page)
            except Exception as exc:
                print(repr(exc))
                pass

        
if __name__ == '__main__':
    main()
