# TODO:
# - try to use system ffmpeg (some ancient 0.5 snap here)
#
# Conditional build:
%bcond_without	xvid			# without xvid support
%bcond_with	gdkpixbuf		# use GdkPixbuf thumbnail rendering (default=no)
%bcond_with	system_ffmpeg		# use system ffmpeg (ancient only)
%bcond_without	system_libmpeg3		# use system libmpeg3

%define		pkgname	gimp-gap
%define		pkgver	2.6

Summary:	The GIMP Animation Package
Summary(pl.UTF-8):	Pakiet animacyjny dla GIMP-a
Name:		gimp-plugin-gap
Version:	%{pkgver}.0
Release:	1
License:	GPL v2+
Group:		X11/Applications/Graphics
Source0:	http://download.gimp.org/pub/gimp/plug-ins/v2.6/gap/%{pkgname}-%{version}.tar.bz2
# Source0-md5:	249ed829de8b78675c0fe4ef4212089f
Patch0:		%{name}-ffmpeg-texi2html.patch
Patch1:		%{name}-format.patch
URL:		http://www.gimp.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
%{!?with_system_ffmpeg:BuildRequires:	bzip2-devel}
%{!?with_system_ffmpeg:BuildRequires:	faac-devel}
%{!?with_system_ffmpeg:BuildRequires:	faad2-devel}
BuildRequires:	gettext-devel
BuildRequires:	gimp-devel >= 2.6.0
BuildRequires:	glib2-devel >= 1:2.8.0
BuildRequires:	intltool >= 0.35.0
%{!?with_system_ffmpeg:BuildRequires:	lame-libs-devel}
BuildRequires:	libjpeg-devel
%{?with_system_libmpeg3:BuildRequires:	libmpeg3-devel >= 1.8}
# ABI 0.65
%{!?with_system_ffmpeg:BuildRequires:	libx264-devel}
BuildRequires:	nasm
BuildRequires:	pkgconfig
BuildRequires:	xvid-devel >= 1:1.0.0
Obsoletes:	gimp-mpeg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		gimpplugindir	%(gimptool --gimpplugindir)/plug-ins
%define		gimpscriptdir	%(gimptool --gimpdatadir)/scripts

%description
The GIMP-GAP (GIMP Animation Package) is a collection of Plug-Ins to
extend GIMP %{pkgver} with capabilities to edit and create animations as
sequences of single frames.

%description -l pl.UTF-8
GIMP-GAP (GIMP Animation Package) jest kolekcją wtyczek
rozszerzających GIMP-a o możliwość edycji i tworzenia animacji i
sekwencji pojedynczych ramek.

%prep
%setup -q -n %{pkgname}-%{version}
%patch1 -p1

%build
%{__glib_gettextize}
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_xvid:--disable-libxvidcore --disable-ff-libxvid} \
	%{?with_gdkpixbuf:--enable-gdkpixbuf-pview} \
	%{?with_system_libmpeg3:--with-preinstalled-libmpeg3incdir=%{_includedir}/libmpeg3} \
	%{?with_system_libmpeg3:--with-preinstalled-libmpeg3=%{_libdir}/libmpeg3.so}

cd extern_libs/ffmpeg
%patch0 -p1
cd ../..

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{pkgname}-%{pkgver}/*.a

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sr@Latn,sr@latin}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%dir %{_libdir}/%{pkgname}-%{pkgver}
%attr(755,root,root) %{_libdir}/%{pkgname}-%{pkgver}/audioconvert_to_wav.sh
%attr(755,root,root) %{gimpplugindir}/gap_*
%{gimpscriptdir}/gap-dup-continue.scm
%{gimpscriptdir}/sel-to-anim-img.scm
