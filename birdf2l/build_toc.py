import sys
import json
from pandas import read_csv, DataFrame
from jinja2 import Environment, PackageLoader

ENV = Environment(
    loader=PackageLoader('birdf2l', 'templates'),
)

def main():
    navbar = ENV.get_template('navbar.html').render()
    
    with open("index.html", "w") as writer:
        try:
            template = ENV.get_template('baseidx.html')
            page = template.render(navbar=navbar)
            writer.write(page)
        except Exception as exc:
            print(repr(exc))
            pass
    
    with open("app/index.html", "w") as writer:
        try:
            template = ENV.get_template('basetoc.html')
            page = template.render(navbar=navbar)
            writer.write(page)
        except Exception as exc:
            print(repr(exc))
            pass

        
if __name__ == '__main__':
    main()
