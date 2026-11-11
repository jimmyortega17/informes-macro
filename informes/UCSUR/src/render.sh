set -e
D=/tmp/claude-0/-home-user-informes-macro/d71153c2-c436-5a73-abb0-cc6bc32355e9/scratchpad
cd $D/pdf2 && rm -f *.pdf && cp "$1" v.docx && zip -d v.docx '*/' >/dev/null 2>&1 || true
cd $D/pdf2 && timeout 200 soffice --headless --convert-to pdf v.docx >/dev/null 2>&1 && pdfinfo v.pdf | grep Pages
