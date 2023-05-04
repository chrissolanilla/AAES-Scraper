from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

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
state_select = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, '6-field')))

# Define the state select element as a Select object
state_select = Select(state_select)
# Initialize empty lists for doctor data
names = []
addresses = []
phones = []
faxes = []
emails = []
patient_websites = []
clinical_interests = []
specialties = []
#ccount all teh dcocotrs
doctor_count = 0
def wait_for_state_select(driver, timeout=30):
    try:
        return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.ID, '6-field')))
    except TimeoutException:
        return None
# Iterate over each state in the Us_States_Number_List
for state_number in Us_States_Number_List:
   try:
        # Select the state option
        state_select = state_select_elem = wait_for_state_select(driver)
        
        if state_select_elem is None:
            print(f"State select not clickable for state {state_number}, refreshing the page and retrying...")
            driver.refresh()
            state_select_elem = wait_for_state_select(driver)

        # Define the state select element as a Select object
        state_select = Select(state_select)

        print("test")
        state_select.select_by_value(str(state_number))
        # Click the search button
        search_button = driver.find_element(By.XPATH, '//a[contains(@class, "gen-button") and contains(text(), "Search")]')
        search_button.click()
        driver.implicitly_wait(10)

        doctor_elements =  driver.find_elements(By.CLASS_NAME, 'search-profile')
        no_email_losers=0
        driver.implicitly_wait(10)
        print("TEST HELP")
        for doctor in doctor_elements:
            doctor_count+=1
            print(f"Currently on doctor {doctor_count}")
            try:
                name = doctor.find_element(By.CSS_SELECTOR,'.ds-contact-name p strong span').text
                try:
                    address = doctor.find_element(By.CSS_SELECTOR,'.ds-left div:nth-child(2) span').text
                except:
                    address= ''
                try:
                    phone = doctor.find_element(By.CSS_SELECTOR,'.ds-right div:nth-child(1) span span').text.split(": ")[1]
                except:
                    phone=''
                try:
                    fax_element = doctor.find_element(By.CSS_SELECTOR,'.ds-right div:nth-child(2) span span')
                    fax = fax_element.text.split(": ")[1] if "Fax" in fax_element.text else ''
                except:
                    fax = ''
                email = doctor.find_element(By.CSS_SELECTOR,'.ds-right div:nth-child(3) a').text
                try:
                    clinical_interest = doctor.find_element(By.CSS_SELECTOR,'.ds-footer div:nth-child(2) span span').text.split(": ")[1]
                except:
                    clinical_interest= ''
                    print("doctor has no email")
                    no_email_losers+=1
                #none of these doctors list a speciality
                try:
                    specialty = doctor.find_element(By.CSS_SELECTOR,'.ds-footer div:nth-child(3) span span').text
                except:
                    specialty=''
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
        driver.get("https://www.endocrinesurgery.org/surgeon-finder-2#/")
   except Exception as e:
        print(f"error :( with state {state_number}: {e}")
        continue
    
   finally:
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
        df.to_csv('doctor_data.csv', index=False)
        
    
    
        
    
# Wait for the search results to load

#time.sleep(2)
# Get all the doctor elements


#print(doctor_elements)


# Iterate over each doctor element and extract the data
# Iterate over each doctor element and extract the data




# Create a Pandas DataFrame with the extracted data
print(f"Total doctors processed: {doctor_count}")
print(f"total doctos with no emails is {no_email_losers}")
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
