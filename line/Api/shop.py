from typing import List

from ..curve.console import Console
listen = Console.line_thrift

class Shop:

    def __init__(self):
        if self.isLoggin:
            if self.mod == "binary": path = "/SHOP3"
            else: path = self.endpoint.SHOP
            self.shop = self._connect(host=self.host,
                                         path= path,
                                         Headers= self.headers,
                                         service= self.console.ShopService,
                                         method = self.mod
            )

    def buyCoinProduct(self, paymentReservation):
        return self.call.buyCoinProduct(0, paymentReservation)

    def buyFreeProduct(self, receiverMid, productId, messageTemplate, language, country, packageId):
        return self.call.buyFreeProduct(0, receiverMid, productId, messageTemplate, language, country, packageId)

    def buyMustbuyProduct(self, receiverMid, productId, messageTemplate, language, country, packageId, serialNumber):
        return self.call.buyMustbuyProduct(0, receiverMid, productId, messageTemplate, language, country, packageId, serialNumber)

    def checkCanReceivePresent(self, recipientMid, packageId, language, country):
        return self.call.checkCanReceivePresent(0,  recipientMid, packageId, language, country)

    def getActivePurchases(self, start, size, language, country):
        return self.call.getActivePurchases(0, start, size, language, country)

    def getActivePurchaseVersions(self, start, size, language, country):
        return self.call.getActivePurchaseVersions(0, start, size, language, country)

    def getCoinProducts(self, appStoreCode, country, language) -> listen.CoinProductItem:
        return self.call.getCoinProducts(0, appStoreCode, country, language)

    def getCoinProductsByPgCode(self, appStoreCode, pgCode, country, language):
        return self.call.getCoinProductsByPgCode(0, appStoreCode, pgCode, country, language)

    def getCoinPurchaseHistory(self, request):
        return self.call.getCoinPurchaseHistory(0, request)

    def getCoinUseAndRefundHistory(self, request):
        return self.call.getCoinUseAndRefundHistory(0, request)

    def getDownloads(self, start, size, language, country) -> listen.ProductList:
        return self.call.getDownloads(0, start, size, language, country)

    def getEventPackages(self, start, size, language, country) -> listen.ProductList:
        return self.call.getEventPackages(0, start, size, language, country)

    def getNewlyReleasedPackages(self, start, size, language, country) -> listen.ProductList:
        return self.call.getNewlyReleasedPackages(0, start, size, language, country)

    def getPopularPackages(self, start, size, language, country) -> listen.ProductList:
            return self.call.getPopularPackages(0, start, size, language, country)

    def getPresentsReceived(self, start, size, language, country) -> listen.ProductList:
        return self.call.getPresentsReceived(0, start, size, language, country)

    def getPresentsSent(self, start, size, language, country) -> listen.ProductList:
        return self.call.getPresentsSent(0, start, size, language, country)

    def getProduct(self, packageID, language, country) -> listen.Product:
        return self.call.getProduct(0, packageID, language, country)

    def getProductList(self, productIdList, language, country) -> listen.ProductList:
        return self.call.getProductList(0, productIdList, language, country)

    def getProductListWithCarrier(self, productIdList, language, country, carrierCode) -> listen.ProductList:
        return self.call.getProductListWithCarrier(0, productIdList, language, country, carrierCode)

    def getProductWithCarrier(self, packageID, language, country, carrierCode) -> listen.Product:
        return self.call.getProductWithCarrier(0, packageID, language, country, carrierCode)

    def  getPurchaseHistory(self, start, size, language, country) -> listen.ProductList:
        return self.call.getPurchaseHistory(0, start, size, language, country)

    def getTotalBalance(self, appStoreCode: listen.PaymentType) -> listen.Coin:
        return self.call.getTotalBalance(0, appStoreCode)

    def notifyDownloaded(self, packageId, language):
        return self.call.notifyDownloaded(0, packageId, language)

    def reserveCoinPurchase(self, request: listen.CoinPurchaseReservation) -> listen.PaymentReservationResult:
        return self.call.reserveCoinPurchase(0, request)

    def reservePayment(self, paymentReservation: listen.PaymentReservation) -> listen.PaymentReservationResult:
        return self.call.reservePayment(0, paymentReservation)
