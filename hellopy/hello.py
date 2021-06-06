from playwright.sync_api import sync_playwright
import time
import sys
import re

class WebScrape(object):

    def __init__(self, parcel = None):
        self.parcel = parcel

    def insert_scraping(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://permits.placer.ca.gov/CitizenAccess/Default.aspx")
            # time.sleep(10)
            iframe = page.wait_for_selector('#ACAFrame').content_frame()
            table = iframe.wait_for_selector('#ctl00_PlaceHolderMain_TabDataList_TabsDataList_ctl01_LinksDataList_ctl00_LinkItemUrl')
            table.click()
            iframe = page.wait_for_selector('#ACAFrame').content_frame()
            # iframe.wait_for_load_state()
            iframe.wait_for_selector('#ctl00_PlaceHolderMain_generalSearchForm_txtGSParcelNo')
            iframe.fill('#ctl00_PlaceHolderMain_generalSearchForm_txtGSParcelNo', self.parcel)
            table = iframe.wait_for_selector('#ctl00_PlaceHolderMain_btnNewSearch')
            table.click()
            iframe = page.wait_for_selector('#ACAFrame').content_frame()
            table = iframe.wait_for_selector('#lnkMoreDetail')
            table.click()
            apply = iframe.wait_for_selector('#imgASI')
            apply.click()
            apply_2 = iframe.wait_for_selector('#imgParcel')
            apply_2.click()
            permit_number = iframe.wait_for_selector('#ctl00_PlaceHolderMain_lblPermitNumber').inner_text()
            applicant_name = iframe.wait_for_selector('.contactinfo_fullname').inner_text()
            work_location = iframe.wait_for_selector('.NotBreakWord').inner_text()
            work_place = re.sub(r"\n", " ", work_location)
            data={}
            data['Permit Number']= permit_number
            data['Applicant Name']= applicant_name
            data['Work Location']= work_place

            print(data)
            # time.sleep(10)

            print(table.inner_text())
            print(page.title())
            browser.close()


if __name__ == "__main__":
    print("### Building permit info for Placer County ###")
    print("Parcel number is : ", sys.argv[1])
    print("Looking up, building permits...")
    parcel_number = str(sys.argv[1])
    web_scrape = WebScrape(parcel = parcel_number)
    web_scrape.insert_scraping()


# print("### Building permit info for Placer County ###")

# parcel_number = input("please enter a parcel number : ")

# print("Parcel number is : ", parcel_number)

