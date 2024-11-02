import requests

def jina(url):
        base_url = "https://r.jina.ai/"
        url = base_url + url
        response = requests.get(url)
        # print(response.text)
        return response.text

cities = ['Ahmedabad', 'Ayodhya' , 'Bangalore' , 'Bhubaneswar' , 'Chandigarh' , 'Chennai', 'Coimbatore', 'Delhi' , 'Hyderabad' , 'Jaipur' , 'Kerala' , 'Kolkata', 'Lucknow', 'Madurai' , 'Mangalore' , 'Mumbai' , 'Mysore' , 'Nagpur' , 'Nashik' , 'Patna' , "Pune" , 'Rajkot' , 'Salem' , 'Surat' , 'Trichy' , 'Vadodara' , 'Vijayawada' , 'Visakhapatnam' ]

def price_cities(url):
  text = jina(url)
  pos1 = text.find('**')
  new = text[:pos1]
  twentytwok = new[int(new.find('22K')):int(new.find('24K'))]
  value_22k = twentytwok[int(twentytwok.find('\n\n')+1): int(twentytwok.find('\n\n+'))][3:]
  twentyfourk = new[int(new.find('24K')):int(new.find('18K'))]
  value_24k = twentyfourk[int(twentyfourk.find('\n\n')+1): int(twentyfourk.find('\n\n+'))][3:]
  eighteenk = new[int(new.find('18K')):]
  value_18k = eighteenk[int(eighteenk.find('\n\n')+1): int(eighteenk.find('\n\n+'))][3:]
  return value_22k, value_24k, value_18k


for city in cities[0:15]:
  city_url = f"https://www.goodreturns.in/gold-rates/{city}.html"
  print(city_url)
  x,y,z = price_cities(city_url)
  print(x,y,z)
  print(f"Price of 24K: {y} , 22K: {x} , 18K: {z} in {city}")

# def one