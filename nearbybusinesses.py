import requests
import pandas as pd
# import tkinter as tk
# from tkinter import *

# root = Tk()

df1 = pd.DataFrame(columns= ['Name','Business Status','Address','Rating','Phone Number','Website'])
df2 = pd.DataFrame(columns= ['Name','Business Status','Address','Rating','Phone Number','Website'])
df3 = pd.DataFrame(columns= ['Name','Business Status','Address','Rating','Phone Number','Website'])
lastpagetoken = ""
lastpage = False

# List of all business type supported by Google's Place API as of Jan 6 2023 
business_types = ["accounting", "airport", "amusement_park", "aquarium", "art_gallery", "atm", "bakery", "bank", "bar", "beauty_salon", "bicycle_store", "book_store", 
        "bowling_alley", "bus_station", "cafe", "campground", "car_dealer", "car_rental", "car_repair", "car_wash", "casino", "cemetery", "church", "city_hall", "clothing_store", "convenience_store", "courthouse", "dentist", 
        "department_store", "doctor", "drugstore", "electrician", "electronics_store", "embassy", "fire_station", "florist", "funeral_home", "furniture_store", "gas_station", "gym", "hair_care", "hardware_store", "hindu_temple", 
        "home_goods_store", "hospital", "insurance_agency", "jewelry_store", "laundry", "lawyer", "library", "light_rail_station", "liquor_store", "local_government_office", "locksmith", "lodging", "meal_delivery", 
        "meal_takeaway", "mosque", "movie_rental", "movie_theater", "moving_company", "museum", "night_club", "painter", "park", "parking", "pet_store", "pharmacy", "physiotherapist", "plumber", "police", "post_office", 
        "primary_school", "real_estate_agency", "restaurant", "roofing_contractor", "rv_park", "school", "secondary_school", "shoe_store", "shopping_mall", "spa", "stadium", "storage", "store", "subway_station", "supermarket", 
        "synagogue", "taxi_stand", "tourist_attraction", "train_station", "transit_station", "travel_agency", "university", "veterinary_care", "zoo", ]

def get_apikey_from_user():
    user_entered_apikey = ent_userapikey.get()
    return user_entered_apikey

def get_businesstype_from_user():
    user_selected_businesstype = drop_clicked.get()
    return user_selected_businesstype

def get_coordinates_from_address():
    url = 'https://addressvalidation.googleapis.com/v1:validateAddress?key='+get_apikey_from_user()
    data =  { 
    "address": {
    "addressLines": [ent_userlocation.get()]
        },
    "enableUspsCass": "true"
    }
    response = requests.post(url, json=data)
    resp_dict = response.json()
    user_coordinates = str(resp_dict['result']['geocode']['location']['latitude'])+","+str(resp_dict['result']['geocode']['location']['longitude'])
    return user_coordinates

def get_radius_entry():
    user_entered_radius = ent_custom_radius.get()
    converted_to_meters = int(user_entered_radius)*1650
    converted_to_meters_string = str(converted_to_meters)
    return converted_to_meters_string

def looping_results(business_results):
        temp_df = pd.DataFrame(columns= ['Name','Business Status','Address','Rating','Phone Number','Website'])
        for index, row in business_results.iterrows():
            row_place = requests.get('https://maps.googleapis.com/maps/api/place/details/json?fields=name%2Cbusiness_status%2Crating%2Cformatted_address%2Cformatted_phone_number%2Cwebsite&place_id='+row['place_id']+'&key='+get_apikey_from_user()) 
            resp_dict = row_place.json()
            business = resp_dict['result']
            # Varaibles to build the individual rows of the large dataframe
            if 'name' in business:
                varname = business['name']
            else: 
                varname = "no name"
            if 'business_status' in business:
                varbusstatus = business['business_status']
            else: 
                varname = "no name"                
            if 'formatted_address' in business:
                varaddress = business['formatted_address']
            else: 
                varaddress = "no address"
            if 'rating' in business:
                varrating = business['rating']
            else: 
                varrating = "no rating"
            if 'formatted_phone_number' in business:
                varphone = business['formatted_phone_number']
            else: 
                varphone = "no phone"
            if 'website' in business: 
                varwebsite = business['website']
            else: 
                varwebsite = "no website"
            # Inserting the row from each loop into the large array
            temp_df.loc[index] = [varname,varbusstatus,varaddress,varrating,varphone,varwebsite]
        return temp_df

