from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
Us_States_Number_List=[1,
2,
4,
5,
6,
7,
8,
9,
10,
12,
13,
15,
16,
17,
18,
19,
20,
21,
22,
23,
25,
26,
27,
28,
29,
30,
31,
32,
33,
34,
35,
36,
37,
38,
39,
41,
42,
43,
45,
79,
47,
48,
49,
50,
51,
52,
54,
55,
56,
57,
58]
# Create a new instance of the Firefox driver
driver = webdriver.Chrome()

# Navigate to the website
driver.get("https://www.endocrinesurgery.org/surgeon-finder-2#/")

# Wait for the page to load
driver.implicitly_wait(10)

# Select the state option
# Wait for the state select element to be visible and enabled
state_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, '6-field')))

# Define the state select element as a Select object
state_select = Select(state_select)

# Select the state option
state_select.select_by_value('1')  # Replace '1' with the value of the state you want to select
#time.sleep(10)

#SO THIS WORKS, now we just have to click search

# Click the search button
search_button = driver.find_element(By.XPATH, '//a[contains(@class, "gen-button") and contains(text(), "Search")]')
search_button.click()
#IT WORKED I CAN SEE IT

# Wait for the search results to load
driver.implicitly_wait(10)
#time.sleep(2)
# Get all the doctor elements

doctor_elements =  driver.find_elements(By.CLASS_NAME, 'search-profile')
#print(doctor_elements)

# Initialize empty lists for doctor data
names = []
addresses = []
phones = []
faxes = []
emails = []
patient_websites = []
clinical_interests = []
specialties = []

# Iterate over each doctor element and extract the data
# Iterate over each doctor element and extract the data
driver.implicitly_wait(10)
print("TEST HELP")
for doctor in doctor_elements:
    try:
        name = doctor.find_element(By.CSS_SELECTOR,'.ds-contact-name p strong span').text
        address = doctor.find_element(By.CSS_SELECTOR,'.ds-left div:nth-child(2) span').text
        phone = doctor.find_element(By.CSS_SELECTOR,'.ds-right div:nth-child(1) span span').text.split(": ")[1]
        try:
            fax_element = doctor.find_element(By.CSS_SELECTOR,'.ds-right div:nth-child(2) span span')
            fax = fax_element.text.split(": ")[1] if "Fax" in fax_element.text else ''
        except:
            fax = ''
        email = doctor.find_element(By.CSS_SELECTOR,'.ds-right div:nth-child(3) a').text
        clinical_interest = doctor.find_element(By.CSS_SELECTOR,'.ds-footer div:nth-child(2) span span').text.split(": ")[1]
        specialty = doctor.find_element(By.CSS_SELECTOR,'.ds-footer div:nth-child(3) span span').text
        
        # Check if patient website element is present
        patient_website_elem = doctor.find_elements(By.CSS_SELECTOR,'.ds-footer div:nth-child(1) a')
        if len(patient_website_elem) > 0:
            patient_website = patient_website_elem[0].text
        else:
            patient_website = ''
        
        names.append(name)
        addresses.append(address)
        phones.append(phone)
        faxes.append(fax)
        emails.append(email)
        patient_websites.append(patient_website)
        clinical_interests.append(clinical_interest)
        specialties.append(specialty)
    except:
        continue



# Create a Pandas DataFrame with the extracted data
df = pd.DataFrame({
    'Name': names,
    'Address': addresses,
    'Phone': phones,
    'Fax': faxes,
    'Email': emails,
    'Patient Website': patient_websites,
    'Clinical Interest': clinical_interests,
    'Specialty': specialties
})

# Save the DataFrame as a CSV file
df.to_csv('doctor_data.csv', index=False)

# Close the browser
driver.quit()
