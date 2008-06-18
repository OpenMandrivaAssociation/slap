Summary:	SLAP - SEIKO SmartLabel Printing Utility
Name:		slap
Version:	2r4p4
Release:	%mkrel 10
License:	GPL
Group:		Publishing
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

# SLAP
Source:		http://members.tripod.com/~uutil/slap/%{name}%{version}.tar.bz2
# Static library needed by SLAP
Source1:	http://members.tripod.com/~uutil/slap/mjsulib3r0p1.tar.bz2

Url:		http://members.tripod.com/~uutil/slap/

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
./Configure $RPM_BUILD_DIR/%name/mjsulibfiles
%make install
cd ..

# Compile SLAP
yes | ./Configure $RPM_BUILD_ROOT/usr
# Set library path
perl -p -i -e 's!/somewhere!/'$RPM_BUILD_DIR'/%name/mjsulibfiles!' makefile
# Correct path for man pages
perl -p -i -e 's!man/man1!share/man/man1!' makefile
%make

# Compile SLAP font converter
%make sdk

%install

# Clean up
rm -fr %buildroot

# Install SLAP
%makeinstall

# Install font converter
install -m 755 makefont %buildroot/%_bindir

# Correct file permissions
chmod -R u+w %buildroot/*


%clean
rm -fr %buildroot

%files
%defattr(-,root,root)
%doc *.txt 9devnotes COPYING FAQ.htm HOWTO
%_bindir/*
%_prefix/lib/slap*
%_mandir/man*/*

