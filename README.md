# taxiRoka
## 프로젝트 개요 및 셋업
- python 3.11
- 가상환경 세팅후 requirements.txt 를 통해 필요 라이브러리 설치 (추가적으로 사용하는 라이브러리가 생길 경우 반드시 추가할 것)
  - `pip install -r requirements.txt`
- redis 설치 후 redis서버 실행 (채팅)

## 프로젝트 설명 및 주요 기능
- [기획안 링크](https://www.figma.com/file/7moP30bEJTYJeyoaSUACyt/PIRO19-ROKA?type=design&node-id=0-1&mode=design)
- [ERD CLOUD 링크](https://www.erdcloud.com/d/zB3wiAaQY7PxnzLyY)

##URL
user/main/ : 로그인 회원가입 누르는 메인창
user/signup/: 회원가입
user/login/: 로그인창
user/logout/: 로그아웃
user/send_email/: 이메일 보내기
user/activate/pk: 인증하기

matching/: 매칭 리스트
matching/create: 매칭방 생성
matching/apply/room/pk: 매칭 신청
matching/update/room/pk: 매칭방 수정
matching/delete/room/pk: 매칭방 나가기
matching/history: 매칭 히스토리

chat/room_name: 채팅방 입장
report/form: 신고하기 페이지
report/: 신고하기

## 기능 상세
- 회원 관련 기능
  - 회원가입
  - 로그인
  - 회원 정보 수정
  - 회원탈퇴

- 매칭방 관련 기능
  - 매칭방 목록
  - 매칭방 생성 (출발지점, 도착지점, 예약일시, 최대 인원, 좌석 위치 설정 필요)
  - 채팅 입장 및 퇴장
  - 유저간 채팅

- 채팅방 관련 기능
  - 채팅 입장 및 퇴장
  - 유저간 채팅

- 신고 관련 기능
  - 채팅방에서 유저명을 클릭하면 신고 모달창이 나오도록
  - 신고 모달창에서 '신고하기' 버튼을 클릭하면 신고 페이지로 이동
  - 'ROKA 팀에게 전달하기' 버튼 클릭을 통해 신고 접수

- 캘린더 관련 기능
  - 휴가 일정 등록
  - 휴가 일정 수정
  - 휴가 일정 삭제


## 현재 구현한 기능
- 회원 관련 기능
 - 회원가입
 - 이메일 인증
 - 로그인
 - 카카오로그인(수정필요)
 - 구글로그인(수정필요)

- 매칭방 관련 기능
  - 매칭방 목록
  - 매칭방 생성
  - 매칭방 수정,삭제
  - 매칭 신청

- 채팅방 관련 기능
  - 유저간 채팅
  - 채팅방 입장 및 퇴장
  - 다른 유저의 입장, 퇴장을 알려주는 메시지
  - 메시지를 전송한 사람의 이름(익명으로) 보여주기(단, 내 이름을 나한테 나타낼 필요는 없음)

- 신고 관련 기능
  - 채팅방에서 유저명을 클릭하면 신고 모달창이 나오도록
  - 신고 모달창에서 '신고하기' 버튼을 클릭하면 신고 페이지로 이동
  - 'ROKA 팀에게 전달하기' 버튼 클릭을 통해 신고 접수

- 캘린더 관련 기능

## 구현해야하는 기능
- 회원 관련 기능
   - 기본적인 css,js
   - 부대 목록 테이블로 만들기
     
- 매칭방 관련 기능
  - css,js
  - 채팅방과 연결
    
- 채팅방 관련 기능
  
- 캘린더 관련 기능
  - 휴가 일정 등록
  - 휴가 일정 수정
  - 휴가 일정 삭제
