import re
import requests
import click
import bs4
from flask import Flask
from urllib.parse import urljoin


def main(URL, LEN_SYMBOLS):
    app = Flask(__name__)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def proxy(path):
        return change_page(path)

    def change_page(path):
        pattern = "(\w{%s,})" % LEN_SYMBOLS
        symbol = "™"
        response = requests.get(urljoin(URL, path))
        page = bs4.BeautifulSoup(response.content, "lxml")
        body = page.find("body")
        for a in body.find_all(text=True):
            if a:
                new_text = re.sub(pattern, r"\1" + symbol, a)
                a.replace_with(new_text)
        return page.prettify()

    app.run()


@click.command()
@click.option("--len_symbols", "-l", default=10)
@click.option("--url", "-u", default="https://example.com")
def enter_point(url, len_symbols,):
    main(url, len_symbols)


if __name__ == "__main__":
    enter_point()
