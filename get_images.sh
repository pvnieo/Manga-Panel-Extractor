#!/bin/sh
# get all pages
curl 'https://onepiecechapters.com/chapters/5613/one-piece-chapter-1073?&date=7-2-2023-13' -o '#1.html'

# get all images
grep -oh 'https://cdn.onepiecechapters.com/file/CDN-M-A-N/.*png' *.html >urls.txt

# download all images
sort -u urls.txt | wget -i- -P images/