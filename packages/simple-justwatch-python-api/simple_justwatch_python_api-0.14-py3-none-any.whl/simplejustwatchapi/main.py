from justwatch import details, offers_for_countries, search
from query import MediaEntry, Offer, OfferPackage


def main():
    response = search("The Matrix", "US", "en", 3, True)
    print(response)
    print()

    response = details("tm10", "US", "en", False)
    print(response)
    print()

    response = offers_for_countries("tm10", {"US", "GB", "FR"}, "en", True)
    print(response)
    print()



if __name__ == "__main__":
    main()
