---
title: "Scraping Google Maps to Measure Electric Vehicle Infrastructure: Real-time EV Charger Data V1.0"
url: https://medium.com/p/77a2b4142a78
---

# Scraping Google Maps to Measure Electric Vehicle Infrastructure: Real-time EV Charger Data V1.0

[Original](https://medium.com/p/77a2b4142a78)

# Scraping Google Maps to Measure Electric Vehicle Infrastructure: Real-time EV Charger Data V1.0

[![Anna Mowat](https://miro.medium.com/v2/resize:fill:64:64/1*GzPFT9BVa98YxMq76GJtng.jpeg)](/@annamowat13?source=post_page---byline--77a2b4142a78---------------------------------------)

[Anna Mowat](/@annamowat13?source=post_page---byline--77a2b4142a78---------------------------------------)

4 min read

·

Jan 21, 2021

--

Listen

Share

More

Several factors have to be considered to measure how well established the EV infrastructure is within a country. Infrastructure factors include: current number of EVs owned, number of car dealerships, subsidies, number of chargers, and more.

Many of these measurements exist online and can often be found in long market reports, or on industry websites. The challenge is that these measurements are usually only updated annually.

**What if I wanted to measure the number of EV chargers in a country at this very moment?**

Let me show you how.

Press enter or click to view image in full size

![]()

[## Hong Kong EV Chargers | scattermapbox made by Amowat13 | plotly

### Amowat13's interactive graph and data of "Hong Kong EV Chargers" is a scattermapbox.

chart-studio.plotly.com](https://chart-studio.plotly.com/~amowat13/1.embed?share_key=oWJ2hHtC5JJTyszK4p1Bq7&source=post_page-----77a2b4142a78---------------------------------------)

We all know how to find the closest EV charger. All you have to do is just open your phone, type “ev charger” into google maps, and hit search. Boom, now you know where the closest twenty charging stations are.

So, in theory, you could:

(1) run this search,

(2) write down all the relevant search results,

(3) walk 10 km in one direction,

(4) and repeat.

While that is a super effective way to hit your daily step count, it is not realistic. Fortunately, there is a way to write a code that convinces google maps that you are very into long walks and car chargers.

**For this code, I have selected the geography of Hong Kong SAR to use as a case study.**

Using google map’s [Place API](https://developers.google.com/places/web-service/overview), we can feed a keyword, set of coordinates, and search radius to receive a list of relevant locations.

```
#Initial Parameters  
keywords = "ev charger"  
api_key = "your_API_key"#Coordinates for Exchange Square, Central, Hong Kong  
coordinates = ["22.2840,114,1578"]
```

We can then run the Places API using the above parameters. You use the API by giving it the coordinates of the place of interest and it responds to you with the top 60 hits in that area. Looping the code over the above coordinate, or more coordinates, you can pull information about each listed site that the keyword search recommends.

My code, seen below, saves the Name, Place ID, Latitude, Longitude, Rating, Type, Address, and Business Status of each listing.

```
#Pulls data from Google Maps based on coordinate grid and pushes data into final_data list final_data = []for coordinate in coordinates:     
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={coordinate}&radius=10000&keyword={keywords}&key={your_API_key}"     
       while True:       
         print(url)        
         respon = requests.get(url)            
         jj = json.loads(respon.text)          
         results = jj['results']     
         for result in results:            
            name = result['name']            
            place_id = result ['place_id']            
            lat = result['geometry']['location']['lat']            
            lng = result['geometry']['location']['lng']               
            rating = result['rating']            
            types = result['types']            
            vicinity = result['vicinity']            
            business_status = result['business_status']              
            data = [name, place_id, lat, lng, rating, types, vicinity, business_status]            
            final_data.append(data)             
    
            time.sleep(1)   
     
       if 'next_page_token' not in jj:      
              break     
       else:             
              url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={jj['next_page_token']}&key={your_API_key}"
```

Once the data is collected, I then:

(1) save the data into a pandas data frame,

(2) clean and delete any duplicate Place IDs,

(3) and push the data into a google sheet to save it.

```
import pandas as pd#Generated data is parsed into a Dataframe formlabels = ['Place Name','Place ID', 'Latitude', 'Longitude', 'Types', 'Vicinity', 'Business Status']ev_df = pd.DataFrame.from_records(final_data,columns=labels)#Drop duplicate rows  
ev_clean_df = ev_df.drop_duplicates(subset="Place ID")#Push Dataframe into Google Sheet  
wb = gc.open_by_url("Enter_Your_Google_Sheet_URL_Here")sheet = wb.worksheet('Enter_Sheet_Name_Here')  
set_with_dataframe(sheet, ev_clean_df)
```

To take this a step further, I added a function that produces a whole grid of coordinates when fed the specific corner quadrant values. Taking the geographic information of Hong Kong SAR and running the inputs through the code gave me all of the publicly available EV chargers in the country.

```
#Hong Kong Special Administrative Region lies between Latitude 22°08' North and 22°35' North, Longitude 113°49' East and 114°31' Eastlat0 = 20.08  
lon0 = 113.49  
coordinates = []  
lat_coordinates = ["20.08"]  
lon_coordinates = ["113.49"]#Generates Latitude values over 10 km intervals  
while True:  
   if lat0 < 22.35:  
      lat0 = lat0 + (180/3.14159265)*(10000/6378137)  
      lat_coordinates.append(f"{lat0}")   
      print(lat0)  
   else:  
      break#Generates Longitude values over a 10 km interval  
while True:  
   if lon0 < 114.31:  
      lon0 = lon0 + (180/3.14159265)*(10000/6378137)/math.cos(lat0)  
      lon_coordinates.append(f"{lon0}")  
      print(lon0)  
   else:   
      break#Iterates over the longitude and latitude variables to create a coordinate grid  
for lat in lat_coordinates:  
   for lon in lon_coordinates:  
      coordinates.append(f"{lat},{lon}")
```

A few rows of my dataset can be seen in the image below.

Press enter or click to view image in full size

![]()

Now that I have the exact location of each charger I can scrape even more information that will allow me to start measuring the maturity of the infrastructure, how individuals move through these spaces, and how well different companies are established in each country.

I re-ran this code a year after I originally wrote it to see how HK electric vehicle infrastructure has changed. A write-up of the update can be found below.

[## Scrapping Google APIs to Measure the Real-Time Change of Electric Vehicle Infrastructure (An…

### In late January 2021, I published a medium article providing a method (with the actual code) for how someone could…

annamowat13.medium.com](https://annamowat13.medium.com/scrapping-google-apis-to-measure-the-real-time-change-of-electric-vehicle-infrastructure-an-67a4138e4fa?source=post_page-----77a2b4142a78---------------------------------------)