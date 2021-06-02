from playwright.sync_api import sync_playwright
import time
import sys

print("### Building permit info for Placer County ###")
print("Parcel number is : ", sys.argv[1])
print("Looking up, building permits...")
parcel_number = str(sys.argv[1])
# print("### Building permit info for Placer County ###")

# parcel_number = input("please enter a parcel number : ")

# print("Parcel number is : ", parcel_number)

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
    iframe.fill('#ctl00_PlaceHolderMain_generalSearchForm_txtGSParcelNo', parcel_number)
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
    data={}
    data['Permit Number']= permit_number
    data['Applicant Name']= applicant_name
    data['Work Location']= work_location

    print(data)
    time.sleep(10)

    print(table.inner_text())
    print(page.title())
    browser.close()