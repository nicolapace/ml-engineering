
import datetime
import re

from functools import partial
from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin
from pathlib import Path

from utils.github_md_utils import md_header_to_anchor, md_process_local_links, md_expand_links, md_convert_md_target_to_html
from utils.build_utils import get_markdown_files

mdit = (
    MarkdownIt('commonmark', {'breaks':True, 'html':True})
    .use(anchors_plugin, max_level=7, permalink=False, slug_func=md_header_to_anchor)
    .enable('table')
)

my_repo_url = "https://github.com/stas00/ml-engineering/blob/master"

#md_expand_links_my_repo = partial(md_expand_links, repo_url=my_repo_url)

def convert_markdown_to_html(markdown_path):
    md_content = markdown_path.read_text()

    cwd_rel_path = markdown_path.parent
    # md_content = md_process_local_links(md_content, cwd_rel_path, md_expand_links_my_repo)
    # md_content = md_process_local_links(md_content, cwd_rel_path, md_convert_md_target_to_html)
    md_content = md_process_local_links(md_content, md_expand_links, cwd_rel_path=cwd_rel_path, repo_url=my_repo_url)
    md_content = md_process_local_links(md_content, md_convert_md_target_to_html)

    #tokens = mdit.parse(md_content)
    html_content = mdit.render(md_content)
    # we don't want <br />, since github doesn't use it in presentation
    html_content = re.sub('<br />', '', html_content)

    html_file = markdown_path.with_suffix(".html")
    html_file.write_text(html_content)

def make_cover_page_file(cover_md_file, date):
    with open(cover_md_file, "w") as f:
        f.write(f"""
## Machine Learning Engineering Open Book

This is a PDF version of [Machine Learning Engineering Open Book by Stas Bekman](https://github.com/stas00/ml-engineering/).

As this book is an early work in progress that gets updated frequently, if you downloaded it as a pdf file, chances are that it's already outdated - make sure to check the latest version at [https://github.com/stas00/ml-engineering](https://github.com/stas00/ml-engineering/).

This PDF was generated on {date}.
""")
    return Path(cover_md_file)

def write_html_index(html_chapters_file, markdown_files):
    html_chapters = [str(l.with_suffix(".html")) for l in markdown_files]
    html_chapters_file.write_text("\n".join(html_chapters))


if __name__ == "__main__":

    date = datetime.datetime.now().strftime("%Y-%m-%d")

    cover_md_file = "book-front.md"

    md_chapters_file = Path("chapters-md.txt")
    html_chapters_file = Path("chapters-html.txt")

    pdf_file = f"Stas Bekman - Machine Learning Engineering ({date}).pdf"

    markdown_files = [make_cover_page_file(cover_md_file, date)] + get_markdown_files(md_chapters_file)

    pdf_files = []
    for markdown_file in markdown_files:
        convert_markdown_to_html(markdown_file)

    write_html_index(html_chapters_file, markdown_files)
