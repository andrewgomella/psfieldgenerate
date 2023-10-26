"""
download json of RDE from rsna.org/radelement
this will download them into your local directory in subfolders named /sets and /elements. 
"""
import requests
import json
import logging
import time


def downloadRDE(url, outputFolder="", maxRdeNum=200):
    projectid = 1  # initiate value for projectid
    while True:
        try:
            d = requests.request('GET', url + str(projectid), allow_redirects=False)
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
        time.sleep(1) # reasonable waiting time to prevent overloading radelement.org
        print(projectid)
        print(type(projectid))
        if projectid == maxRdeNum:
            # there are currently ~1331 elements, stop early for now
            break


if __name__ == "__main__":
    seturl = 'https://api3.rsna.org/radelement/v1/sets/'
    downloadRDE(seturl, outputFolder='.\\sets\\')
    elementurl = 'https://api3.rsna.org/radelement/v1/elements/'
    downloadRDE(elementurl, outputFolder='.\\elements\\')
