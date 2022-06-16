from bs4 import BeautifulSoup
import requests
from bokeh.plotting import figure, show, output_file, save
from bokeh.io import export_png
from bokeh.models import DatetimeTickFormatter
import datetime
import pandas as pd

link = "https://www.gumtree.com/search?search_category=cars&search_location=eh165xp&distance=50&vehicle_mileage=up_to_80000.html"

price_data = pd.read_csv("/Users/oscarslater/Documents/VScode/carprice/pricedata.csv")
print(price_data)

pg_list = [link]

#unable to find data sfor total pages, just doing 7 but should figure this out
first_half = "https://www.gumtree.com/search?search_category=cars&search_location=eh165xp"
second_half = "&distance=50&vehicle_mileage=up_to_80000.html"

for i in range(2,8,1):
    pg_list.append((first_half+"&page="+str(i)+second_half))

price_list = []
for page in pg_list:
    r = requests.get(page)
    c = r.content

    soup = BeautifulSoup(c, "html.parser")
    prices = soup.find_all("strong", {"class": "h3-responsive"})
    for price in prices:
        price = price.text
        if price == '':
            pass
        else:
            plainprice = float((price.replace('£','')).replace(",",""))
            price_list.append(plainprice)

averageprice = (sum(price_list)/len(price_list))
date = datetime.datetime.now()
d = {'Date': date,
    'Price': averageprice}
df = pd.DataFrame(d, index=[0])

price_data_new = pd.concat([price_data, df])
price_data_new.to_csv('/Users/oscarslater/Documents/VScode/carprice/pricedata.csv', index=False)
# tried bokeh, can't work it
p = figure(title = 'Car prices', x_axis_label = 'Date', y_axis_label = '£', x_axis_type = 'datetime')
p.line(price_data['Date'], price_data['Price'], line_width = 2)
p.xaxis[0].formatter = DatetimeTickFormatter(months = ["%b %d"])
output_file('carprices.html')
save(p)
