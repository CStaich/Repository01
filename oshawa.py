import requests
from bs4 import BeautifulSoup
from unicodecsv import writer
from tqdm import tqdm
import rauth
import string

# This program scrapes the main directory below for business information,
# organizes the information into dictionaries
# then dumps the results into dumpfile.txt
#Code written by Charlie Staich


#main_directory = "http://web.oshawachamber.com/allcategories"
main_directory = "http://web.oshawachamber.com/Restaurants-Food-Beverages"
rootdir = "http://web.oshawachamber.com"
loc = "Oshawa"
secretsfile = "yelp_secrets.txt"
outfile = "Restaurants-Food-Beverages test.csv"



info = []
name_dict = {
    "title": [0, "^title$"],
    "url": [0, "^url$"],
    "info": [0, "^company_info_ifr$"],
    "description": [0, "^no_coupon_text_ifr$"],
    "address1": [0, "^address$"],
    "address2": [0, "^address2$"],
    "city": [0, "^city$"],
    "state": [2, "^state$"],
    "zip": [0, "^zip$"],
    "phone": [0, "^phone$"],
    "vct": [0, "^view_coupons_text$"],
    "vit": [0, "^view_info_text"]
}

def yelp_search(params, secretsfile=secretsfile):
    #pulls secrets, searches api, returns response
    secrets = []
    with open(secretsfile, 'r') as sf:
        for line in sf:
            secrets.append(str(line.strip()))

    session = rauth.OAuth1Session(
    consumer_key = secrets[0],
    consumer_secret = secrets[1],
    access_token = secrets[2],
    access_token_secret = secrets[3]
    )

    request = session.get("http://api.yelp.com/v2/search",params=params)
    data = request.json()
    session.close()
    return data

def prettify(i):
    i = str(i).encode("utf-8").replace("(","").replace(")","")
    if i[0:2] == "u'" or i[0:2] == 'u"':
        i = i[2:-2]
    return i

def yelp_desc(listing_title):
    #fill desc with yelp listing info
    term = " ".join((listing_title.translate(string.maketrans("",""), string.punctuation)[:-3]).split(' ')[:-1])
    print term
    yelp_api_listing = yelp_search({
        'term': term,
        'location': loc,
        'limit': 1
    })
    if yelp_api_listing["total"] > 0:
        """
        yelp_api_listing = yelp_api_listing["businesses"][0]
        listing_link = "https://yelp.com/biz/" + yelp_api_listing["id"]
        yelp_listing = BeautifulSoup(requests.get(listing_link.content, "html.parser"))
        try:
            listing_desc = yelp_listing.find("div", {"class": "ywidget js-from-biz-owner"}).find("p").text.strip().replace("\n","")
            return listing_desc
        except:
            return "-none-"
            """
    else:
        print "no results"

def build_querylist(main_directory):
    r = requests.get(main_directory)
    soup = BeautifulSoup(r.content, "html.parser")
    links = soup.find("div", {"class": "left twoThirdsWidth"}).find_all("a")
    out_links = []
    for link in links:
        out_links.append(rootdir + link.get("href"))
    print "---BEGINNING SCRAPE---"
    return out_links

def scrape(listing, query):
    listing_info = {}
    listing_info["title"] = listing.find("span", {"itemprop": "name"}).text + " CS",
    listing_info["address1"] = listing.find("span", {"itemprop": "street-address"}).text,
    listing_info["city"] = listing.find("span", {"itemprop": "locality"}).text,
    listing_info["state"] = listing.find("span", {"itemprop": "region"}).text,
    listing_info["zip"] = listing.find("span", {"itemprop": "postal-code"}).text.replace(" ",""),
    try:
        listing_info["phone"] = listing.find("div", {"class": "ListingResults_Level3_PHONE1"}).text.replace(" ","-"),
    except:
        pass
    try:
        listing_info["url"] = listing.find("span", {"class": "ListingResults_Level3_VISITSITE"}).find("a").get("href").replace("http://","")
    except:
        try:
            listing_info["url"] = listing.find("a", {"class": "ListingDetails_Level3_SITELINK"}).get("href").replace("http://","")
        except:
            try:
                listing_info["url"] = query.replace("http://","")
            except:
                pass
    for i in listing_info:
        listing_info[i] = prettify(listing_info[i])
    listing_info["description"] = '<p style="text-align: center;" data-mce-style="text-align: center;"><span class="header3"></span></p>'
    listing_info["info"] = '<p style="text-align: center;" data-mce-style="text-align: center;"><span class="header3">Visit our website for more information</span></p>'
    listing_info["vit"] = "More Information"
    listing_info["vct"] = "About Us"
    #yelp_desc(listing_info["title"])
    info.append(listing_info)
    print "    " + listing_info["title"]
    return

def get_listings(querylist):
    #search for keywords pass in 'query' on yelp.com
    for query in querylist:
        print query
        try:
            r = requests.get(query)
            soup = BeautifulSoup(r.content, "html.parser")
        except:
            pass #invalid link
        try:
            listings = soup.find_all("div", {"class": "ListingResults_All_CONTAINER ListingResults_Level3_CONTAINER"})
            if len(listings) > 0:
                for listing in listings:
                    scrape(listing, query=query)
            else:
                scrape(soup, query=query)
        except:
            pass
    return info

def main():
    #list of links to search terms
    querylist = build_querylist(main_directory)
    #initialize output dumps with headers, column names
    profiles = [["### PROFILES ###","","","",""],["Profile ID","Name","Site","Overwrite",""]]
    autofillrules = [["### AUTOFILL RULES ###","","","",""],["Type","Name","Value","Site","Profile"]]
    count = 0
    results = get_listings(querylist)
    for result in results:
        count = count + 1
        profileid = "c" + str(count)
        profiles.append([profileid, result['title'],"", 1, ""])
        for item in result:
            autofillrules.append([name_dict[item][0], name_dict[item][1], result[item], "", profileid])
    with open(outfile,'w') as df:
        dumpfile = writer(df, delimiter=',', lineterminator='\n')
        dumpfile.writerows(profiles)
        dumpfile.writerows(autofillrules)

if __name__ == "__main__":
    main()
