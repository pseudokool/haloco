# HALOCO
Just a basic helper utility, to speed up web lookups of quiz games. Capture of the device screen is required. ADB can run over USB or WiFi.
* Runs on Python 2.7.*
* pytesseract (latest)
* requests
* BeautifulSoup 4

### NOTES
Use pipenv for dependency management.

Quick fix on macos, add to ~/.bash_profile
```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

### TODO
* Speed up parsing of search results
* Sharpen 'question' string capture and OCR
* 
### CHANGELOG
* 0.1 - Switched parser from html to lxml (~2s improvement)
