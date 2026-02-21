# Git 작업 가이드

## 최초 1회 — 저장소 초기화 및 원격 연결

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/본인아이디/저장소이름.git
git push -u origin main
```

## 이후 작업 — 변경사항 올리기

```bash
git add .
git commit -m "커밋 메시지"
git push
```

## 원격 저장소에서 가져오기

```bash
git pull
```

## .gitignore

프로젝트 루트에 `.gitignore` 파일을 만들고 아래 내용 입력:

```
__pycache__/
```
