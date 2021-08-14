# Connect API

## Usage
Python 3.8.3 (Python >= 3.6)   
Library requirements.txt 참고

## Download
```
git clone https://github.com/gongul/connect-api.git
```

## Setting
순서대로 설정해주세요.

- **데이터 베이스 설정**<br/>
  MySQL를 기반으로 설정하고 있습니다 MySQL 외에 다른 DB를 설정시 Django 세팅을 바꿔주셔야 합니다.
  
  **MySQL** <br/>
  이름 변경후 MySQL 접속 정보를 입력해주시면 됩니다. <br/>
  resources/private/mysql_development.cnf.sample -> resources/private/mysql_development.cnf (rename) <br/>
  resources/private/mysql_production.cnf.sample -> resources/private/mysql_production.cnf (rename)

  ```
  [client]
  host = 127.0.0.1
  database = database
  user = user
  password = password
  default-character-set = utf8mb4
  port = 3306
  ```

- **settings.json**<br/>
  이름 변경후 MySQL 접속 정보를 입력해주시면 됩니다.

  resources/private/settings.json.sample -> resources/private/settings.json (rename) <br/>

  ```
  {
    "SECRET_KEY": "랜덤 고유키",
    "EMAIL": { // 이메일 발송 시 필요한 정보
        "HOST": "",
        "PORT": "",
        "HOST_USER": "",
        "HOST_PASSWORD": "",
        "USER_TLS": true
    }
  }
  ```

- **Virtual Env**
```
python -m venv env
```

- **Visual Studio Code 사용시 필수**
  .vscode/settings.json.sample -> .vscode/settings.json

  .vscode/settings.json
  ```
  "python.pythonPath": "가상경로 패치",
  ```

- **Library Download (Window)(이제부터 가상환경이 활성화 되어 있어야합니다.)**
  ```
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
  ```


## Run
```
python src/mange.py runserver 
```

## Lint
해당 프로젝트는 flake8를 이용하여 코드 검사는 하고 있으며 기본적으로 예외대상인 규칙들 .flake8 파일에 서술되어 있습니다.

## Third Project 
##### corn_soup : https://github.com/cookieCornSoup/simpleCommunity