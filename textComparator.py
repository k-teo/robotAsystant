
class TextComparator:
    def __init__(self):
        pass

    def compare(self, searchedProduct: str, storeProduct: str)->bool:
        return searchedProduct.lower() == storeProduct.lower()