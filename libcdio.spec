#
# Conditional build:
%bcond_without	cddb		# build cd-info without CDDB lookups (for bootstrap)
%bcond_without	static_libs	# don't build static library
%bcond_without	vcd		# build cd-info without VCD support (for bootstrap)
#				  (affects only -utils, not libraries)
#
Summary:	GNU Compact Disc Input, Output and Control Library
Summary(pl.UTF-8):	Biblioteka GNU do obsługi wejścia, wyjścia i sterowania czytnikiem CD
Name:		libcdio
Version:	0.93
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	http://ftp.gnu.org/gnu/libcdio/%{name}-%{version}.tar.bz2
# Source0-md5:	8be842d903f086941c45ad0360420314
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/libcdio/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.8.3
# for AM_ICONV and config.rpath
BuildRequires:	gettext-tools >= 0.14
BuildRequires:	help2man
%{?with_cddb:BuildRequires:	libcddb-devel >= 1.0.1}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	texinfo
%{?with_vcd:BuildRequires:	vcdimager-devel >= 0.7.21}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library is to encapsulate CD-ROM reading and control.
Applications wishing to be oblivious of the OS- and device-dependent
properties of a CD-ROM can use this library.

Some support for disk image types like BIN/CUE and NRG is available,
so applications that use this library also have the ability to read
disc images as though they were CD's.

Immediate uses are VCDImager, a navigation-capable Video CD plugin
and CD-DA plugin for the media player xine.

A sample utility, cd-info which displayings CD info is included in
utils subpackage.

%description -l pl.UTF-8
Ta biblioteka obudowuje czynności odczytu i sterowania czytnikami
CD-ROM. Aplikacje chcące zapomnieć o zależnych od systemu lub
urządzenia własnościach CD-ROM-u mogą używać tej biblioteki.

Dostępna jest pewna obsługa obrazów dysków typu BIN/CUE czy NRG, więc
aplikacje używające tej biblioteki mogą czytać także takie obrazy
dysków tak jakby były płytami.

Biblioteka jest używana bezpośrednio w VCDImagerze, wtyczce z
nawigacją do Video CD oraz wtyczce CD-DA dla odtwarzacza multimediów
xine.

W podpakiecie utils załączone jest przykładowe narzędzie cd-info
służące do wyświetlania informacji o płytach kompaktowych.

%package devel
Summary:	Header files for libcdio libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek libcdio
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libcdio libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek libcdio.

%package static
Summary:	Static libcdio libraries
Summary(pl.UTF-8):	Statyczne biblioteki libcdio
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libcdio libraries.

%description static -l pl.UTF-8
Statyczne biblioteki libcdio.

%package c++
Summary:	C++ libcdio libraries
Summary(pl.UTF-8):	Biblioteki C++ libcdio
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
C++ libcdio libraries.

%description c++ -l pl.UTF-8
Biblioteki C++ libcdio.

%package c++-devel
Summary:	Header files for C++ libcdio libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek C++ libcdio
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libstdc++-devel

%description c++-devel
Header files for C++ libcdio libraries.

%description c++-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek C++ libcdio.

%package c++-static
Summary:	Static C++ libcdio libraries
Summary(pl.UTF-8):	Statyczne biblioteki C++ libcdio
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
Static C++ libcdio libraries.

%description c++-static -l pl.UTF-8
Statyczne biblioteki C++ libcdio.

%package utils
Summary:	libcdio utilities: cd-info, cd-read
Summary(pl.UTF-8):	Narzędzia używające libcdio: cd-info, cd-read
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description utils
libcdio utilities: cd-info, cd-read.

%description utils -l pl.UTF-8
Narzędzia używające libcdio: cd-info, cd-read.

%prep
%setup -q
%patch0 -p1

%{__sed} -i 's, example$,,' Makefile.am

# bug: *.pc for C++ bindings, not programs
%{__sed} -i 's,ENABLE_CPP,ENABLE_CXX_BINDINGS,' Makefile.am

cp -f /usr/share/gettext/config.rpath .

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CPPFLAGS="-I/usr/include/ncurses"
%configure \
	--disable-silent-rules \
	--enable-cd-info-linux \
	--enable-maintainer-mode \
	--enable-rock \
	%{!?with_cddb:--disable-cddb} \
	%{!?with_vcd:--disable-vcd-info} \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	c++ -p /sbin/ldconfig
%postun	c++ -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_libdir}/libcdio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcdio.so.16
%attr(755,root,root) %{_libdir}/libiso9660.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libiso9660.so.10
%attr(755,root,root) %{_libdir}/libudf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libudf.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcdio.so
%attr(755,root,root) %{_libdir}/libiso9660.so
%attr(755,root,root) %{_libdir}/libudf.so
%{_includedir}/cdio
%{_pkgconfigdir}/libcdio.pc
%{_pkgconfigdir}/libiso9660.pc
%{_pkgconfigdir}/libudf.pc
%{_infodir}/libcdio.info*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcdio.a
%{_libdir}/libiso9660.a
%{_libdir}/libudf.a
%endif

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcdio++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcdio++.so.0
%attr(755,root,root) %{_libdir}/libiso9660++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libiso9660++.so.0

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcdio++.so
%attr(755,root,root) %{_libdir}/libiso9660++.so
%{_includedir}/cdio++
%{_pkgconfigdir}/libcdio++.pc
%{_pkgconfigdir}/libiso9660++.pc

%if %{with static_libs}
%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libcdio++.a
%{_libdir}/libiso9660++.a
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cd-drive
%attr(755,root,root) %{_bindir}/cd-info
%attr(755,root,root) %{_bindir}/cd-read
%attr(755,root,root) %{_bindir}/cdda-player
%attr(755,root,root) %{_bindir}/cdinfo-linux
%attr(755,root,root) %{_bindir}/iso-info
%attr(755,root,root) %{_bindir}/iso-read
%attr(755,root,root) %{_bindir}/mmc-tool
%{_mandir}/man1/cd-drive.1*
%{_mandir}/man1/cd-info.1*
%{_mandir}/man1/cd-read.1*
%{_mandir}/man1/iso-info.1*
%{_mandir}/man1/iso-read.1*
