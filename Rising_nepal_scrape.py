import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
from selenium import webdriver
from time import sleep
import re



class Page:
    def __init__(self ,path='/home/lazar/Desktop/'): 
        
        
        self.path = path
        self.driver = webdriver.Chrome(executable_path='C:/Users/my pc/chromedriver_win32/chromedriver.exe') #Change this to your ChromeDriver path.
        self.error = False
        self.main_url = 'http://therisingnepal.org.np'
        self.driver.get(self.main_url)        
        self.different_category()
        self.category="World"
        sleep(1)
        self.driver.close()






    def different_category(self,):
        category_no=[5,8,1,2,7]      
          
        for item in category_no:
            ###To Find the category
            if item==5:
                category="World"
            if item==8:
                category="Headline"
            if item==1:
                category="Nation"
            if item==2:
                category=="Business"
            if item==7:
                category="Sports"
            self.category=category

            ###browse through various pages
            self.url='http://therisingnepal.org.np/category/'+str(item)
            self.driver.get(self.url)
            sleep(3)

            ###collects all the url link of the respective category
            self.get_page()
            sleep(3)





###collects all the url link of the respective category
    def get_page(self,):

        soup = BeautifulSoup(self.driver.page_source,'lxml')
        urls=[]
        count=0
        while True:
            count+=1
            if count==4:
                break
            links=soup.find_all('div',id='cat-news-item')
            for item in links:
                urls.append(item.find('a').get('href'))
            try:
                next_page=self.driver.find_element_by_xpath('/html/body/div[4]/section/div[5]/div[1]/div/div[3]/ul/li[4]/a')
                next_page.click()
            except:
                next_page=self.driver.find_element_by_xpath('//*[@id="pagination"]/ul/li[6]/a')
                next_page.click()
            
            sleep(3)
            soup = BeautifulSoup(self.driver.page_source,'lxml')
            
        self.Find_info(urls)




###Goes to every article and looks for all the required
    def Find_info(self,urls):
        for item in urls:
            self.post=item
            self.driver.get(self.post)
            soup=BeautifulSoup(self.driver.page_source,'lxml')

            ########INFORMATIONS REQUIRED FOR THE DATABASE###############################

            ### For TITLE of the news

            Headline=soup.find('div',class_="panel-heading").text




            ### For the CONTENT of the news

            contents=soup.find('div',class_="panel-body").find_all('p')
            content=''
            sentences=[]
            for item in contents:
                content=content+item.text
                sentences.append(content.split('. '))
                
                
               

            ##############################to find DATE##############################
            #to find DATE
            #to find DATE

            ###Two paragraphs are combined as in some articles date is in second paragraph
            if len(contents)>=2:
                text1=contents[0].text
                text2=contents[1].text
                text=text1+text2
            else:
                text=contents[0].text
            
            ###Searching for : or - to find the date ; date is between , and (:|-)
            
            if "—" in text:
                colonPosition=text.find('—')
            elif ":" in text:
                colonPosition=text.find(':')
            else:
                colonPosition=-1
            
            step=int(colonPosition)-1
            if step==-2:
                date="0000-00-00"
            else:
                flag=1
                while True:
                    if step==0:
                        flag=0
                        break
                    if text[step]==',':
                        commaposition=step
                        break
                    step=step-1
                step=int(colonPosition)-1

                ###ERROR###
                #numbers=['0','1','2','3','4','5','6','7','8','9']
                #while True:                    
                 #   if step==0:
                  #      flag=0
                   #     break
                    #for item in numbers:
                     #   if text[step]==item:
                      #      dateposition=step
                       #     break
                    #step=step-1

                while True:                    
                    if step==0:
                        flag=0
                        break
                    if (text[step]=='0' or text[step]=='1' or text[step]=='2' or text[step]=='3' or text[step]=='4' or text[step]=='5' or text[step]=='6' or text[step]=='7' or text[step]=='8' or text[step]=='9'):
                        dateposition=step
                        break
                    step=step-1
               
                if flag==0:
                    date_default='0000-00-00'
                else:
                    date_default=text[commaposition+2:dateposition+1]
                
                
                if len(date_default)>20 and len(date_default)>5:
                    date="0000-00-00"
                else:
                    date=date_default
                
                year=['July','June','Jan','Feb','April','May','August','Oct','Nov','Dec','Mar','Sep']
                year_2019=['July','June','Jan','Feb','April','May','Mar']
                
                for item in year:
                    if item in date:
                        for item_year in year_2019:
                            if item_year in date:
                                date_withyear=date+",2019"
                                break
                            else:
                                date_withyear=date+",2018"
                        break
                                
                    else:
                        date_withyear="no date given"
                    ## To correct some typos in some article ##         
                    date_withyear=date_withyear.replace(".","")
                    date_withyear=date_withyear.replace("Mar","March")
                            
                        
                print(date_withyear)

                ##########################################END of DATE######################## 
                




                    #For the CATEGORY OF NEWS, Category is already separated in different_category page                   




                print(self.category)


            


if __name__=='__main__':
    page=Page()





