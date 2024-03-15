# b3o_fedlearn
AWS를 활용한 연합학습을 진행하기 위한 패키지 입니다.

---
## Installation

패키지를 설치하기 위해서는 다음과 같은 pip 명령어를 사용합니다:
```python
pip install b3o-fedlearn
```

---
## Getting Started

패키지를 사용하는 방법에 대한 간단한 예제입니다:

```python
from b3o_fedlearn import data_processing, fedlearner

# 연합학습을 위한 데이터 셋 준비
data_processing.input_fn()

# 연합학습 진행
fedlearner.FL_start()
```
---

## Contributing
여러분의 기여를 환영합니다. 이슈를 등록하거나 풀 리퀘스트를 보내주세요.

---
## License
MIT License 라이센스 하에 제공됩니다. 자세한 내용은 LICENSE 파일을 참조해주세요.