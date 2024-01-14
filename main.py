import smtplib
import os

from bs4 import BeautifulSoup
import requests
import lxml

url = "https://www.amazon.co.uk/Samsung-Inch-CU8000-Smart-Built/dp/B0BW9STF5G/ref=sr_1_2_sspa?crid=30AH8IIZOLOL9&dib=eyJ2IjoiMSJ9.SoE81yCtXc7N1LtX_ZiV0CKCOYCqmVvcruwMrwFUAuv2xDEj2ZVXO4DLflgfYBd4W7X582kaDAEek8O4J54ImPOHzkXqcWFFILe0_ZfqxQeYxf-uGtJUHJaYHmSpVugPH5SRVTyPX7n0oJOgPYs3SA.DZQKVZqEmXsl7R26ZMHCSn-Eyc6ug8i9Eq8pM1kBIgU&dib_tag=se&keywords=UE65CU8500KXXU&qid=1705246914&s=electronics&sprefix=ue65cu8500kxxu%2Celectronics%2C113&sr=1-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1&smid=A37EAWMTY48SBW"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3",
    "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8"
}

YOUR_SMTP_ADDRESS = os.getenv("YOUR_SMTP_ADDRESS")
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
YOUR_PASSWORD = os.getenv("YOUR_PASSWORD")
FromYOUR_EMAIL = os.getenv("FromYOUR_EMAIL")
ToYOUR_EMAIL = os.getenv("ToYOUR_EMAIL")

response = requests.get(url, headers=header)
#print(response.text)
#top_hits = response.text

soup = BeautifulSoup(response.content, "lxml")
print(soup.prettify())

price = soup.find(class_="a-price-whole")

#price_without_currency = price.split("£")[1]
if price:
    price_as_float = float(price.get_text())
    print(price_as_float)
else:
    print("Element (Price) not found")

title = soup.find(id="productTitle")
print(title)

BUY_PRICE = 580

if title:
    if price_as_float < BUY_PRICE:
        message = f"{title} is now {price}"

        with smtplib.SMTP(YOUR_SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
            connection.sendmail(
                from_addr=FromYOUR_EMAIL,
                to_addrs=ToYOUR_EMAIL,
                msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
            )
else:
    print("Element (Title) not found")
