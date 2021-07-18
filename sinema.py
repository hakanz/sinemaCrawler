import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
import urllib
profile = webdriver.FirefoxProfile("3js2pbup.default")
driver = webdriver.Firefox(profile,options=options)
driver2 = webdriver.Firefox(profile,options=options)
pageNumber = 0
totalPageCount = 0
movies = {}
moviesCount = 0

def startScan():
    global options
    global driver
    global totalPageCount
    driver.get("https://www.sinemalar.com/filmler")
    time.sleep(0.5)
    pageBtnsUl = driver.find_element_by_xpath("//div[ul/@class='pager']")
    pageBtns = pageBtnsUl.find_elements_by_tag_name("a")
    btnCount = 0
    for p in pageBtns:
        if p.get_attribute("data-page") != "None":
            if btnCount == 9:
                if totalPageCount == 0:
                    totalPageCount = p.get_attribute("data-page")
        btnCount += 1
    print(totalPageCount, " adet sayfadan veri toplanacak, ilk sayfa toplanıyor.")
    collectListPageData()

def collectListPageData():
    global movies
    global moviesCount
    global totalPageCount
    global pageNumber
    time.sleep(0.4)
    movieList = driver.find_elements_by_xpath("//div[@class='movie-detail']")
    for m in movieList:
        movieTitleTurkish = m.find_element_by_xpath("div[@class='title left']/a").text
        movieDetailPageUrl = m.find_element_by_xpath("div[@class='title left']/a").get_attribute("href")
        print("Film adı: ",movieTitleTurkish)
        getMovieDetailPage(movieTitleTurkish,movieDetailPageUrl)
    if not pageNumber > int(totalPageCount):
        getNextPage()

def getMovieDetailPage(movieTitle,url):
    global movies
    global moviesCount
    driver2.get(url)
    movieImg = driver2.find_element_by_xpath("//img[@class='poster']")
    movieImgUrl = movieImg.get_attribute("src")
    infoGroups = driver2.find_elements_by_xpath("//div[@class='info-group']")
    labelTitles = infoGroups[0].find_elements_by_xpath("//span[@class='label-title']")
    labels = infoGroups[0].find_elements_by_xpath("//span[@class='label']")
    description = ""
    try:
        description = driver2.find_element_by_xpath("//p[@itemprop='description']").text
    except:
        description = ""
    counter = 0
    movieDetails = {}
    for label in labels:
        title = labelTitles[counter].text.replace(":","").casefold()
        title = title.replace(" ","")
        title = title.replace("İ","i")
        title = title.replace("ü","u")
        title = title.replace("ö","o")
        title = title.replace("ı","i")
        movieDetails[title] = label.text
        counter = counter+1

    movies[moviesCount] = {"filmAdi": movieTitle,"poster": movieImgUrl,"details":movieDetails,"description":description}
    moviesCount += 1

def getNextPage():
    global driver
    global pageNumber
    global totalPageCount
    nextBtn = driver.find_element_by_xpath("//li[a/@class='pure-button next']")
    if not pageNumber == int(totalPageCount):
        print(totalPageCount," sayfadan ",pageNumber,". sayfa tamamlandı, sıradaki sayfaya geçiliyor.")
        pageNumber += 1
        nextBtn.click()
        collectListPageData()
    else:
        print(totalPageCount," adet sayfanın taraması tamamlandı.")
        saveScan()

def saveScan():
    global movies
    global moviesCount
    global totalPageCount
    driver.close()
    driver2.close()
    print("Tarama sonucu kayıt edildi.")
    with open("sonuc.json", 'a', encoding='utf8', errors='ignore') as jsonFile:
        encoded_str = json.dumps(movies)
        jsonFile.write(encoded_str)

startScan()
