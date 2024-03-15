from selenium import webdriver
from selenium.webdriver.common.by import By 

class focus :

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        
        options = webdriver.EdgeOptions()
        options.add_argument('--headless')
        driver = webdriver.Edge(options=options)
    
        driver.get("https://focus.pcsb.org/focus/Modules.php?modname=misc/Portal.php")

        driver.find_element(by=By.ID, value="username-input").send_keys(username)
        driver.find_element(by=By.NAME, value="password").send_keys(password)
        driver.find_element(by=By.XPATH, value="/html/body/div/div[3]/div/div[1]/form/div[2]/div[2]/button").click()
        
        print("attempting login")

        while True :
            try :
                if "Permission denied" in driver.find_element(by=By.XPATH, value="/html/body/div/div[3]/div/div[1]/form/div[2]/div[1]/div[2]").text :
                    print("login wrong")
                    return driver.close() 

            except : 
                pass

            if len(driver.find_elements(by=By.XPATH, value="/html/body/div[1]/div[2]/div")) > 0 :
                print("login success")
                break

        self.driver = driver


    def getGrades(self) :
       rawGrades = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div").text
       rawGrades = str(rawGrades).split("\n")
       
       finalGrades = []

       for posGrade in rawGrades :
          indexLength = len(posGrade)
          
          if "ABC" in posGrade :
             finalGrades.append(posGrade)

          if indexLength != 0 and posGrade[indexLength -1] in ['A', 'B', 'C', 'D', 'F'] and indexLength <= 6 and "," not in posGrade :
             finalGrades.append(posGrade)
       


       grades = {}
       itera = 0
       while True :
           if not itera < len(finalGrades) : break

           grades[finalGrades[itera]] = finalGrades[itera + 1]
           itera += 2

       
       return grades


    def getSchedule(self):
        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/nav/div[1]/div[1]/a[6]").click() 

        scheduleTable = self.driver.find_element(by=By.ID, value="lo_num1").text
        
        finalList = []

        for i in scheduleTable.split("\n") :
            if i[0].isdigit() :
                continue

            finalList.append(i)

        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/nav/div[1]/div[1]/a[1]").click()
        
        
        returnStr = ""
        for i in finalList : returnStr = returnStr + i + "\n"

        return returnStr



    def studentInfo(self) :
        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/nav/div[1]/div[1]/a[3]").click()     
        
        # write exact wait while loop   
        
        while True :
            if len(self.driver.find_elements(by=By.XPATH, value="/html/body/div[1]/div[2]/div/main/div/div[5]/div/div[1]/div/div[2]/a[1]")) > 0 :
                break

        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/main/div/div[5]/div/div[1]/div/div[2]/a[1]").click()

        box = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/main/div/div[5]/div/div[2]/div[2]/div[1]/div").text

        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/nav/div[1]/div[1]/a[1]").click()

        
        return box




    def schoolInfo(self) :
        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/nav/div[1]/div[1]/a[2]").click() 
        
        while True :
            if (len(self.driver.find_elements(by=By.XPATH, value="/html/body/div[1]/div[2]/div/main/div/div[5]/div/div[2]/div[2]/div[1]"))) > 0 :
                break

        box = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/div/main/div/div[5]/div/div[2]/div[2]/div[1]").text


        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div[2]/nav/div[1]/div[1]/a[1]").click()
        return box 



    def quit(self) :
        self.driver.close()


