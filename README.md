# Mac M2 Pro - AUTOMATIC1111 NSFW Setup

Mac M2 Pro 16GB에서 AUTOMATIC1111을 사용한 NSFW 이미지 생성 도구입니다.

## 🍎 Mac M2 Pro 16GB - 완벽 지원!

- **16GB 통합 메모리** = 일반 16GB RAM보다 효율적
- **M2 Pro GPU** = Metal 가속으로 빠른 성능
- **768x768 이미지**: 45-60초 생성
- **1024x1024 이미지**: 90초 생성

## 🚀 빠른 설치

```bash
# 1. 의존성 설치
pip install -r requirements_auto1111.txt

# 2. 자동 설정 (추천)
python quick_start_mac_m2.py

# 3. 수동 설정
brew install python@3.10 git wget
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui
# launch_mac_m2.sh 스크립트 생성 후 실행
```

## 📱 사용법

### Web UI 사용
```bash
cd stable-diffusion-webui
./launch_mac_m2.sh
```
- 웹 UI: http://localhost:7860
- API 문서: http://localhost:7860/docs

### Python API 사용
```python
from auto1111_client import Auto1111Client

client = Auto1111Client("http://localhost:7860")

result = client.generate_nsfw_image(
    prompt="beautiful portrait, professional photography",
    width=768, height=768, steps=25
)

if result:
    client.save_image(result['images'][0], "output.png")
```

### Mac M2 최적화 예제
```bash
python mac_m2_example.py
```

## 📁 주요 파일

- **`auto1111_client.py`** - AUTOMATIC1111 API 클라이언트
- **`quick_start_mac_m2.py`** - Mac M2 자동 설치 스크립트
- **`mac_m2_example.py`** - Mac M2 최적화 사용 예제
- **`requirements_auto1111.txt`** - 필요한 패키지 목록

## 🎯 NSFW 모델 사용

### 모델 다운로드
```bash
cd stable-diffusion-webui/models/Stable-diffusion
wget -O deliberate_v2.safetensors "https://huggingface.co/XpucT/Deliberate/resolve/main/deliberate_v2.safetensors"
```

### 추천 모델
- **Deliberate v2** - 고품질 NSFW 생성
- **Realistic Vision** - 빠른 실사풍 생성
- **DreamShaper** - 다양한 스타일 지원

## 💡 Mac M2 Pro 최적화 팁

- **768x768** 해상도 사용 (품질/속도 균형)
- **20-30 스텝** 설정
- **Euler a** 샘플러 사용 (가장 빠름)
- 생성 중 다른 앱 종료
- Activity Monitor로 메모리 사용량 모니터링

## ⚠️ 중요 사항

- 로컬 법률 및 규정 준수
- 개인적 사용 목적으로만 사용
- 생성된 콘텐츠의 윤리적 사용
- 플랫폼 이용약관 준수

---

**Mac M2 Pro 16GB = AUTOMATIC1111에 최적화된 환경입니다!** 