Name:		qmmp
Version:	0.1.5
Release:	1%{?dist}
Summary:	Qt-based multimedia player

Group:		Applications/Multimedia
License:	GPLv2+
URL:		http://qmmp.ylsoftware.com/index_en.html
Source:		http://qmmp.ylsoftware.com/files/%{name}-%{version}.tar.bz2
Source2:	qmmp-filter-provides.sh
#Patch:		qmmp-0.1.4-install-permissions.patch
%define		_use_internal_dependency_generator 0
%define		__find_provides %{SOURCE2}

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	cmake flac-devel >= 1.1.3
BuildRequires:	jack-audio-connection-kit-devel >= 0.102.5
BuildRequires:	libmpcdec-devel >= 1.2.2 libvorbis-devel libogg-devel
BuildRequires:	libsamplerate-devel alsa-lib-devel taglib-devel
BuildRequires:	qt4-devel >= 4.2 desktop-file-utils

Requires(post):	/sbin/ldconfig
Requires(pre):	/sbin/ldconfig

%description
This program is an audio-player, written with help of Qt library.
The user interface is similar to winamp or xmms.
Main opportunities:

	* unpacked winamp skins support;
	* plugins support;
	* Ogg Vorbis support;
	* Native FLAC support;
	* Musepack support;
	* WMA support;
	* AlSA sound output;
	* JACK sound output.

%prep
%setup -q
#%patch -p1

%build
%cmake \
	-D USE_FFMPEG:BOOL=FALSE \
	-D USE_MAD:BOOL=FALSE \
	-D CMAKE_INSTALL_PREFIX=%{_prefix} \
	-D LIB_DIR=%{_lib} \
	./
make VERBOSE=1

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
# Install icon and desktop file
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
mv  %{buildroot}%{_datadir}/pixmaps/qmmp.xpm %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
desktop-file-install --delete-original --vendor fedora --dir \
	%{buildroot}%{_datadir}/applications \
	%{buildroot}/%{_datadir}/applications/qmmp.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog ChangeLog.rus COPYING README README.RUS
%{_bindir}/qmmp
%{_libdir}/qmmp
%{_libdir}/libqmmp.so
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/

%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi
 
%postun
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%changelog
* Mon Dec 10 2007 Karel Volny <kvolny@redhat.com> 0.1.5-1
- new version
- simplified setting of library destination
- removed install-permissions patch, fixed upstream

* Wed Nov 21 2007 Karel Volny <kvolny@redhat.com> 0.1.4-5
- included Hans de Goede's patch for file permissions

* Mon Nov 19 2007 Karel Volny <kvolny@redhat.com> 0.1.4-4
- additional spec improvements as suggested in comment #10 to bug #280751

* Wed Sep 12 2007 Karel Volny <kvolny@redhat.com> 0.1.4-3
- additional spec improvements as suggested in comment #4 to bug #280751

* Tue Sep 11 2007 Karel Volny <kvolny@redhat.com> 0.1.4-2
- spec cleanup as suggested in comment #2 to bug #280751

* Mon Sep 10 2007 Karel Volny <kvolny@redhat.com> 0.1.4-1
- version bump
- install vendor-supplied .desktop file

* Thu Sep 6 2007 Karel Volny <kvolny@redhat.com> 0.1.3.1-2
- patched for multilib Fedora setup
- added .desktop entry and icon
- fixed spec to meet Fedora policies and rpm requirements
- removed ffmpeg and mad plugins to meet Fedora no-mp3 policy

* Wed Aug 1 2007 Eugene Pivnev <ti DOT eugene AT gmail DOT com> 1.1.9-1
- Initial release for Fedora 7