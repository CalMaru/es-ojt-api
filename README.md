# es-ojt

## 필요 기능

1. 키워드 검색
2. 검색 옵션 - [네이버 검색 옵션](https://help.naver.com/service/5603/contents/19113?lang=ko)
   - 정렬
   - 기간
   - 언론사
   - 기자명
3. 추가 기능
   - 자동 완성
     - 기자명, 언론사명, 사용자 쿼리
   - 관련 뉴스
4. 검색 결과
   1. 네이버와 동일한 검색결과 형식 사용
   2. 화면 개발 없이 postman으로 결과 확인

## 데이터

- AI 허브 뉴스 데이터

## API

### Search API

- url: `/search`
- method: GET
- query parameters
  - query, string, required
  - sort, enum: [related, latest, oldest], default: related, required
    - related: 해당 검색어와 연관성이 높은 순서대로 정렬하여 제공
    - latest: 최신 날짜 순서대로 정렬하여 제공
    - oldest: 1990년 이후 기사를 오래된 순으로 제공
  - period, enum: [all, hour, day, week, month, year, etc], deafult: all, required
    - all: 전체
    - hour: 시간 단위
    - day: 일 단위
    - week: 주 단위
    - month: 개월 단위
    - year: 년 단위
    - etc: 사용자 지정
  - unit, int
    - hour - 1~6
    - day - 1
    - week - 1
    - month - 1, 3, 6
    - year - 1
  - start, datetime(%Y.%M.%D.%h%.%m)
  - end, datetime(%Y.%M.%D.%h%.%m)
  - press_type, enum: [all, category, detail, local, alphabetic], default: all, required
    - all: 전체
    - category: 유형별
    - detail: 언론사 분류순
    - local: 지역언론사별
    - alphabetic: 가나다순
  - press_category, int
  - press_detail: int
  - service_area, enum: [news, reporter], default: news, required
    - new: 뉴스 검색
    - reporter: 기자명 검색 - 여기 수정해야 할 듯
- response
  - 

### Press API

---

## 2024-04-29 기준

### 구현 방식

- get next scroll API
  - Search After Pagenation 방식 사용
    - 이전 페이지의 마지막 문서 값을 기반으로 쿼리 실행
  - Point In Time 사용

### get option API

- url: `/search/option`
- method: GET
- response
  - categories, list, 분류 리스트
    - key, string, 분류 기준
    - values, list(string), 분류 리스트
  - providers, list, 언론사 리스트
    - key, string, 언론사 분류 기준
    - values, list(string), 언론사 리스트

### get next scroll API

- url: `/search/scroll`
- method: GET
- 나머지 정의 필요

### Search API  - naver

- url: `/search/naver`
- method: GET
- query parameters
  - query
    - (required, string) 검색어 쿼리
  - reporter
    - (optional, string) 기자명 쿼리 
  - start_date
    - (required, datetime) 뉴스 조회 시작일
    - format: `Y-%m-%d`
  - end_date
    - (required, datetime) 뉴스 조회 마지막일
    - format: `Y-%m-%d`
  - category_type
    - (required, string) 뉴스 분류 유형
    - available types: all, 유형별, 분야별, 가나다순
      - all: 전체
      - category: 유형별
      - detail: 분야별
      - alphabetic: 가나다순
  - category_name
    - (optional, string) 뉴스 분류 이름
    - category_type이 detail, alphabetic일 경우 category_name을 입력해야 함
  - provider_type
    - (required, string) 언론사 유형
    - available types: all, 유형별, 언론사 분류순, 지역언론사별, 가나다순
      - all: 전체
      - category: 유형별
      - detail: 언론사 분류순
      - local: 지역언론사별
      - alphabetic: 가나다순
  - provider_name
    - (optional, string) 언론사 이름
    - provider_type이 detail, local, alphabetic일 경우 provider_name을 입력해야 함
  - size
    - (optional, int) 뉴스 수
    - 입력하지 않는 경우 기본 값으로 10개 반환

- response
  - 정의 필요

### ㅇㅇㅇ



