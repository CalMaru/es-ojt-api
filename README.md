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

