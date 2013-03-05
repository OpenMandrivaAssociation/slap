Summary:	SLAP - SEIKO SmartLabel Printing Utility
Name:		slap
Version:	2r4p4
Release:	16
License:	GPL
Group:		Publishing
Url:		http://www.shelldozer.im/slap/
# SLAP
Source0:	http://members.tripod.com/~uutil/slap/%{name}%{version}.tar.bz2
# Static library needed by SLAP
Source1:	http://members.tripod.com/~uutil/slap/mjsulib3r0p1.tar.bz2

%description
SLAP is a UNIX command line program that prints labels on many SEIKO Smart
Label Printers. It prints only text, no graphics, PostScript, and so on.
The text can be printed in 16 different fonts and in 6 font sizes. Enter
"man slap" at the command prompt for more info.

%prep
# Load source code
%setup -q -n slap
%setup -q -T -D -a 1 -n slap

# Correct file permissions
chmod -R u+w *

%build
# Compile static library
mkdir mjsulibfiles
cd mjsulib/
./Configure $RPM_BUILD_DIR/%{name}/mjsulibfiles
%make install
cd ..

# Compile SLAP
yes | ./Configure %{buildroot}/usr
# Set library path
perl -p -i -e 's!/somewhere!/'$RPM_BUILD_DIR'/%{name}/mjsulibfiles!' makefile
# Correct path for man pages
perl -p -i -e 's!man/man1!share/man/man1!' makefile
%make

# Compile SLAP font converter
%make sdk

%install
%makeinstall

# Install font converter
install -m 755 makefont %{buildroot}/%{_bindir}

# Correct file permissions
chmod -R u+w %{buildroot}/*

%files
%doc *.txt 9devnotes COPYING FAQ.htm HOWTO
%{_bindir}/*
%{_prefix}/lib/slap*
%{_mandir}/man*/*

