from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

url = 'https://framememories.net'
root_domain = urlparse(url).netloc

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
items = soup.find_all('img')

def get_image_name(url):
    parsed_url = urlparse(url)
    path = parsed_url.path.rstrip('/')
    if path:
        return path.split('/')[-1]
    else:
        return None

def get_images_urls(items, root_domain):
    links = []
    for i in items:
        if i.findChildren("a"):
            image_tag = i.findChildren("a")
            links.append( 
                { get_image_name(image_tag[0]['href']) : image_tag[0]['href']}
            )
        else:
            image_tag = f"https://{root_domain}" +i.get('src')
            links.append(
                {get_image_name(image_tag) : image_tag}
            )
    return links


def download_img(images_urls):
    for image in images_urls:
        name, url = next(iter(image.items()))
        print("Downloading " + name + "...")
        response = requests.get(url).content
        with open("images/" + str(name) + ".jpg", "wb") as f:
            f.write(response)
            print('Image scraped successfully.')


for i in range(0,1000):
    images_urls = get_images_urls(items, root_domain)
    count = len(images_urls)
    print(f"{count} images counted")
    download_img(images_urls)

