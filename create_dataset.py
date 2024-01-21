import requests
from bs4 import BeautifulSoup
import os

base_url = 'http://www.rembrandtpainting.net/'
folder_path = "schilderijen/Rembrandt"

def download_image(path, save_path):
    response = requests.get(path)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Find the image in the div with id 'workimage'
        workimage_div = soup.find('div', {"id": "workimage"})
        img_tag = workimage_div.find('img')
        img_url = img_tag.get('src')

        # Construct the full URL
        img_url = os.path.join(base_url, img_url.replace('../', ''))

        # Fetch the image
        image = requests.get(img_url)
        if image.status_code == 200:
            image.raise_for_status()
            image_name = os.path.basename(img_url)

            print(f'image {image_name}')
            # Save the image
            with open(os.path.join(save_path, image_name), "wb") as f:
                f.write(image.content)

def get_url_of_image(row):
    tds = row.find_all('td')

        # If there's a second td, get the 'a' tag inside it
    if len(tds) > 1:
        a_tag = tds[1].find('a')

        # If 'a' tag exists and has 'href' attribute, get the 'href'
        if a_tag and a_tag.get('href'):
            link = a_tag.get('href')

            # Convert relative URL to absolute
            return os.path.join(base_url + "/complete_catalogue/", link)



def download_every_image(url, folder):
    print(f'Downloading {url}')
    try:
        response = requests.get(url)
        response.raise_for_status()

        table = BeautifulSoup(response.content, "html.parser")
        # Find the table with the class 'tablelinks'
        # Get all rows of the table
        all_rows = table.find_all('tr')

        # Initialize an empty list to store the URLs
        all_links = []

        # Iterate over all rows
        for row in all_rows:
            all_links.append(get_url_of_image(row))


        for link in all_links:
            download_image(link, folder)


    except Exception as e:
        print(f"An error occured: {e}")


def paginate_table_links(url):
    # Request the page
    response = requests.get(url)

    # If the request is successful, the status code will be 200
    if response.status_code == 200:
        # get the content of the page
        page_content = response.content

        # Create BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'html.parser')

        # Find the table with the class 'tablelinks'
        link_table = soup.find('table', {"class": "tablelinks"})

        # Find all 'a' tags in the table
        links = link_table.findAll('a')

        # Extract the 'href' attribute of each link and add the base url
        urls = ["{}{}".format(base_url + "/complete_catalogue/", link.get('href')) for link in links]

        return urls


# Check if the folder exists
if os.path.isdir(folder_path):
    print(f"The folder '{folder_path}' exists.")
else:
    os.makedirs("schilderijen/Rembrandt")

urls = paginate_table_links(base_url + "/complete_catalogue/complete_catalogue.htm")
for url in urls:
    print(url)
    download_every_image(url, folder_path)