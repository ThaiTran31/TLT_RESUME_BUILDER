gunicorn --bind=0.0.0.0 --timeout 600 core.wsgi --access-logfile '-' --error-logfile '-'
sudo python -m spacy download en
git clone -b 4.1 https://github.com/tesseract-ocr/tesseract.git
cd tesseract
sudo ./autogen.sh
sudo ./configure
sudo make
sudo make install
sudo ldconfig
cd ..