# crwaling_valenteer
봉사활동 중 크롤링을 활용한 업무자동화 기여


봉사활동 기간 : 12.05 ~ 12.09

봉사활동 업무 : 해당 기관 사무 보조 및 업무 지원

사용 라이브러리 : Selenium, BeautifulSoup4, Pandas, Openpyexcel, Webdriver_manager,Pyinstaller

해당 기관에서 사람인에서 정보를 조사해 수작업으로 엑셀에 기입하고 있던 업무를 크롤링 코드로 업무 자동화한 결과물입니다.

해당 기관 담당자 분들이 프로그래밍 언어에 생소해 하셨기 때문에 .exe 파일로 만들었습니다.

우선 exe로 변환을 위해 pyinstaller 라이브러리를 설치합니다.

```bash
pip install pyinstaller
```

이후 cli에 pyinstaller 명령어를 통해 해당 코드를 exe 파일로 변환합니다.

- -F : 부수적인 파일을 만들지 않고, 하나의 exe 파일로 패키징.

```bash
pyinstaller -F saram.py
```

이후 exe 파일을 돌려보면 정상적으로 작동합니다.

![program_img](./Untitled.png)
