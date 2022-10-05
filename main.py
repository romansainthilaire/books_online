from pathlib import Path
import requests
import bs4
import re
from word2number import w2n
from slugify import slugify
import csv


def get_soup(url):
    """
    Args:
        url (str): url of the page to scrape

    Returns:
        BeautifulSoup: parse tree used to extract data from HTML document
    """
    result = requests.get(url)
    return bs4.BeautifulSoup(result.text, "lxml")

def get_universal_product_code(product_page_soup):
    """
    Args:
        product_page_soup (BeautifulSoup): parse tree of the product page 

    Returns:
        str: universal product code (upc)
    """
    return product_page_soup.select("td")[0].text

def get_product_title(product_page_soup):
    """
    Args:
        product_page_soup (BeautifulSoup): parse tree of the product page 

    Returns:
        str: product title
    """
    return product_page_soup.select("h1")[0].text

def get_product_price_including_tax(product_page_soup):
    """
    Args:
        product_page_soup (BeautifulSoup): parse tree of the product page 

    Returns:
        str: product price including tax
    """
    return product_page_soup.select("td")[3].text[1:]

def get_product_price_excluding_tax(product_page_soup):
    """
    Args:
        product_page_soup (BeautifulSoup): parse tree of the product page 

    Returns:
        str: product price excluding tax
    """
    return product_page_soup.select("td")[2].text[1:]

def get_product_number_available(product_page_soup):
    """
    Args:
        product_page_soup (BeautifulSoup): parse tree of the product page 

    Returns:
        str: number of products available
    """
    return re.findall(r"\d+", product_page_soup.select("td")[5].text)[0]

def get_product_description(product_page_soup):
    """
    Args:
        product_page_soup (BeautifulSoup): parse tree of the product page 

    Returns:
        str: description of the product
    """
    return product_page_soup.select("p")[3].text

def get_product_category(product_page_soup):
    """
    Args:
        product_page_soup (BeautifulSoup): parse tree of the product page 

    Returns:
        str: category of the product
    """
    return product_page_soup.select(".breadcrumb > li")[2].text[1:-1]

def get_product_review_rating(product_page_soup):
    """
    Args:
        product_page_soup (BeautifulSoup): parse tree of the product page 

    Returns:
        str: review rating of the product
    """
    rating_class = product_page_soup.select("p")[2].attrs["class"][1]
    return w2n.word_to_num(rating_class)

def get_product_image_url(product_page_soup):
    """
    Args:
        product_page_soup (BeautifulSoup): parse tree of the product page 

    Returns:
        str: url of the product image
    """
    base_url = "https://books.toscrape.com"
    return  base_url + str(product_page_soup.select("img")[0]["src"][5:])

def get_product_details(product_url):
    """
    Args:
        product_url (str): url of the product

    Returns:
        List[str]: list of all the product details
    """
    product_page_soup = get_soup(product_url)
    return [
        product_url,
        get_universal_product_code(product_page_soup),
        get_product_title(product_page_soup),
        get_product_price_including_tax(product_page_soup),
        get_product_price_excluding_tax(product_page_soup),
        get_product_number_available(product_page_soup),
        get_product_description(product_page_soup),
        get_product_category(product_page_soup),
        get_product_review_rating(product_page_soup),
        get_product_image_url(product_page_soup)
    ]

def get_all_category_urls():
    """Returns the urls of all the categories

    Returns:
        List[str]: urls of all the categories
    """
    soup = get_soup("https://books.toscrape.com/")
    base_url = "https://books.toscrape.com/"
    return [base_url + str(a["href"]) for a in soup.select(".nav.nav-list a")][1:]

def get_all_product_urls_by_category(category_url):
    """Returns the urls of all the products for a specific category

    Args:
        category_url (str): url of the category

    Returns:
        List[str]: all product urls of the category
    """
    soup = get_soup(category_url)
    all_product_urls = []
    n = 1
    base_url = "https://books.toscrape.com/catalogue/"
    while True:
        product_urls = [base_url + str(a["href"][9:]) for a in soup.select(".product_pod > h3 > a")]
        all_product_urls.extend(product_urls)
        next_button = soup.select(".next")
        if next_button == []:
            break
        n += 1
        category_url = f"{category_url[:-11]}/page-{n}.html"
        soup = get_soup(category_url)
    return all_product_urls

def create_csv_file_by_category(category_name, category_product_urls):
    """Creates a csv file for a specific category.
       The csv file is created in a sub-folder called 'data' in the same folder as this python script.
       The name of the csv file is the same as the name of the category.

    Args:
        category_name (str): name of the category
        category_product_urls (List[str]): all product urls of the category
    """
    data_folder = Path(__file__).parent / "data"
    data_folder.mkdir(exist_ok=True)
    with open(data_folder / f"{slugify(category_name)}.csv", mode="w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")
        headlines = [
            "product_page_url",
            "universal_product_code (upc)",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url"
            ]
        csv_writer.writerow(headlines)
        for product_url in category_product_urls:
            product_details = get_product_details(product_url)
            csv_writer.writerow(product_details)

def create_images_folder_by_category(category_name, category_product_urls):
    """Creates a folder containing the images of all the products of a specific category.
       The images folder is created in a sub-folder called 'data' in the same folder as this python script.
       The images folder name is the same as the category name. 

    Args:
        category_name (str): name of the category
        category_product_urls (List[str]): all product urls of the category
    """
    data_folder = Path(__file__).parent / "data"
    data_folder.mkdir(exist_ok=True)
    images_folder = data_folder / slugify(category_name)
    images_folder.mkdir(exist_ok=True)
    for product_url in category_product_urls:
        product_details = get_product_details(product_url)
        image_url = product_details[-1]
        image = requests.get(image_url)
        product_title = product_details[2][:100] # maximum of 100 chars to avoid too file name
        with open(images_folder / f"{slugify(product_title)}.jpg", "wb") as file:
            file.write(image.content)


if __name__ == "__main__":

    for category_url in get_all_category_urls():
        soup = get_soup(category_url)
        category_name = soup.select(".breadcrumb > li")[2].text
        category_product_urls = get_all_product_urls_by_category(category_url)
        print(f"Scraping category '{category_name}' ({len(category_product_urls)} products) :")
        print("→ Creating csv file...")
        create_csv_file_by_category(category_name, category_product_urls)
        print("→ Downloading images...")
        create_images_folder_by_category(category_name, category_product_urls)
