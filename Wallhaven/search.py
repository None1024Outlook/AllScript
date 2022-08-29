# ApiKey = wujdxIsRu0KDDJegilcTuhYADRR1WyGR

import requests
import threading
import time
import json

# Value
SourceUrl = "https://wallhaven.cc/api/v1/search?q={}&purity={}&page={}&atleast={}&apikey={}"
Time = 0
PngUrlList = []
PngNameList = []
PngFileType = []
PngSavePath = ""

# Error
class Error():
    def NsfwAndApikey(ApiKey : str):
        if ApiKey == "":
            raise Exception("Search Don't Have ApiKey")
    def PurityNotInput():
        raise Exception("Search Purity Error")
    def PageCheck(Page):
        if str(type(Page)) != "<class 'int'>":
            raise Exception("Page Not INT")
    def PngSaveCheck(Path : str):
        if Path == "":
            raise Exception("Don't Have Png Save Path")
    def NsfwPngNotHaveApiKey():
        raise Exception("Don't Have ApiKey")
    def TotalCheck(Total : int):
        if Total == 0:
            raise Exception("Don't Have Img")
    def DataCheck(Data):
        if Data == []:
            raise Exception("The Page Don't Have Img")

# time
class TimeCommand():
    def TimeAdd():
        global Time
        while True:
            time.sleep(1)
            Time += 1
    def TimeAddGo():
        threading.Thread(target=TimeCommand.TimeAdd)
    def TimeReturn():
        global Time
        return (60 - (Time % 60))

# Json
def TextToJson(ReqText : str):
    return json.loads(ReqText)

#Get
class Get():
    def GetPngUrl(Dic):
        return Dic["path"]
    def GetPngName(Dic):
        return Dic["id"]
    def GetPngType(Dic):
        if Dic["file_type"] == "image/jpeg":
            return "jpg"
        elif Dic["file_type"] == "image/png":
            return "png"
        else:
            return "NullFileType"

#Download
class Download():
    def Png(PageNum):
        global PngUrlList
        global PngNameList
        global PngFileType
        global PngSavePath
        print(f"\n==========Download Start==========\nPage : {PageNum}\n==========Download Start==========\n")
        for PngI in range(len(PngFileType)):
            Req = requests.get(url=PngUrlList[PngI])
            ReqCode = Req.status_code
            if ReqCode == 200:
                PngPath = PngSavePath + "/" + PngNameList[PngI] + "." + PngFileType[PngI]
                with open(PngPath, "wb") as f:
                    f.write(Req.content)
                    print(f"{PngPath} ok - Download")
            elif ReqCode == 429:
                print("Requests too many")
                TimeSleep = TimeCommand.TimeReturn()
                print(f"Sleep {TimeSleep} s - Download")
                time.sleep(TimeSleep)
                print("Sleep ok - Download")
                Download.Png(PngUrlList[PngI])
            elif ReqCode == 401:
                Error.NsfwPngNotHaveApiKey()
        PngUrlList = []
        PngNameList = []
        PngFileType = []
        print(f"\n==========Download OK==========\nPage : {PageNum}\n==========Download OK==========")

# Search
class Search():
    def SearchInit(SearchString : str, ApiKey = "", Purity = "sfw", Atleast = "", Page = 1, SavePath=r"./Png"):
        global PngSavePath
        # Png Save
        Error.PngSaveCheck(SavePath)
        PngSavePath = SavePath
        # Purity To str(int)
        if Purity == "sfw":
            Purity = "100"
        elif Purity == "sketchy":
            Purity = "010"
        elif Purity == "nsfw":
            Purity = "001"
            Error.NsfwAndApikey(ApiKey)
        elif Purity == "sfw&sketchy":
            Purity = "101"
        elif Purity == "sfw&sketchy":
            Purity = "110"
        elif Purity == "sketchy&nsfw":
            Purity = "011"
            Error.NsfwAndApikey(ApiKey)
        elif Purity == "sfw&sketchy&nsfw":
            Purity = "111"
            Error.NsfwAndApikey(ApiKey)
        else:
            Error.PurityNotInput()
        # Page Check
        Error.PageCheck(Page)
        # Msg To Url
        NewUrlList = []
        for PageI in range(1, Page + 1):
            NewUrlList.append(SourceUrl.format(SearchString, Purity, PageI, Atleast, ApiKey))
        for Url in NewUrlList:
            Search.SearchPng(Url)
    def SearchPng(Url : str):
        global PngUrlList
        global PngNameList
        global PngFileType
        print(f"\n==========Requests Start==========\nUrl : {Url}\n==========Requests Start==========")
        TimeCommand.TimeAddGo()
        Req = requests.get(url=Url)
        ReqCode = Req.status_code
        ReqText = Req.text
        JsonData = TextToJson(ReqText)
        Data = JsonData["data"]
        Meta = JsonData["meta"]
        Error.DataCheck(Data)
        Total = Meta["total"]
        Error.TotalCheck(Total)
        PageNum = Meta["current_page"]
        print(f"\n==========Requests OK==========\nUrl : {Url}\n==========Requests OK==========")
        if ReqCode == 200:
            for DataI in Data:
                PngUrlList.append(Get.GetPngUrl(DataI))
                PngNameList.append(Get.GetPngName(DataI))
                PngFileType.append(Get.GetPngType(DataI))
            Download.Png(PageNum)
        elif ReqCode == 429:
            print("Requests too many")
            TimeSleep = TimeCommand.TimeReturn()
            print(f"Sleep {TimeSleep} s - Search")
            time.sleep(TimeSleep)
            print("Sleep ok - Search")
            Search.SearchPng(Url)
        elif ReqCode == 401:
            Error.NsfwPngNotHaveApiKey()

# Start
Search.SearchInit("genshin", Purity="nsfw", ApiKey="wujdxIsRu0KDDJegilcTuhYADRR1WyGR", SavePath=r"./Png/Genshin/Nsfw", Page=100)
