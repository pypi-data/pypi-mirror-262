# CrepeX django util

## 개발환경
- `poetry` 를 사용해서 개발
- 가상환경은 `poetry shell`
- 패키지 설치는 `poetry install`
- 최조 pre-commit 셋팅 `pre-commit install`

## 배포

### 테스트
- TestPypi 계정준비, API 토큰 준비

```shell
# test pypi repository 등록
poetry config repositories.testpypi https://test.pypi.org/legacy/
# poetry 에 토큰 등록
poetry config http-basic.testpypi __token__ pypi-your-api-token-here

# Build & Publish
poetry build
poetry publish -r testpypi

# Get package
pip install -i https://test.pypi.org/simple/ your-package-name
```

### Private 사용 (Now)

```shell
# Clone 후 설치
$ pip install git+https://[user-token]@github.com/[user-name]/[repo-name].git@[브랜치명|태그|해시]

# Clone 없이 설치된 버전 사용
$ pip install https://[user-token]@raw.githubusercontent.com/[user-name]/[repo-name]/[branch]/dist/[package_name]-[version].tar.gz

```
