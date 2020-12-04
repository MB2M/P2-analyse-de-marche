import csv
import requests
import nums_from_string
from bs4 import BeautifulSoup

urlForImg = 'http://books.toscrape.com/'

url = 'http://books.toscrape.com/catalogue/the-past-never-ends_942/index.html'


response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

bookTitle = soup.find(class_="product_main").h1.text

productInformations = {}
for row in soup.find(class_="table table-striped").find_all('tr'):
    productInformations[row.th.text] = row.td.text

bookUPC = productInformations['UPC']
bookTTC = productInformations['Price (incl. tax)'].strip('Â')
bookHT = productInformations['Price (excl. tax)'].strip('Â')
bookStock = nums_from_string.get_nums(productInformations['Availability'])[0]
bookDescription = soup.find("div", id={'product_description'}).find_next_sibling("p").text

bookTitle = soup.find(class_="product_main").h1.text
bookCategory = soup.find('li', class_='active').find_previous_sibling('li').a.text
bookRating = soup.find('p', class_='star-rating')['class'][1]
bookImageUrl = urlForImg + soup.find('div', class_="item active").img['src'].replace('../', "")

with open('books.csv', 'w', newline='') as csvfile:
    csvfile.write('product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,'
                  'number_available,product_description,category,review_rating,image_url\n')
    csvfile.write(url + "," + bookUPC + "," + bookTitle + "," + bookTTC + "," + bookHT + "," + str(bookStock) +
                  "," + bookDescription + "," + bookCategory + "," + bookRating + "," + bookImageUrl + '\n')
