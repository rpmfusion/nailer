Name:           nailer
Version:        0.4.6
Release:        1%{?dist}
Summary:        A thumbnail generator using mplayer

License:        GPLv2+
URL:            http://kdekorte.googlepages.com/nailer
Source0:        http://mplayer-video-thumbnailer.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:  GConf2-devel
BuildRequires:  gtk2-devel
Requires:       GConf2
Requires:       mplayer
#We need to conflict with totem until http://bugzilla.gnome.org/show_bug.cgi?id=497264 gets fixed
Conflicts:      totem

Requires(pre):  GConf2
Requires(post): GConf2
Requires(preun): GConf2

%description
MPlayer-Video-Thumbnailer aka Nailer is a Glib application that uses MPlayer to
generate thumbnails of video media files.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT

#remove intrusive docs
rm -rf $RPM_BUILD_ROOT%{_docdir}

#remove the desktop file
rm -rf $RPM_BUILD_ROOT%{_datadir}/thumbnailers


%pre
%gconf_schema_prepare


%post
%gconf_schema_upgrade


%preun
%gconf_schema_remove


%files
%doc COPYING ChangeLog
%{_sysconfdir}/gconf/schemas/nailer.schemas
%{_bindir}/nailer


%changelog
* Thu Oct 11 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.4.6-1
- Updated to 0.4.6
- Dropped included patches
- Added GConf2-devel to BuildRequires

* Mon Feb 20 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.3-8
- Rebuilt for devel/F-17 inter-branch

* Sat Feb 11 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.4.3-7
- Fixed build failures
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Updated scriptlets to the latest spec

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 08 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.4.3-5
- Added Conflicts: totem for the time being

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.4.3-4
- rebuild for new F11 features

* Sat Feb 28 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.4.3-3
- Dropped the .desktop file entirely
- Patched the gconf schema

* Sat Feb 28 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.4.3-2
- Added desktop-file-utils to BuildRequires, validate the .desktop file
- Own the %%{_datadir}/thumbnailers
- Added GConf2 to Requires for the purpose of directory ownership

* Fri Jan 16 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.4.3-1
- Cleaned up upstream spec for RPM Fusion
