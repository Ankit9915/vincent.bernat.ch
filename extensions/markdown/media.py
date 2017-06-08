"""Support more media for the ![]() image syntax.

Currently, we only support Youtube videos using:

    ![](youtube:xxxxx)
"""

from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.inlinepatterns import LinkPattern
from markdown.util import AtomicString, etree

YOUTUBE_RE = r'\!\[\]\(youtube:([\w-]+)\)'


class YoutubePattern(LinkPattern):
    def handleMatch(self, m):
        id = m.group(2)
        outer = etree.Element("div")
        outer.set('class', 'lf-video-outer')
        inner = etree.SubElement(outer, "div")
        inner.set('class', 'lf-video-inner')
        a = etree.SubElement(inner, "a")
        a.set('class', 'lf-video')
        a.set('href', 'https://www.youtube.com/watch?v={}'.format(id))
        a.set('title', 'YouTube video #{}'.format(id))
        a.text = AtomicString('YouTube video #{}'.format(id))
        button = etree.SubElement(a, "div")
        button.set('class', 'lf-video-play-button')
        return outer


class YoutubeProcessor(Treeprocessor):

    def run(self, node):
        for idx, child in enumerate(node):
            if child.tag == 'p' and \
               len(child) == 1 and \
               child[0].tag == "div" and \
               child[0].attrib['class'] == "lf-video-outer":
                node.remove(child)
                node.insert(idx, child[0])


class MediaExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('youtube-link',
                              YoutubePattern(YOUTUBE_RE),
                              '<image_link')
        md.treeprocessors.add('youtube-link', YoutubeProcessor(), '_end')


def makeExtension(*args, **kwargs):
    return MediaExtension(*args, **kwargs)
