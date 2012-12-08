Summary:	SLAP - SEIKO SmartLabel Printing Utility
Name:		slap
Version:	2r4p4
Release:	%mkrel 15
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



%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 2r4p4-14mdv2011.0
+ Revision: 669986
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2r4p4-13mdv2011.0
+ Revision: 607542
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 2r4p4-12mdv2010.1
+ Revision: 524115
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 2r4p4-11mdv2010.0
+ Revision: 427170
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 2r4p4-10mdv2009.0
+ Revision: 225443
- rebuild

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2r4p4-9mdv2008.1
+ Revision: 179507
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - kill re-definition of %%buildroot on Pixel's request


* Wed May 24 2006 Pascal Terjan <pterjan@mandriva.org> 2r4p4-8mdk
- fix build
- mkrel

* Fri Sep 02 2005 Till Kamppeter <till@mandriva.com> 2r4p4-7mdk
- Removed the dust of 1 year not rebuilding.

* Fri Aug 13 2004 Till Kamppeter <till@mandrakesoft.com> 2r4p4-6mdk
- Rebuilt.

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2r4p4-5mdk
- rebuild
- don't rm -rf $RPM_BUILD_ROOT in %%prep

