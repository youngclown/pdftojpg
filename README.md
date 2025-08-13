# PDF to JPG Converter

PDF to JPG Converter는 PDF 파일을 고품질 JPG 이미지로 변환하는 Python 애플리케이션입니다. 단일 PDF 파일 또는 폴더 내의 여러 PDF 파일을 처리할 수 있으며, 사용하기 쉬운 그래픽 사용자 인터페이스(GUI)를 제공합니다.

## 기능

- PDF 파일을 고품질(300 DPI) JPG 이미지로 변환
- 단일 PDF 파일 또는 폴더 내의 모든 PDF 파일 처리 가능
- 각 PDF 파일의 모든 페이지를 개별 JPG 이미지로 변환
- 사용하기 쉬운 그래픽 사용자 인터페이스(GUI)
- 변환 진행 상황 및 상태 메시지 실시간 표시
- 변환 작업을 백그라운드에서 실행하여 UI 응답성 유지

## 설치 요구사항

1. Python 3.6 이상
2. 필요한 Python 패키지:
   - pdf2image
   - tkinter (대부분의 Python 설치에 기본 포함)
3. Poppler 라이브러리 (pdf2image의 의존성)

### 설치 방법

1. Python 패키지 설치:
   ```
   pip install pdf2image
   ```

2. Poppler 설치:
   - Windows: [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)에서 다운로드하여 설치
   - macOS: `brew install poppler`
   - Linux: `apt-get install poppler-utils`

3. 코드에서 Poppler 경로 설정:
   ```python
   POPPLER_PATH = "설치한 Poppler의 bin 폴더 경로"
   ```

## 사용 방법

### GUI 애플리케이션 사용

1. 스크립트 실행:
   ```
   python pdf_to_jpg.py
   ```

2. "폴더 선택" 버튼을 클릭하여 PDF 파일이 있는 폴더를 선택합니다.
3. "PDF를 JPG로 변환" 버튼을 클릭하여 변환 프로세스를 시작합니다.
4. 변환 진행 상황과 상태 메시지가 실시간으로 표시됩니다.
5. 변환된 JPG 파일은 원본 PDF 파일이 있는 폴더 내의 "jpg" 하위 폴더에 저장됩니다.

### 프로그래밍 방식으로 사용

PDF to JPG 변환 기능을 다른 Python 스크립트에서 직접 사용할 수 있습니다:

```python
from pdf_to_jpg import pdf_to_jpg

# 단일 PDF 파일 변환
pdf_to_jpg("경로/파일명.pdf")

# 폴더 내의 모든 PDF 파일 변환
pdf_to_jpg("폴더/경로")

# 상태 및 진행 상황 콜백 함수 사용
def status_update(message):
    print(f"상태: {message}")

def progress_update(current, total):
    print(f"진행률: {current}/{total}")

pdf_to_jpg("경로/파일명.pdf", status_update, progress_update)
```

## 출력 파일 구조

변환된 JPG 파일은 다음과 같은 구조로 저장됩니다:

```
원본_폴더/
├── 원본.pdf
└── jpg/
    └── 원본/
        ├── 원본_0001.jpg
        ├── 원본_0002.jpg
        └── ...
```

## 주의사항

1. 대용량 PDF 파일을 변환할 때는 충분한 메모리가 필요할 수 있습니다.
2. 변환 속도는 PDF 파일의 크기, 페이지 수, 그리고 컴퓨터 성능에 따라 달라집니다.
3. Poppler 경로가 올바르게 설정되어 있는지 확인하세요.

## 문제 해결

- **오류: "No module named 'pdf2image'"** - `pip install pdf2image` 명령으로 패키지를 설치하세요.
- **오류: "poppler_path is not defined"** - Poppler를 설치하고 코드에서 경로를 올바르게 설정하세요.
- **변환 실패** - PDF 파일이 손상되었거나 암호로 보호되어 있지 않은지 확인하세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여

버그 신고, 기능 요청 또는 코드 기여는 언제든지 환영합니다.