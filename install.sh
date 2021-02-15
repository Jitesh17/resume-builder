cd /src/
wget http://www.freedesktop.org/software/fontconfig/release/fontconfig-2.10.91.tar.gz
cd fontconfig-2.10.91
tar -xzf fontconfig-2.10.91.tar.gz
./configure
make

cd /src/
wget http://poppler.freedesktop.org/poppler-0.22.1.tar.gz
tar -xzf poppler-0.22.1.tar.gz
cd poppler-0.22.1
FONTCONFIG_LIBS="-L/src/fontconfig-2.10.91/src/.libs/ -lfontconfig" FONTCONFIG_CFLAGS="-I/src/fontconfig-2.10.91/" ./configure
make