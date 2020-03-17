import requests
from pprint import pprint
import csv

class Urbania:
    postings_url = "https://urbania.pe/rplis-api/postings"
    postings_miraflores_and_san_isidro_id = "51119497,51119502"
    postings_miraflores_id = "51119497"
    postings_san_isidro_id = "51119502"
    postings_magdalena_id = "51119496"
    less_than_five_years = 1
    urbania_rent = "2"
    urbania_buy = "1"
    postings_body = {
        "tipoDePropiedad": "2",
        "tipoDeOperacion": urbania_buy,
        "zone": postings_miraflores_id,
        "antiguedad": less_than_five_years
    }
    posting_map_url = "https://urbania.pe/rpfic-api/posting-map/"

    def postings(self, currentPage):
        self.postings_body["pagina"] = currentPage
        postings_request = requests.post(self.postings_url, json = self.postings_body)
        return postings_request.json()

class Paging:
    def __init__(self, total, currentPage, totalPages):
        self.total = total
        self.currentPage = currentPage
        self.totalPages = totalPages

    def nextPage(self):
        self.currentPage += 1

    def print(self):
        print("Total postings: ", self.total, "Total pages: ", self.totalPages, "current Page: ", self.currentPage)

class UrbaniaPosting:
    def __init__(self, postingJson):
        self.postingId = postingJson["postingId"]
        self.title = postingJson["title"]
        self.generatedTitle = postingJson["generatedTitle"]
        self.description = postingJson["description"]
        self.postingAntiquity = postingJson["antiquity"]
        self.url = "https://urbania.pe" + postingJson["url"]
        self.status = postingJson["status"]
        self.postingType = postingJson["postingType"]

        mainFeatures = postingJson["mainFeatures"]

        self.totalArea = mainFeatures.get("CFT100", {}).get("value")
        self.roofedSurface = mainFeatures.get("CFT101", {}).get("value")
        self.bedrooms = mainFeatures.get("CFT2", {}).get("value")
        self.bathrooms = mainFeatures.get("CFT3", {}).get("value")
        self.halfBathrooms = mainFeatures.get("CFT4", {}).get("value")
        self.antiquity = mainFeatures.get("CFT5", {}).get("value")
        self.parkingSlots = mainFeatures.get("CFT7", {}).get("value")
        self.priceAmount = postingJson["priceOperationTypes"][0]["prices"][0]["amount"]
        self.priceCurrencyId = postingJson["priceOperationTypes"][0]["prices"][0]["currencyId"]
        self.priceCurrency = postingJson["priceOperationTypes"][0]["prices"][0]["currency"]

    def toDict(self):
        return self.__dict__

#############

#############

urbaniaAPI = Urbania()
# Get Total postings
postingsPage = urbaniaAPI.postings(1)
paging = Paging(postingsPage["paging"]["total"], postingsPage["paging"]["currentPage"], postingsPage["paging"]["totalPages"])

f = open('miraflores_buy.csv', 'w')
with f:
    fnames = ['postingId', 'title', 'generatedTitle', 'description', 'postingAntiquity',
            'url', 'status', 'postingType', 'totalArea', 'roofedSurface', 'bedrooms',
            'bathrooms', 'halfBathrooms', 'antiquity', 'parkingSlots', 'priceAmount',
            'priceCurrencyId', 'priceCurrency']
    writer = csv.DictWriter(f, fieldnames=fnames)
    writer.writeheader()
    # Loop Postings pages
    while paging.currentPage < paging.totalPages:
        paging.print()
        postingsPage = urbaniaAPI.postings(paging.currentPage)
        postingsJson = postingsPage["listPostings"]
        for postingJson in postingsJson:
            urbaniaPosting = UrbaniaPosting(postingJson)
            pprint(urbaniaPosting.postingId)
            writer.writerow(urbaniaPosting.toDict())
        paging.nextPage()
