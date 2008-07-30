Name:		qmmp
Version:	0.2.0
Release:	1%{?dist}
Summary:	Qt-based multimedia player

Group:		Applications/Multimedia
License:	GPLv2+
URL:		http://qmmp.ylsoftware.com/index_en.html
Source:		http://qmmp.ylsoftware.com/files/%{name}-%{version}.tar.bz2
Source2:	qmmp-filter-provides.sh
%define		_use_internal_dependency_generator 0
%define		__find_provides %{SOURCE2}

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	cmake flac-devel >= 1.1.3
BuildRequires:	jack-audio-connection-kit-devel >= 0.102.5
BuildRequires:	libmpcdec-devel >= 1.2.2 libvorbis-devel libogg-devel
BuildRequires:	libsamplerate-devel alsa-lib-devel taglib-devel
BuildRequires:	qt4-devel >= 4.2 desktop-file-utils
BuildRequires:	libsndfile-devel wavpack-devel pulseaudio-libs-devel
BuildRequires:	libmodplug-devel curl-devel

Requires(post):	/sbin/ldconfig
Requires(pre):	/sbin/ldconfig

%package devel
Summary:	Header files for qmmp
Group:		Development/Libraries

%description
This program is an audio-player, written with help of Qt library.
The user interface is similar to winamp or xmms.
Main opportunities:

	* Winamp and xmms skins support
	* plugins support
	* Ogg Vorbis support
	* native FLAC support
	* Musepack support
	* WavePack support
	* ModPlug support
	* PCM WAVE support
	* AlSA sound output
	* JACK sound output
	* OSS sound output
	* PulseAudio output
	* Last.fm scrobbler
	* D-Bus support
	* Spectrum Analyzer
	* sample rate conversion 
	* streaming support

%description devel
QMMP is Qt-based audio player. This package contains its header files.

%prep
%setup -q

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
# Install desktop file
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
%{_libdir}/libqmmp*
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/icons/hicolor/

%files devel
%{_includedir}

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
* Tue Jul 29 2008 Karel Volny <kvolny@redhat.com> 0.2.0-1
- new version
- updated %%description to match upstream
- added BuildRequires: libsndfile-devel wavpack-devel pulseaudio-libs-devel
- added BuildRequires: libmodplug-devel curl-devel
- xpm icon is not used anymore (several pngs available)
- created devel subpackage

* Mon May 19 2008 Karel Volny <kvolny@redhat.com> 0.1.6-2
- fixed %%description not to include patent-encumbered formats (bug #447141)

* Tue May 13 2008 Karel Volny <kvolny@redhat.com> 0.1.6-1
- new version

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
