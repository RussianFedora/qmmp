Name:		qmmp
Version:	0.3.1
Release:	2%{?dist}
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
BuildRequires:	libbs2b-devel
BuildRequires:	libcdio-devel
BuildRequires:	libmpcdec-devel >= 1.2.2 libvorbis-devel libogg-devel
BuildRequires:	libprojectM-devel
BuildRequires:	libsamplerate-devel alsa-lib-devel taglib-devel
BuildRequires:	qt-devel >= 4.2 desktop-file-utils
BuildRequires:	libsndfile-devel wavpack-devel pulseaudio-libs-devel
BuildRequires:	libmodplug-devel libcurl-devel openssl-devel

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
	* CD Audio support
	* CUE sheet support
	* ALSA sound output
	* JACK sound output
	* OSS sound output
	* PulseAudio output
	* Last.fm/Libre.fm scrobbler
	* D-Bus support
	* Spectrum Analyzer
	* projectM visualization
	* sample rate conversion
	* bs2b dsp effect
	* streaming support
	* removable device detection
	* MPRIS support
	* global hotkey support
	* lyrics support

%description devel
QMMP is Qt-based audio player. This package contains its header files.

%prep
%setup -q

%build
%cmake \
	-D USE_AAC:BOOL=FALSE \
	-D USE_FFMPEG:BOOL=FALSE \
	-D USE_MAD:BOOL=FALSE \
	-D USE_MPLAYER:BOOL=FALSE \
	-D CMAKE_INSTALL_PREFIX=%{_prefix} \
	-D LIB_DIR=%{_lib} \
	./
make %{?_smp_mflags} VERBOSE=1

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
# Install desktop file
desktop-file-install --delete-original --vendor fedora --dir \
	%{buildroot}%{_datadir}/applications \
	%{buildroot}/%{_datadir}/applications/qmmp.desktop
# new files since 0.3.0, using Vendor is deprecated, so just validate
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}_cue.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}_enqueue.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog ChangeLog.rus COPYING README README.RUS
%{_bindir}/qmmp
%{_libdir}/qmmp
%{_libdir}/libqmmp*
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/applications/%{name}_cue.desktop
%{_datadir}/applications/%{name}_enqueue.desktop
%{_datadir}/icons/hicolor/

%files devel
%{_includedir}/*

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
* Wed Nov 25 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.3.1-2
- rebuild for Qt 4.6.0 RC1 in F13 (was built against Beta 1 with unstable ABI)

* Wed Nov 04 2009 Karel Volný <kvolny@redhat.com> 0.3.1-1
- new version

* Wed Sep 02 2009 Karel Volný <kvolny@redhat.com> 0.3.0-3
- add libbs2b support, as it got added to Fedora (see bug #519138)

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 0.3.0-2
- rebuilt with new openssl

* Tue Aug 25 2009 Karel Volný <kvolny@redhat.com> - 0.3.0-1
- new version
- updated %%description to match upstream
- new plugins = new BuildRequires, new .desktop files
- AAC support disabled due to patent restrictions
- mplayer plugin disabled due to mplayer missing from Fedora

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 05 2009 Karel Volny <kvolny@redhat.com> 0.2.3-3
- do not own /usr/include in -devel subpackage (fixes bug #484098)

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 0.2.3-2
- rebuild with new openssl

* Fri Dec 05 2008 Karel Volny <kvolny@redhat.com> 0.2.3-1
- new version
- added %%{?_smp_mflags} to make, as parallel build was fixed

* Tue Sep 02 2008 Karel Volny <kvolny@redhat.com> 0.2.2-1
- new version

* Wed Jul 30 2008 Karel Volny <kvolny@redhat.com> 0.2.0-1
- new version
- updated %%description to match upstream
- added BuildRequires: libsndfile-devel wavpack-devel pulseaudio-libs-devel
- added BuildRequires: libmodplug-devel libcurl-devel openssl-devel
- xpm icon is not used anymore (several pngs available)
- created devel subpackage

* Mon May 19 2008 Karel Volny <kvolny@redhat.com> 0.1.6-2
- fixed %%description not to include patent-encumbered formats (bug #447141)

* Tue May 13 2008 Karel Volny <kvolny@redhat.com> 0.1.6-1
- new version

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.5-2
- Autorebuild for GCC 4.3

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
