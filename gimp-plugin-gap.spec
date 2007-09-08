# TODO:
# - try to use update to current libmpeg3 API
# - try to use system ffmpeg (some old snap here)
#
# Conditional build:
%bcond_without	xvid		# without xvid support
%bcond_with	gdkpixbuf	# use GdkPixbuf thumbnail rendering (default=no)
%bcond_with	libmpeg3	# use system libmpeg3 (1.5.x only)
#
Summary:	The GIMP Animation Package
Summary(pl.UTF-8):	Pakiet animacyjny dla GIMP-a
Name:		gimp-plugin-gap
Version:	2.2.2
Release:	1
License:	GPL v2+
Group:		X11/Applications/Graphics
Source0:	ftp://ftp.gimp.org/pub/gimp/plug-ins/v2.2/gap/gimp-gap-%{version}.tar.bz2
# Source0-md5:	2c7ea1cf560a2693310781265d8f3c05
URL:		http://www.gimp.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gimp-devel >= 2.2.0
BuildRequires:	intltool
BuildRequires:	libjpeg-devel
%{?with_libmpeg3:BuildRequires:	libmpeg3-devel >= 1.5}
%{?with_libmpeg3:BuildRequires:	libmpeg3-devel < 1.6}
BuildRequires:	nasm
BuildRequires:	pkgconfig
BuildRequires:	xvid-devel >= 1:1.0.0
Obsoletes:	gimp-mpeg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		gimpplugindir	%(gimptool --gimpplugindir)/plug-ins
%define		gimpscriptdir	%(gimptool --gimpdatadir)/scripts

%description
The GIMP-GAP (GIMP Animation Package) is a collection of Plug-Ins to
extend GIMP 2.2 with capabilities to edit and create animations as
sequences of single frames.

%description -l pl.UTF-8
GIMP-GAP (GIMP Animation Package) jest kolekcją wtyczek
rozszerzających GIMP-a o możliwość edycji i tworzenia animacji i
sekwencji pojedynczych ramek.

%prep
%setup -q -n gimp-gap-%{version}

%build
%{__glib_gettextize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	%{!?with_xvid:--disable-libxvidcore} \
	%{?with_gdkpixbuf:--enable-gdkpixbuf-pview} \
	%{?with_libmpeg3:--with-preinstalled-libmpeg3incdir=%{_includedir}/libmpeg3} \
	%{?with_libmpeg3:--with-preinstalled-libmpeg3=%{_libdir}/libmpeg3.so}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gimp-gap-2.2/*.a

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%dir %{_libdir}/gimp-gap-2.2
%attr(755,root,root) %{_libdir}/gimp-gap-2.2/audioconvert_to_wav.sh
%attr(755,root,root) %{gimpplugindir}/gap_*
%{gimpscriptdir}/*.scm
