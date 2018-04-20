#! /bin/sh

# Spit out flag as hex
xxd -p key.bin | fold -w 20 > tmp/key.hex
qrencode -o tmp/qr.png < tmp/key.hex

# Encode flag as PNG
cat secdsm_flag.txt | base64 | xxd -p | tr -d '\n' | python hex2pool.py tmp/secdsm_secret_image.png

# Run accessibility
cat secdsm_flag.txt | base64 | xxd -p | tr -d '\n' | tr "0123456789abcdef" "WYURPOGNByurpogn" > tmp/poolballs.txt
python3 insert_accessibility.py

# Angecrypt
python3 angecrypt.py

# Encode the IV
base32 < tmp/iv.bin > tmp/iv

# Clean up zips
rm -rf *.zip

# Create hints zip
echo -n "Enter the password: "
cat password.txt
zip -e hints.zip hints/*

mv hints.zip "`base32 password.txt | base64 | base32 | base64 -d | base32 -w 0`.zip"

# Load up secrets.zip
rm -rf secrets
mkdir secrets
cp tmp/f1.png secrets/secrets.png
#cp pocorgtfo03.pdf secrets
sha256sum pocorgtfo03.pdf key.bin > secrets/sha256sums.txt

pushd tmp
sha256sum iv.bin >> ../secrets/sha256sums.txt
popd

mv *.zip secrets/

# Add as metadata
cp dangerous.png secrets/dangerous.png
exiftool -"UserComment"=`cat tmp/iv` secrets/dangerous.png
rm secrets/dangerous.png_original

pushd secrets
cat ../key.bin | xxd -p | tr -d '\n' >> sha256sums.txt
cat ../tmp/iv.bin | xxd -p | tr -d '\n' >> sha256sums.txt
echo '  secrets.png' >> sha256sums.txt
sha256sum *.zip dangerous.png >> sha256sums.txt
popd

zip useful_stuff.zip secrets/*
rm -f ctf.pdf
cat Optiv*.pdf useful_stuff.zip > ctf.pdf
