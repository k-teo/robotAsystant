import nltk


class TextComparator:
    def __init__(self):
        pass

    def compare(self, searchedProduct: str, storeProduct: str) -> bool:
        return self.is_the_same(searchedProduct, storeProduct) or self.is_similar(searchedProduct, storeProduct)

    def is_the_same(self, searchedProduct: str, storeProduct: str) -> bool:
        return searchedProduct.lower() == storeProduct.lower()

    def is_similar(self, searchedProduct: str, storeProduct: str) -> bool:
        return nltk.edit_distance(searchedProduct.lower(), storeProduct.lower()) < (1 if len(searchedProduct) <= 4 else 2) and \
               nltk.edit_distance(searchedProduct.lower(), storeProduct.lower()) < len(storeProduct)
