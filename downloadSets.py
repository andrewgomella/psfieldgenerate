"""
download json of RDE from rsna.org/radelement
"""
import requests
import json
import logging
import time


def downloadRDE(url, outputFolder=""):
    projectid = 1  # initiate value for projectid
    while True:
        try:
            # _url = url + str(projectid)
            # print(url)
            d = requests.request('GET', url + str(projectid), allow_redirects=False)
            # data = d.json()["data"]
            data = d.json()
            print(data)
            rdeName = data["data"]["id"]
            print('\t' + rdeName)
            with open(outputFolder + rdeName + ".json", "w+") as outfile:
                json.dump(data, outfile)
        except requests.HTTPError:
            logging.error('HTTPError')
        except Exception as e:
            print(e)
            logging.error('Unknown exception')
        projectid += 1
        time.sleep(0.2)
        print(projectid)
        print(type(projectid))
        if projectid == 200:
            # there are currently 1331 elements, stop early for now
            break


if __name__ == "__main__":
    seturl = 'https://api3.rsna.org/radelement/v1/sets/'
    downloadRDE(seturl, outputFolder='.\\sets\\')
    elementurl = 'https://api3.rsna.org/radelement/v1/elements/'
    downloadRDE(elementurl, outputFolder='.\\elements\\')
