from langchain_core.documents import Document
from bs4 import BeautifulSoup
from .tag import Tag
from typing import Optional
from .utils import get_minified_soup, find_article_in_soup
from lxml import etree


def get_contentful_nodes(soup, *, contentful_length=500, min_contentful_sentence_length=50, min_contentful_sentences=3):
    # text of self and all child
    texts = soup.get_text(strip=True)
    # text of self only
    only_direct_texts = soup.find(text=True)
    # check is this dom a complete sentence (by length)
    is_an_acceptable_sentence = len(only_direct_texts) < min_contentful_sentence_length
    # non meaningful, if no content
    if len(texts) < contentful_length: return None

    # is meaningful, but it may be a parent, you need to check all the child
    child_list = soup.find_all(recursive=False)

    # not meaningful, if it is not enough length for a sentence, and if it does not have a child
    if not is_an_acceptable_sentence and len(child_list) == 0: return None

    # print(f"has {len(child_list)} child")
    found_contentful_child_list = []
    for child in child_list:
        contentful = get_contentful_nodes(child)
        if contentful is not None:
            found_contentful_child_list.append(contentful)
    print("found_contentful_child_list: ", found_contentful_child_list)
    # print("found_contentful_child_list: ", found_contentful_child_list)
    if len(found_contentful_child_list) == 0 or len(found_contentful_child_list) >= min_contentful_sentences:
        # self is contentful, but non is child is contentful, then, I AM the contentful node
        # or more than $min_contentful_sentences child is contentful, then, I AM the contentful node
        return soup
    if len(found_contentful_child_list) == 1:
        # only 1 child is contentful, then this child is the contentful node
        return found_contentful_child_list[0]
    return None


def auto_load_meaningful_content(html: str) -> Document:
    """Auto-detect the major content part
    will try to exclude menu data and footer data
    do its best to keep the contentful body


    Rules:
    normally, major content will be wrap in a parallel structure
    <div>
        <p>major content...</p>
        <p>major content...</p>
        <p>major content...</p>
    </div>
    Therefore, we need to find parallel content
    """

    soup = BeautifulSoup(html, 'html.parser')
    soup, tag = find_article_in_soup(soup)
    if tag == "article" or tag == "main":
        # Found article or main, proceed directly
        return Document(page_content=soup.get_text(),
                        metadata={
                            "feature": "autoload",
                            "is_contentful": True,
                            "article_detected": True,
                            "images_loaded": None
                        })

    # use a fallback method
    soup = get_minified_soup(soup)

    # build an HTML Tag tree
    t = Tag.from_soup(soup)
    contentful = t.get_contentful_tag()
    contentful_text = contentful.get_contentful_tag_texts()

    # if the contentful text is too short, maybe we have done something wrong
    if len(contentful_text) < 500:  # less than a normal article, we will use original text
        return Document(page_content=soup.get_text(strip=True), metadata={
            "feature": "autoload",
            "is_contentful": False,
            "article_detected": False,
            "images_loaded": None
        })
    # use the contentful text
    return Document(
        page_content=contentful_text,
        metadata={
            "feature": "autoload",
            "is_contentful": True,
            "article_detected": False,
            "images_loaded": None
        }
    )


def xpath_load_meaningful_content(html: str, *, xpath_for_contentful_data: str,
                                  child_xpath_for_contentful_image: Optional[str] = None,
                                  image_loader=None) -> Optional[Document]:
    html_etree = etree.HTML(html)
    text_elements = html_etree.xpath(xpath_for_contentful_data)
    if text_elements is None or len(text_elements) == 0: return None

    texts = []
    images_loaded = 0
    for el in text_elements:
        # replace images in el if necessary
        if child_xpath_for_contentful_image is not None:
            # child xpath
            print("el: ", el)
            print("child_xpath_for_contentful_image: ", child_xpath_for_contentful_image)
            images = el.xpath(child_xpath_for_contentful_image)
            print("images: ", images)
            for image in images:
                print(image)
                src = image.attrib.get("src")
                if src is None: continue
                loader = image_loader(src)
                loaded: Document = loader.load()
                # replace img with a span
                image_tree = etree.HTML(f'<div>![Image Content: {loaded.page_content}]({src})</div>')
                image.getparent().replace(image, image_tree)
                images_loaded += 1
        texts += el.xpath(".//text()")
    if len(texts) == 0: return None
    return Document(
        page_content="\n".join(texts),
        metadata={
            "feature": "xpath",
            "is_contentful": None,
            "article_detected": None,
            "images_loaded": images_loaded
        }
    )


class KebleHtmlLoader:

    def __init__(self, html: str, *, xpath_for_contentful_data: Optional[str] = None,
                 child_xpath_for_contentful_image: Optional[str] = None, image_loader=None):
        self.__html = html
        self.__xpath_for_contentful_data = xpath_for_contentful_data
        assert xpath_for_contentful_data is None or "text()" not in xpath_for_contentful_data, "You do not need to includes text() in your xpath_for_contentful_data, loader will automatically includes text() for you."
        assert child_xpath_for_contentful_image is None or child_xpath_for_contentful_image[
            0] == ".", "You child_xpath_for_contentful_image should start with \".\"; child_xpath_for_contentful_image will be use on all the contentful elements."
        assert child_xpath_for_contentful_image is None or xpath_for_contentful_data is not None, "You must provide xpath_for_contentful_data to have xpath_for_contentful_image works"
        self.__child_xpath_for_contentful_image = child_xpath_for_contentful_image
        self.__image_loader = image_loader

    def load(self) -> Document:
        if self.__xpath_for_contentful_data is None:
            return auto_load_meaningful_content(self.__html)

        else:
            loaded = xpath_load_meaningful_content(self.__html,
                                                   xpath_for_contentful_data=self.__xpath_for_contentful_data,
                                                   child_xpath_for_contentful_image=self.__child_xpath_for_contentful_image,
                                                   image_loader=self.__image_loader)
            if loaded is None:
                print("[Warning] xpath shows no result on html, switch to autoload instead.")
                return auto_load_meaningful_content(self.__html)
            return loaded
