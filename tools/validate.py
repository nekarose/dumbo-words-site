#!/usr/bin/env python3
"""공개 자료의 구조/링크를 검사해요. 초안의 법적 적합성을 판정하지 않아요."""
import json
import re
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
        self.korean = False
        self.viewport = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.korean = attrs.get("lang") == "ko"
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = True
        for key in ("href", "src"):
            if key in attrs:
                self.paths.append(attrs[key])


def validate_version(data):
    assert data["schemaVersion"] == 1, "지원하지 않는 스키마"
    assert data["appId"] == "dumbo_words", "다른 앱의 manifest"
    assert isinstance(data["enabled"], bool), "enabled는 불리언"
    date.fromisoformat(data["updatedAt"])
    assert set(data["platforms"]) == {"ios", "android"}
    for platform, config in data["platforms"].items():
        identity = "bundleId" if platform == "ios" else "applicationId"
        expected = "com.nekarose.dumboWords" if platform == "ios" else "com.nekarose.dumbo_words"
        assert config[identity] == expected
        assert re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", config["latestVersion"])
        latest, minimum = config["latestBuild"], config["minimumSupportedBuild"]
        assert type(latest) is int and type(minimum) is int
        assert 1 <= minimum <= latest
        assert isinstance(config["forceUpdate"], bool)
        assert isinstance(config["releaseNotes"], list) and config["releaseNotes"]
        assert all(isinstance(item, str) and item.strip() for item in config["releaseNotes"])
        url = config["storeUrl"]
        if url is not None:
            parsed = urlparse(url)
            host = "apps.apple.com" if platform == "ios" else "play.google.com"
            assert parsed.scheme == "https" and parsed.hostname == host
            assert not parsed.username and not parsed.password
        if data["enabled"]:
            assert url is not None, "운영 manifest는 정식 스토어 주소가 필요해요"
        else:
            assert not config["forceUpdate"], "준비 manifest는 강제 업데이트하지 않아요"


def main():
    data = json.loads((ROOT / "version.json").read_text(encoding="utf-8"))
    validate_version(data)
    for html in ROOT.rglob("*.html"):
        parser = Links()
        parser.feed(html.read_text(encoding="utf-8"))
        assert parser.korean and parser.viewport, html
        for link in parser.paths:
            if not link or link.startswith("#") or urlparse(link).scheme:
                continue
            target = (html.parent / link.split("#", 1)[0]).resolve()
            assert target.is_relative_to(ROOT), "공개 폴더 밖 링크"
            if target.is_dir():
                target = target / "index.html"
            assert target.is_file(), f"{html}: 없는 링크 {link}"
    entries = [line for line in (ROOT / "app-ads.txt").read_text(encoding="utf-8").splitlines()
               if line.strip() and not line.lstrip().startswith("#")]
    for entry in entries:
        assert re.fullmatch(r"google\.com,\s*pub-[0-9]{16},\s*DIRECT,\s*f08c47fec0942fa0", entry.strip()), entry
        assert "3940256099942544" not in entry, "Google 시험 게시자 ID는 운영에 쓰지 않아요"
    print("HTML 링크·모바일 메타·업데이트 JSON 구조 검사 통과")
    print("광고 파일: " + ("선언문 형식 확인(실제 소유/AdMob 수집은 별도)" if entries else "실제 게시자 선언문 입력 대기"))
    print("업데이트 안내: " + ("활성 상태(스토어 실제 배포는 별도 확인)" if data["enabled"] else "비활성 준비 상태"))
    print("정책 법률 검토·공식 문의처·Pages 배포·앱 연결은 별도 완료가 필요해요.")


if __name__ == "__main__":
    main()
