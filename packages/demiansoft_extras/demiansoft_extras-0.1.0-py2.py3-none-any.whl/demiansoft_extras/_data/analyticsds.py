"""
1. 네이버 애널리틱스
    - https://analytics.naver.com/ 에서 아이디 발급후 naver_id 변수에 입력
2. 구글 애널리틱스
    - https://analytics.google.com/ 에서 계정 및 속성 생성후 google_id 변수에 입력
3. 구글 애즈
    - ads_id 및 conversion_click, conversion_pageload 변수는 전환추적에 이용한다.
    - https://ads.google.com/ 에서 전환을 생성하여 태그를 생성하여 이벤트 스니펫 코드를 등록한다.
    (목표 - 전환 - 요약 - 전환 아이템에서 태그 설정)

conversion_click dict 형식 의미
추적을 원하는 링크를 <a href> 형식이 아닌 <a onclick> 형식으로 제작하여 onclick에
{{ key }}_gtag_report_conversion(url) 형식으로 함수를 호출한다.

- cta 및 calling section 수정(함수 이름 맞추기)이 필요하다.
"""

context = {
    'analytics': {
        'google_id': "G-BYZ2M4WE1L",
        'naver_id': "2fecdf0545d4d6",
        'ads_id': "AW-1018052709",
        'conversion_click': {
            # cta 버튼 수에 맞춰서 추가 한다.
            'cta1': "91WCCPvk6fEBEOWAueUD",  # 네이버 예약
            'cta2': "psz_CNiCwYoYEOWAueUD",  # 네이버 톡톡
            'calling': "pThXCJXpsN8DEOWAueUD",
        },
    },
}
