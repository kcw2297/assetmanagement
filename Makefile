.PHONY: bump-patch bump-minor bump-major build publish clean

# 버전 업데이트
bump-patch:
	@python version.py patch

bump-minor:
	@python version.py minor

bump-major:
	@python version.py major

# 빌드 & 배포
build:
	@echo "빌드 시작..."
	@rm -rf dist/
	@python -m build
	@echo "빌드 완료: dist/"

publish: build
	@echo "PyPI 배포 시작..."
	@twine upload dist/*
	@echo "배포 완료!"

# 정리
clean:
	@rm -rf dist/ build/ *.egg-info/
	@echo "정리 완료"

# 릴리스 (버전업 + 빌드 + 배포)
release-patch: bump-patch build publish
release-minor: bump-minor build publish
release-major: bump-major build publish
