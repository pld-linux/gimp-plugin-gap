######		/root/rpm/SOURCES/rpm.groups: no such file

%bcond_with	maintainer-mode        # enable make rules and dependencies not useful (and sometimes confusing) to the casual installer
%bcond_without dependency-tracking # speeds up one-time build
%bcond_without unix-frontends      # don't build with UNIX specific frontends for mplayer, xanim and mpeg encoders
%bcond_without videoapi-support    # don't build with videoapi support
%bcond_without libavformat         # don't build with libavformat/libavcodec  
%bcond_without libmpeg3            # don't build with libmpeg3
%bcond_without libxvidcore         # don't build with libxvidcore
%bcond_without audio-support       # don't build with audio support
%bcond_with gdkpixbuf-pview        # use GdkPixbuf thumbnail rendering (default=no)

%bcond_without preinstalled-libmpeg3incdir # force link with an already installed libmpeg3 library and specify where to find libmpeg3 headerfiles
%bcond_without preinstalled-libmpeg3 # full pathname of the preinstalled libmpeg3.a libraryfile

Summary:	The GIMP Animation Package
Summary(pl):	Pakiet animacyjny dla GIMP'a
Name:		gimp-plugin-gap
Version:	2.2.1
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	ftp://ftp.gimp.org/pub/gimp/plug-ins/v2.2/gap/gimp-gap-%{version}.tar.bz2
# Source0-md5:	c2aa33b5240c57aa6bf9ffc686f3e3ac
URL:		http://www.gimp.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gimp-devel >= 2.2.0
BuildRequires:	intltool
BuildRequires:	libjpeg-devel
BuildRequires:	nasm
BuildRequires:	pkgconfig
BuildRequires:	xvid-devel >= 1:1.0.0.
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define gapplugindir %(gimptool --gimpplugindir)/plug-ins
%define _scriptdir %(gimptool --gimpdatadir)/scripts

%description
The GIMP-GAP (GIMP Animation Package) is a collection of Plug-Ins to
extend GIMP 2.2 with capabilities to edit and create animations as
sequences of single frames.

%description -l pl
GIMP-GAP (GIMP Animation Package) jest kolekcj± wtyczek
rozszerzaj±cych GIMPa o mo¿liwo¶æ edycji i tworzenia animacji i
sekwencji pojedynczych ramek.

%prep
%setup -q -n gimp-gap-%{version}

%build
%{__glib_gettextize}
%__aclocal
%__automake
%__autoconf
%configure \
  %{?with_maintainer-mode --enable-maintainer-mode} \
  %{?without_dependency-tracking --disable-dependency-tracking} \
  %{?without_unix-frontends --disable-unix-frontends} \
  %{?without_videoapi-support --disable-videoapi-support} \
  %{?without_libavformat --disable-libavformat} \
  %{?without_libmpeg3 --disable-libmpeg3} \
  %{?without_libxvidcore --disable-libxvidcore} \
  %{?without_audio-support --disable-audio-support} \
  %{?with_gdkpixbuf-pview --enable-gdkpixbuf-pview} \
  %{!?without_preinstalled-libmpeg3incdir --with-preinstalled-libmpeg3incdir=%{_libdir}} \
  %{!?without_preinstalled-libmpeg3incdir --with-preinstalled-libmpeg3incdir=%{_libdir}/libmpeg3.a}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{_libdir}/gimp-gap-2.2
%attr(755,root,root) %{gapplugindir}/*
%attr(755,root,root) %{_libdir}/gimp-gap-2.2/*
%{__scriptdir}/*
%doc AUTHORS ChangeLog NEWS README
