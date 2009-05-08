Name:           nailer
Version:        0.4.3
Release:        5%{?dist}
Summary:        A thumbnail generator using mplayer

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://kdekorte.googlepages.com/nailer
Source0:        http://mplayer-video-thumbnailer.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:         nailer-0.4.3-gconf.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  GConf2
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
%patch0 -p0 -b .gconf


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

%clean
rm -rf $RPM_BUILD_ROOT


%pre
if [ "$1" -gt 1 ] ; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/nailer.schemas >/dev/null || :
fi


%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/nailer.schemas > /dev/null || :


%preun
if [ "$1" -eq 0 ] ; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/nailer.schemas > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog
%{_sysconfdir}/gconf/schemas/nailer.schemas
%{_bindir}/nailer


%changelog
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
