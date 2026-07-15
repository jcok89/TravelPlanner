import http.server
import socketserver
import os

PORT = 8999
# 이 스크립트가 있는 폴더(리포지토리 루트)를 기본 디렉토리로 설정하여
# 루트 index.html 허브와 하위의 여러 여행 폴더를 모두 서빙합니다.
# 실행: python server.py  →  http://localhost:8999
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

print(f"✈️ 통합 여행 허브 웹 서버가 포트 {PORT}에서 실행을 준비합니다...")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"✅ 통합 서버 실행 완료: http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("\n서버가 종료되었습니다.")