def nexttoken_actions(raw_resp, json_resp):
    global lastpage 
    global lastpagetoken
    global df2
    if "next_page_token" in raw_resp.text:
        print("1. NEXT PAGE AVAILABLE (>20 results)")
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken='+json_resp['next_page_token']+'&key='+get_apikey_from_user()
        nextpage = requests.get(url)
        resp_dict = nextpage.json()
        df = pd.DataFrame(resp_dict.get('results'))
        if "next_page_token" in nextpage.text: lastpage = True
        if "next_page_token" in nextpage.text: lastpagetoken = str(resp_dict['next_page_token'])
        df2 = looping_results(df)
    else:
        print("No additional pages (less than 40 total results)")
    return df2

def lasttoken_actions(lastpage, lastpagetoken):
    global df3
    if lastpage == True:
        print("2. NEXT PAGE AVAILABLE (>40 results)")
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken='+lastpagetoken+'&key='+get_apikey_from_user()
        nextpage = requests.get(url)
        resp_dict = nextpage.json()
        df = pd.DataFrame(resp_dict.get('results'))
        df3 = looping_results(df)
    else:
        print("FINAL PAGE REGARDLESS")
    return df3

def searching(event):
    nearby_search_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+get_coordinates_from_address()+'&radius='+get_radius_entry()+'&type='+get_businesstype_from_user()+'&key='+get_apikey_from_user()
    x = requests.get(nearby_search_url)
    resp_dict = x.json()
    df = pd.DataFrame(resp_dict.get('results'))
    df1 = looping_results(df)
    df2 = nexttoken_actions(x, resp_dict)  
    df3 = lasttoken_actions(lastpage, lastpagetoken)
    # Inline conditional to set large df based on number of smaller not empty dfs 
    large_df = pd.concat([df1, df2, df3]) if not df1.empty and not df2.empty and not df3.empty else pd.concat([df1, df2]) if not df1.empty and not df2.empty else df1
    large_df.to_excel('output.xlsx',index=False)
    # root.destroy()
    return

# tk.Label(text="This is a simple tool to get information on some businesses near you! Please check the folder that this application is located in for a file named output.xlsx for your results.").pack()
# tk.Label(text="One limitation of this application is that it can only return 60 businesses maximum at the moment. This is a limitation by Google's Places API.").pack()
# lbl_userlocation = tk.Label(text="Enter your street address and postal code (i.e. 123 Happy Street 45678)")
# ent_userlocation = tk.Entry()
# lbl_userlocation.pack()
# ent_userlocation.pack()

# lbl_custom_radius = tk.Label(text="Radius in Miles (Up to 30)")
# ent_custom_radius = tk.Entry()
# lbl_custom_radius.pack()
# ent_custom_radius.pack()

# lbl_userapikey = tk.Label(text="Enter your API key")
# ent_userapikey = tk.Entry()
# lbl_userapikey.pack()
# ent_userapikey.pack()

# # Datatype of menu text
# drop_clicked = StringVar()
# # Initial menu text
# drop_clicked.set( "Select an option" )
# # Dropdown for now - can improve when added to GH Actions or built in a combobox with the proper function to run it
# drop = OptionMenu( root , drop_clicked , *business_types )
# drop.pack()

# btn_runit = tk.Button(text="Run the tool!")
# btn_runit.bind("<Button-1>", searching)
# btn_runit.pack()
# root.mainloop()