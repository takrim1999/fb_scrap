# fb_scrap
python3-m venv {name of venv}

#bash/zsh:
source {name of venv}/bin/activate
#windows:
C:\> {venv}\Scripts\activate.bat

git clone https://github.com/takrim1999/fb_scrap.git

pip install scrapy

cd fb_scrap/fb_scrap

#with log:
scrapy crawl login

#withoutlog:

scrapy crawl -nolog
 
