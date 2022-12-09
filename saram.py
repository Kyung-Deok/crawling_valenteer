from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import re
from random import randint

import time
from datetime import datetime
import pandas as pd

print(
    "******** 사람인 정보 탐색기 입니다. ",
    "******** 검색어를 입력하면 해당 검색어에 맞는 공고에서 정보를 가져옵니다.",
    "******** 완료 메세지가 해당 창에 뜨기 전까지 컴퓨터를 끄거나 절전모드로 전환하지 마세요. ",
    "*********강제 종료 시 처음부터 다시 실행 되기 때문에 데이터가 중복으로 발생하게 됩니다. ",
    "******** 해당 프로그램은 최근 기준 40개 씩 하나의 엑셀파일에 넣습니다.",
    "******** 프로그램이 실행되며 기존 파일에 덮어쓰기 되는 것을 방지하고자 설정해 놓았습니다. ",
    "************ 원본 코드 : saram.py ",
    "\n",
    "!!!!!! 경고 : 자동으로 생기는 크롬 창을 절대 닫지 마세요.",
    sep="\n"
    
)

search_word = str(input("** 검색어를 입력하세요 : "))
start_page = int(input("** 몇 번째 페이지부터 수집할까요?(숫자만 적어주세요. 오류납니다.) : "))
end_page = int(input("** 몇 번째 페이지까지 수집할까요?(숫자만 적어주세요. 오류납니다.) : "))

recruit_lst = []
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try :
    for i in range(start_page, end_page+1):
        driver.get(f'https://www.saramin.co.kr/zf_user/search/recruit?search_area=main&search_done=y&search_optional_item=n&searchType=recently&searchword={search_word}&recruitPage={i}&recruitSort=relation&recruitPageCount=40&inner_com_type=&quick_apply=&except_read=&ai_head_hunting=&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&show_applied=&mainSearch=n')
        # 밑에꺼는 테스트
        # driver.get(f"https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=recently&searchword=%EB%B3%B4%EA%B1%B4%EA%B4%80%EB%A6%AC%EC%82%AC%20%EC%82%AC%EB%9E%8C%EC%9D%B8%EC%97%90%EC%9D%B4%EC%B9%98%EC%97%90%EC%8A%A4&loc_mcd=101000%2C102000&recruitPage={i}&recruitSort=relation&recruitPageCount=40")
        time.sleep(randint(2,6))

        # 
        recruit = driver.find_element(By.ID,'container')
        titles = recruit.find_elements(By.CLASS_NAME,'job_tit')
        
        for j in range(len(titles)) :
            recruit_dic = {}
            click = titles[j].find_element(By.CSS_SELECTOR,'a.data_layer')
            link = click.get_attribute("href")
            
            click.send_keys(Keys.ENTER)
            
            time.sleep(randint(3,6))
            
            driver.switch_to.window(driver.window_handles[-1]) # 새 탭으로 이동
            # ## 여기서 크롤링 진행
            driver.get(link)
            time.sleep(randint(3,6))
            corp_name = driver.find_element(By.XPATH,"/html/body/div[3]/div/div/div[3]/section[1]/div[1]/div[1]/div/div[1]/a[1]")
            corp_manager= driver.find_elements(By.CSS_SELECTOR, "body > #sri_section > #sri_wrap > #content > div.wrap_jview > section.jview > div.wrap_jv_cont > div.jv_cont.jv_howto > div.cont.box > dl.guide > dd.manager")
            # 추가로 메일도 있다. 
            corp_call = driver.find_elements(By.CSS_SELECTOR, "body > #sri_section > #sri_wrap > #content > div.wrap_jview > section.jview > div.wrap_jv_cont > div.jv_cont.jv_howto > div.cont.box > dl.guide > dd.info")
            try : 
                corp_mail = [driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/section[1]/div[1]/div[6]/div/dl/dd[4]/span | /html/body/div[3]/div/div/div[3]/section[1]/div[1]/div[6]/div/dl/dd[5]/span").text]
            except NoSuchElementException as err :
                corp_mail = []
                iframes = driver.find_element(By.ID, "iframe_content_0")
                driver.switch_to.frame(iframes)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                
                kk = soup.find('div',class_='user_content').get_text()

                corp_mail_zero= re.findall(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}',kk, flags=re.IGNORECASE)
                corp_mail.append(corp_mail_zero)

                driver.switch_to.default_content()
                if len(corp_mail) ==0 :
                    corp_mail.append(corp_name)
            
            
            if len(corp_manager) == 0 : 
                corp_manager.append(corp_name)
            if len(corp_call) == 0 : 
                corp_call.append(corp_name)

            try : 
                corp_loc = driver.find_element(By.CSS_SELECTOR,"#map_0 > div > address > span.spr_jview.txt_adr")
            except NoSuchElementException as err :
                try : 
                    corp_loc = driver.find_element(By.CSS_SELECTOR,"#content > div.wrap_jview > section.jview.jview-0-44276737 > div.wrap_jv_cont > div.jv_cont.jv_company > div:nth-child(3) > div.wrap_info > div.info > dl.wide > dd")
                except NoSuchElementException as err :
                    corp_loc = corp_name
        
            recruit_dic['회사 명'] = corp_name.text
            recruit_dic['담당자'] = corp_manager[0].text
            recruit_dic['담당자 연락처'] = corp_call[0].text
            recruit_dic['담당자 이메일'] = corp_mail[0]
            recruit_dic['회사 주소'] = corp_loc.text
            
            
            recruit_lst.append(recruit_dic)
            print(f"회사명 : {corp_name.text} / 연락처 : {corp_call[0].text} / 메일 : {corp_mail[0]}")

            time.sleep(randint(3,6))
            # ## 여기까지 크롤링
            
            driver.close()
            time.sleep(randint(2,6))
            driver.switch_to.window(driver.window_handles[-1])  #다시 이전 창(탭)으로 이동
            time.sleep(randint(2,6))
        
        dates = datetime.now().strftime("%Y%m%d")
        df = pd.DataFrame(recruit_lst)
        df.to_excel(f"크롤링_{i}_페이지본_{dates}.xlsx", index=False, encoding="utf-8-sig")
        print("********************* 저장완료 ! 이제 조금만 더 기다려주세요. ************************")


finally :
    print("************************* 최종완료 ! 이제 컴퓨터를 꺼도 좋습니다 **************************")
    driver.quit()
    
