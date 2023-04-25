class MpClass:
    def __init__(self):
    # Максимальное число символов в url
        self.lenFriendlyUrl = 30

    def convertUrl(self, src:str, title:str):
        photoname = src[src.rfind("/")+1:(len(src))]
        if len(title) <= self.lenFriendlyUrl:
            suburl = title.replace(" ", "_")
            return suburl + "_" + photoname
        else:
            # Убираем артиклы, если они есть в начале
            title = title.replace("The ", "", 1)
            title = title.replace("A ", "", 1)
            words = title.split()
            suburl = ""
            suburl_len = 0
            # Заполняем целыми словами
            for iword in words:
                suburl_len += len(iword) + 1
                if suburl_len > self.lenFriendlyUrl:
                    break
                if suburl == "":
                    suburl += iword
                else:
                    suburl += "_" + iword
            return suburl + "_" + photoname