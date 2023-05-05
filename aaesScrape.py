from selenium import webdriver
from selenium.webdriver.support.ui import Select
import traceback
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
# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the website
driver.get("https://www.endocrinesurgery.org/surgeon-finder-2#/")

# Wait for the page to load
driver.implicitly_wait(5)

# Select the state option
# Wait for the state select element to be visible and enabled
state_select = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, '6-field')))

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
        print(f"error: state select element not found")
        return None
    
    
def get_doctor_data_from_elements(doctor_elements):
    doctor_data = []
    for doctor in doctor_elements:
        try:
            name = doctor.find_element(By.CSS_SELECTOR,'.ds-contact-name p strong span').text
            try:
                #this gets all the doctors addresses but excludes the last country line, multiple lines in this address thing
                address_lines = doctor.find_elements(By.CSS_SELECTOR, '.ds-left div.ng-scope > span')
                address = ', '.join([line.text for line in address_lines[:-1]])  # Exclude the last line (country)
                            
                print(f"{name} 's address is {address}")
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
            try:
                email = doctor.find_element(By.CSS_SELECTOR,'.ds-right div:nth-child(3) a').text
            except:
                print("doctor has no email")
                no_email_losers+=1
            try:
                clinical_interest = doctor.find_element(By.CSS_SELECTOR,'.ds-footer div:nth-child(2) span span').text.split(": ")[1]
            except:
                clinical_interest= ''
                                
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
            #this just appends all of our data combined so we can dataframe it in pandas
            doctor_data.append({
                'Name': name,
                'Address': address,
                'Phone': phone,
                'Fax': fax,
                'Email': email,
                'Patient Website': patient_website,
                'Clinical Interest': clinical_interest,
                'Specialty': specialty
            })
                            
        except:
            continue


        
    return doctor_data
done=0
count=0
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

        #print("test")
        state_select.select_by_value(str(state_number))
        # Click the search button
        search_button = driver.find_element(By.XPATH, '//a[contains(@class, "gen-button") and contains(text(), "Search")]')
        search_button.click()
        

        doctor_elements =  driver.find_elements(By.CLASS_NAME, 'search-profile')
        no_email_losers=0
        
        print(f"currently on state {state_number} ")
        if(done>0):
            print("test if we ever get here")
            #driver.get("https://www.endocrinesurgery.org/surgeon-finder-2#/")
            done=0
        #set this to none at first 
        prev_doctor_data=None
        #need to a while true so that i can navigate multiple pages of the state
        while True:
            doctor_elements =  driver.find_elements(By.CLASS_NAME, 'search-profile')
            doctor_data= get_doctor_data_from_elements(doctor_elements)
            
            if prev_doctor_data is not None and doctor_data==prev_doctor_data:
                print("same data!")
                done+=1
                print("reFRESH!")
                driver.get("https://www.endocrinesurgery.org/surgeon-finder-2#/")
                break
            #process doctor data
            else:
                prev_doctor_data=doctor_data
                next_button=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID, 'next')))
                next_button.click()
                doctor_elements= driver.find_elements(By.CLASS_NAME, 'search-profile')
            
            #I have NO IDEA what this does for my code    
            if doctor_data is not None:
                print("doctorData is not None")
                for doctor in doctor_data:
                    names.append(doctor['Name'])
                    addresses.append(doctor['Address'])
                    phones.append(doctor['Phone'])
                    faxes.append(doctor['Fax'])
                    emails.append(doctor['Email'])
                    patient_websites.append(doctor['Patient Website'])
                    clinical_interests.append(doctor['Clinical Interest'])
                    specialties.append(doctor['Specialty'])
                #assing stuff
                
                #click next button
            next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'next')))
            driver.execute_script("arguments[0].scrollIntoView(true);",next_button)
            time.sleep(5)
            #next_button.click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-profile')))
            #update to go to next iteration
            prev_doctor_data=doctor_data

   except Exception as e:
        print(f"error :( with state {state_number}: {e}")
        traceback.print_exc()
        continue
    
   finally:
        print("FINALLY IM OUT")
        done+=1
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
