# 덤보의 단어 바다 — 공개 자료

앱 소개, 개인정보 문서, 광고 판매자 파일, 버전 안내를 관리해요.
어린이 전용이 아닌 영어 단어 학습 러너이며 성인의 학습·복습도 포함해요.
확장 어휘를 제공하되 특정 시험 대비나 어휘 등급은 검수 없이 보장하지 않아요.
2026-10-05 개인정보처리방침·지원 안내를 정식본으로 바꾸고 GitHub Pages로 공개했어요.

## 파일

| 파일 | 용도 | 현재 상태 |
|---|---|---|
| index.html / styles.css | 앱 소개·마케팅 | 공개(스토어 링크는 등록 후) |
| privacy/index.html | 개인정보처리방침 | **정식본**, 시행일 2026-10-05. 앱 안 `assets/legal/privacy_ko.txt` 와 같은 내용 |
| support/index.html | 지원 안내 | 문의 nekarose@gmail.com |
| app-ads.txt | 광고 판매자 정보 | pub-9055371492725478. 실제로 읽히는 건 루트 nekarose.github.io/app-ads.txt(이미 같은 줄) |
| version.json | iOS/Android 버전 안내 | enabled=false, storeUrl=null |
| tools/validate.py | 로컬 파일 검증 | 표준 Python만 사용 |

실행: `python3 tools/validate.py`
미리보기: `python3 -m http.server 8080` 후 브라우저에서 localhost:8080을 열어요.

## 웹사이트 연결

공용 `nekarose.github.io` 저장소는 이미 존재하며 이번 작업에서 수정하지 않았어요.
이 저장소를 GitHub Pages 프로젝트 사이트로 발행하면 기본 경로는
`https://nekarose.github.io/dumbo-words-site/`예요. 2026-10-05 Pages를 켰어요(main 브랜치 루트).

프로젝트 경로의 app-ads.txt만으로 AdMob의 도메인 루트 조회를 충족했다고 주장하지 않아요.
다음 중 하나를 결정한 뒤 배포해요.

1. 별도 커스텀 도메인을 이 저장소 Pages에 연결해 루트 /app-ads.txt를 제공해요.
2. 기존 공용 사이트 관리자의 승인을 받아 루트 app-ads.txt와 앱별 공개 경로를 연결해요.

소개 주소를 스토어의 웹사이트/마케팅 필드에 등록하고 개인정보·지원 주소는 각각 맞는 필드에 등록해요.
실제 HTTPS 응답과 AdMob 수집 완료를 별도로 확인해요.

## 개인정보처리방침 고치기

앱 동작(저장 항목·SDK·동의 변경 방법)이 바뀌면 이 페이지와 앱 안 문서를 같이 고치고 시행일을 갱신해요.
지금은 계정 없는 로컬 학습 기록, AdMob(전체 이용가), 기기 TTS뿐이고 Firebase·애널리틱스·결제는 없어요.

## app-ads.txt

AdMob 콘솔이 제공하는 이 계정의 실제 게시자 선언문을 넣어요.
앱 ID/배너 단위 ID와 게시자(pub-...) ID는 달라요.
현재 주석만 있는 파일은 운영에 사용할 수 없어요. 임의 또는 Google 시험 ID로 채우지 않아요.

## 업데이트 JSON 규칙

`enabled=false`는 앱이 업데이트 안내를 건너뛰어야 한다는 뜻이에요.
앱에서 이 JSON을 읽는 기능은 아직 구현되지 않았어요. 파일 게시만으로 설치 앱이 갱신되지 않아요.

- schemaVersion: 지원하는 스키마(현재 1).
- appId: 앱 논리 식별자 dumbo_words.
- updatedAt: 마지막 수정 날짜(YYYY-MM-DD).
- platforms.ios / android: 각 플랫폼의 독립적인 버전 정보.
- latestVersion: 화면 표시용 x.y.z.
- latestBuild: 비교 기준인 정수 빌드 번호.
- minimumSupportedBuild: 지원하는 최소 빌드. latestBuild 이하여야 해요.
- storeUrl: 정식 Apple/Google 스토어 주소. 출시 준비 중에는 null.
- forceUpdate: 초기 false. 최소 빌드 미달일 때만, 명시적 운영 결정 후 사용해요.
- releaseNotes: 안내 문장 배열.

정식 버전 스토어 배포가 확인된 후 해당 플랫폼의 latestVersion/latestBuild/storeUrl을 갱신해요.
버전 문자열을 사전식으로 비교하지 않고 빌드 정수로 비교해요.
향후 앱은 HTTPS·앱 식별자·스키마·플랫폼·공식 스토어 호스트를 검증하고
오프라인/타임아웃/404/잘못된 JSON이면 정상 실행을 계속해야 해요.
앱 실행 코드를 내려받거나 자동 설치하는 용도가 아니에요.
단어 콘텐츠 원격 갱신은 별도 검수/호환/롤백 설계가 필요해요.

## 공개 전 필수

- [x] 문의처·시행일과 정식 정책 확정 (2026-10-05)
- [x] 대상 연령: 13세 이상·전체 이용가 광고, 진단 서비스 없음
- [x] 게시자 선언: 루트 https://nekarose.github.io/app-ads.txt 에 pub-9055371492725478 이 이미 있어요. 스토어 웹사이트는 https://nekarose.github.io/dumbo-words-site/
- [ ] 정식 스토어 URL과 공개 버전 확인
- [x] Pages 설정 및 HTTPS·링크 응답 검증 (커스텀 도메인은 app-ads.txt 결정 때)
- [ ] 앱 설정 링크/버전 JSON 클라이언트 연결
- [ ] 스토어 개인정보 신고·지원/마케팅/정책 URL 등록

## 참고

- [Apple 심사 기준](https://developer.apple.com/app-store/review/guidelines/)
- [Google Play 가족 정책](https://support.google.com/googleplay/android-developer/answer/9893335?hl=en)
- [AdMob 판매자 파일](https://support.google.com/admob/answer/9363762?hl=en)
- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
