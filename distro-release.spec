# Please update release notes:
# make -C SOURCES release-notes.{html,txt}
#
%bcond_with bootstrap

%define new_distribution OpenMandriva Lx
%define new_vendor OpenMandriva
%define new_product OpenMandriva Lx
# (tpg) use codename from here https://wiki.openmandriva.org/en/policies/codename
%define new_codename ROME
%define vendor_tag %(echo %{new_vendor} |tr A-Z a-z)
%define distribution_tag %(echo %{new_distribution} |tr A-Z a-z |sed -e 's,[ /!?],_,g')
%define product_tag %(echo %{new_product} |tr A-Z a-z |sed -e 's,[ /!?],_,g')
%define shorttag omv
%define new_disturl http://openmandriva.org/
%define new_bugurl https://github.com/OpenMandrivaAssociation/distribution/issues

%define am_i_cooker 0
%define am_i_rolling 1
%if %am_i_cooker
%define distrib Cooker
%else
%if %am_i_rolling
%define distrib Rolling
%else
%define distrib Official
%endif
%endif
%define _distribution %(echo %{new_distribution} | tr A-Z a-z |sed -e 's#[ /()!?]#_#g')
%define product_type Basic
%if %am_i_cooker
%define product_branch Devel
%else
%define product_branch Official
%endif
%define product_release 1
%define product_arch %{_target_cpu}

# The Distribution release, what is written on box
%define distro_release %{version}

# The distro branch: Cooker, Community or Official
%define distro_branch %{distrib}

# The distro arch, notice: using %_target_cpu is bad
# elsewhere because this depend of the config of the packager
# _target_cpu => package build for
# distro_arch => the distribution we are using
%define distro_arch %{_target_cpu}

%define major %(printf %u %(echo %{version}|cut -d. -f1))
%define minor %([ -z "%(echo %{version}|cut -d. -f2)" ] && echo 0 || printf %u %(echo %{version}|cut -d. -f2))
%define subminor %([ -z "%(echo %{version}|cut -d. -f3)" ] && echo 0 || printf %u %(echo %{version}|cut -d. -f3))
%if %am_i_cooker || %am_i_rolling
# 22.12 looks better as omv2212 than omv22012...
%define distro_tag %(echo $((%{major}*100+%{minor})))
%define version_tag %(echo $((%{major}*1000000+%{minor}*1000+%{subminor})))
%else
%define distro_tag %(echo $((%{major}*1000+%{minor})))
%define version_tag %(echo $((%{major}*1000000+%{minor}*1000+%{subminor})))
%endif
%define mdkver %{version_tag}

%ifarch %{x86_64}
%global secondary_distarch i686
%else
%ifarch %{aarch64}
%global secondary_distarch armv7hnl
%endif
%endif

Summary:	%{new_distribution} release file
Name:		distro-release
Version:	22.12
# (tpg) something needs to be done to make comparision 3.0 > 2015.0 came true
# 3001 = 3.1
# 3001 = 3.2 etc.
DistTag:	%{shorttag}%{distro_tag}
Release:	1
License:	GPLv2+
URL:		https://github.com/OpenMandrivaSoftware/distro-release
Source0:	https://github.com/OpenMandrivaSoftware/distro-release/archive/%{version}/%{name}-%{version}.tar.gz
Group:		System/Configuration/Other

%description
%{distribution} release file.

%package common
Summary:	%{new_distribution} release common files
Group:		System/Configuration/Other
BuildArch:	noarch
%rename		mandriva-release-common
%rename		opemandriva-release-common
%rename		mandriva-release
%rename		common-licenses
Requires:	lsb-release
Requires:	setup
Requires:	filesystem
# cf mdvbz#32631
Provides:	arch(%{_target_cpu})
Provides:	%{arch_tagged distro-release-common}

%description common
Common files for %{new_distribution} release packages.

# build release flavour rpm
%package %{new_vendor}
Summary:	%{new_vendor} release file
Group:		System/Configuration/Other
Requires:	%{name}-common = %{version}-%{release}
Requires:	%{arch_tagged distro-release-common}
Requires:	%{name}-common >= %{version}
Provides:	mandriva-release = %{version}-%{release}
Provides:	distro-release = %{version}-%{release}
Provides:	system-release
Provides:	system-release(%{version})
Provides:	system-release(releasever) = %{version}

%description %{new_vendor}
%{new_distribution} release file for %{new_vendor} flavor.

%files %{new_vendor}
%{_rpmmacrodir}/macros.%{new_vendor}
%{_sysconfdir}/os-release.%{vendor_tag}
%{_sysconfdir}/%{vendor_tag}-release
%{_sysconfdir}/product.id.%{new_vendor}
%{_sysconfdir}/version.%{vendor_tag}
%{_sysconfdir}/os-release
%{_prefix}/lib/os-release
%{_sysconfdir}/release
%{_sysconfdir}/product.id
%{_sysconfdir}/version

%if %{without bootstrap}
%package desktop-Plasma
Summary:	Plasma desktop configuration
Group:		Graphical desktop/KDE
BuildRequires:	cmake(ECM)
Requires:	%{name}-desktop >= %{version}
Requires:	%{name}-theme >= %{version}
Requires:	breeze
Requires:	breeze-gtk
Requires:	breeze-icons
Requires:	noto-sans-fonts
%rename		distro-plasma-config
BuildArch:	noarch

%description desktop-Plasma
KDE Plasma desktop configuration.
%endif

#package desktop-Xfce
#description desktop-Xfce

%package theme
Summary:	Themes for %{distribution}
Group:		Graphics
BuildRequires:	imagemagick
BuildRequires:	fontconfig
BuildRequires:	fonts-ttf-dejavu
BuildRequires:	urw-fonts
Provides:	plymouth(system-theme)
Requires:	%{name}
%ifnarch %{armx} %{riscv}
Requires:	plymouth-plugin-script
Requires(post):	plymouth-scripts
Requires:	grub2
%else
Requires:	plymouth-theme-bgrt
%endif
%rename		distro-theme
%rename		grub2-theme
%rename		grub2-theme-common
%rename		grub2-openmandriva-theme
%rename		grub2-OpenMandriva-theme
%rename		distro-theme-common
%rename		distro-theme-extra
%rename		distro-theme-screensaver
%rename		distro-theme-OpenMandriva-screensaver
%rename		distro-theme-OpenMandriva
%rename		distro-theme-OpenMandriva-grub2
%rename		mandriva-theme-common
%rename		mandriva-theme-extra
%rename		mandriva-screensaver
%rename		mandriva-theme-screensave
%rename		mandriva-theme-OpenMandriva
%rename		om-wallpapers-extra
Obsoletes:	distro-theme-OpenMandriva < 0:1.4.46.2-2
BuildArch:	noarch

%description theme
This package provides default themes for %{distribution}'s components:
 - bootloader/grub
 - screensaver
 - plymouth
 - wallpapers

%package repos
Summary:	%{new_vendor} package repositories
Group:		System/Base
License:	MIT
Provides:	openmandriva-repos(%{version})
Requires:	system-release(%{version})
Requires:	%{name}-repos-pkgprefs = %{version}-%{release}
Requires:	%{name}-repos-keys = %{version}-%{release}
%rename		openmandriva-repos-cooker
%rename		openmandriva-repos

%description repos
%{new_vendor} package repository files for DNF and PackageKit
with GPG public keys.

%package repos-keys
Summary:	%{new_vendor} repository GPG keys
Group:		System/Base
%rename	openmandriva-repos-keys
# GPG keys are architecture independent
BuildArch:	noarch

%description repos-keys
%{new_vendor} GPG keys for validating packages from %{new_vendor} repositories by
DNF and PackageKit.

%package repos-pkgprefs
# (ngompa): See the following page on why this exists:
# https://fedoraproject.org/wiki/PackagingDrafts/ProvidesPreferences#Distribution_preference
Summary:	%{new_vendor} repository package preferences
Group:		System/Base
%rename	openmandriva-repos-pkgprefs
# Preferences list is architecture independent
BuildArch:	noarch
## Base packages
# webfetch
Suggests:	curl
# webclient
Suggests:	lynx
%ifnarch %{armx} %{riscv}
# bootloader
Suggests:	grub2
%endif
# vim
Suggests:	vim-enhanced
# libEGL.so.1 (also provided by proprietary drivers)
Suggests:	libegl1
Suggests:	lib64egl1
# libGL.so.1 (also provided by proprietary drivers)
Suggests:	libgl1
Suggests:	lib64gl1
# Prefer openssh-askpass over openssh-askpass-gnome (for keychain)
Suggests:	openssh-askpass
# Python 3.x
Suggests:	python
# Initrd
Suggests:	dracut
## Multimedia
# festival-voice
Suggests:	festvox-kallpc16k
# gnome-speech-driver
Suggests:	gnome-speech-driver-espeak
# esound
Suggests:	pulseaudio-esound-compat
# gst-install-plugins-helper
Suggests:	packagekit-gstreamer-plugin
# libbaconvideowidget.so.0 (totem backend)
Suggests:	libbaconvideowidget-gstreamer0
Suggests:	lib64baconvideowidget-gstreamer0
# phonon-backend: prefer phonon-vlc over phonon-gstreamer
Suggests:	phonon-gstreamer
# phonon4qt5-backend: prefer phonon4qt5-vlc over phonon4qt5-gstreamer
Suggests:	phonon4qt5-gstreamer
# mate backends
Suggests:	mate-settings-daemon-pulse
Suggests:	mate-media-pulse
## Devel
# xemacs-extras provides ctags, prefer simple ctags
Suggests:	ctags
# prefer openssl-devel over libressl-devel
Suggests:	libopenssl-devel
Suggests:	lib64openssl-devel
# preferred compiler(s)
Suggests:	clang
## Servers
# sendmail-command and mail-server
Suggests:	postfix
# imap-server
Suggests:	dovecot
# webserver
Suggests:	apache
# nfs-server
Suggests:	nfs-utils
# ftpserver
Suggests:	proftpd
# postgresql
Suggests:	libpq5
Suggests:	lib64pq5
# vnc
Suggests:	tigervnc
# x2goserver database backend
Suggests:	x2goserver-sqlite
## Various
# sane (also provided by saned)
Suggests:	sane-backends
# skanlite vs. xsane
Suggests:	skanlite
# virtual-notification-daemon
Suggests:	notification-daemon
# sgml-tools
# (the other choice is linuxdoc-tools which requires docbook-utils anyway)
Suggests:	docbook-utils
# input method
Suggests:	fcitx
# drupal database storage
Suggests:	drupal-mysql
# polkit-agent
Suggests:	polkit-kde-agent-1
# java
Suggests:	jre-current
Suggests:	jdk-current
# java-plugin
Suggests:	icedtea-web
Suggests:	lxsession-lite
# pinentry
Suggests:	pinentry-qt5
# %{_lib}qt5-output-driver
Suggests:	libqt5gui-eglfs

%description repos-pkgprefs
This package supplies DNF and PackageKit with global
preferences for packages in which multiple options are possible.

%package rpm-setup
Summary:	Macros and scripts for %{new_vendor} specific rpm behavior
Group:		System/Configuration/Packaging
License:	MIT
Requires:	rpm >= 2:4.14.2-0
BuildArch:	noarch
%rename rpm-openmandriva-setup

%description rpm-setup
Macros and scripts for %{new_vendor} specific rpm behavior.

%package rpm-setup-build
Summary:	Macros and scripts for %{new_vendor} specific rpmbuild behavior
Group:		System/Configuration/Packaging
%rename		rpm-openmandriva-setup-build
# (tpg) do not use %%EVRD here, as it does not exist yet
Requires:	%{name}-rpm-setup = %{version}-%{release}
Requires:	basesystem-build

%description rpm-setup-build
Macros and scripts for %{new_vendor} specific rpmbuild behavior.

%package installer
Summary:	Installer configuration for %{distribution}
Group:		Graphics
Conflicts:	calamares < 3.2.20-5
Requires:	%{name} = %{version}-%{release}

%description installer
Installer configuration files for %{distribution}.

%package indexhtml
Summary:	%{new_vendor} html welcome page
Group:		System/Base
BuildArch:	noarch
BuildRequires:	intltool
Requires(pre):	distro-release
Requires(post):	gawk
Requires(post):	coreutils
Requires(post):	sed
Obsoletes:	indexhtml < 1:0
Provides:	indexhtml = 1:%{version}-%{release}

%description indexhtml
%{new_vendor} index.html welcome page displayed by web browsers
when they are launched, first mail displayed on mail clients
after installation and "about" information.

%package rpmlint-policy
Summary:	Rpmlint %{new_vendor} policy
Group:		Development/Other
License:	GPLv2+
URL:		%{disturl}
BuildArch:	noarch
BuildRequires:	rpmlint >= 1.10
BuildRequires:	python >= 3
Requires:	rpmlint >= 1.10
Provides:	rpmlint-%{_target_vendor}-policy = %{EVRD}
%rename		rpmlint-mandriva-policy
%rename		rpmlint-distro-policy

%description rpmlint-policy
Official rpmlint %{new_vendor} policy, install this if you
want to produce RPMs for %{new_vendor}.

# WARNING !!!
# Keep it as last one as it sets EPOCH
# desktop-common-data
%package desktop
Summary:	Desktop common files
Group:		System/Configuration/Other
Epoch:		2
BuildArch:	noarch
Requires:	distro-release
Requires:	filesystem
#XDG stuff
Requires:	libxdg-basedir
Requires:	xdg-compliance
Requires:	xdg-user-dirs
Requires:	xdg-utils
Requires:	run-parts
Requires(post):	hicolor-icon-theme
Requires:	hicolor-icon-theme
Requires(post):	etcskel
Requires(post):	run-parts
Requires:	shared-mime-info
%rename		mandrake_desk
%rename		menu
%rename		menu-xdg
%rename		faces-openmandriva
%rename		faces-icons
%rename		desktop-common-data
Obsoletes:	desktop-common-data < 1:4.2-4

%description desktop
This package contains useful icons, menu structure and others goodies for the
%{distribution} desktop.

%prep
%autosetup -p1
# check that CREDITS file is in UTF-8, fail otherwise
if iconv -f utf-8 -t utf-8 < doc/CREDITS > /dev/null
then
    true
else
    printf '%s\n' "The CREDITS file *MUST* be encoded in UTF-8"
    printf '%s\n' "Please fix it before continuing"
    false
fi

%install
mkdir -p %{buildroot}%{_sysconfdir}
ln -sf release %{buildroot}%{_sysconfdir}/mandriva-release
ln -sf release %{buildroot}%{_sysconfdir}/redhat-release
ln -sf release %{buildroot}%{_sysconfdir}/mandrake-release
ln -sf release %{buildroot}%{_sysconfdir}/mandrakelinux-release
ln -sf release %{buildroot}%{_sysconfdir}/system-release

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/10distro-release.csh << EOF
if ( -r %{_sysconfdir}/sysconfig/system ) then
    eval $(sed 's|^#.*||' %{_sysconfdir}/sysconfig/system | sed 's|\([^=]*\)=\([^=]*\)|set \1=\2|g' | sed 's|$|;|')
    setenv META_CLASS $META_CLASS
else
    setenv META_CLASS unknown
endif
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/10distro-release.sh << EOF
if [ -r %{_sysconfdir}/sysconfig/system ]; then
    . %{_sysconfdir}/sysconfig/system
    export META_CLASS
else
    export META_CLASS=unknown
fi
EOF

echo %{buildroot}%{_sysconfdir}/product.id.%{new_vendor}
cat >%{buildroot}%{_sysconfdir}/product.id.%{new_vendor} <<EOF
vendor=%{new_vendor},distribution=%{new_distribution},type=%{product_type},version=%{version},branch=%{product_branch},release=%{product_release},arch=%{product_arch},product=%{new_distribution}
EOF

mkdir -p %{buildroot}%{_rpmmacrodir}
cat >%{buildroot}%{_rpmmacrodir}/macros.%{new_vendor} <<EOF
%%distro_release	%{version}
%%distro_branch		%distro_branch
%%distro_class		%%(. %{_sysconfdir}/sysconfig/system; echo \\\$META_CLASS)
# (tpg) legacy stuff should be removed after all packages do not use macros begining with %%mandriva\
%%mandriva_release	%{version}
%%mandriva_branch	%mandriva_branch
%%mdkver		%mdkver
%%mdvver		%%mdkver
%%omvver		%%mdkver
# productid variable
%%product_id vendor=%{vendor_tag},distribution=%{new_distribution},type=%{product_type},version=%{version},branch=%{product_branch},release=%{product_release},arch=%{product_arch},product=%{new_distribution}
%%product_vendor	%{vendor_tag}
%%product_distribution	%{new_distribution}
%%product_type		%{product_type}
%%product_version	%{version}
%%product_branch	%{product_branch}
%%product_release	%{product_release}
%%product_arch		%{product_arch}
%%product_product	%{new_product}
%%distribution		%{new_distribution}
%%_distribution		%{distribution_tag}
%%disturl		%{new_disturl}
%%bugurl		%{new_bugurl}
%%vendor		%{new_vendor}
%%_vendor		%{vendor_tag}
%%distsuffix		%{shorttag}
%%distrelease		%{distro_tag}
EOF

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_prefix}/lib
cat > %{buildroot}%{_sysconfdir}/sysconfig/system <<EOF
SECURITY=3
CLASS=beginner
LIBSAFE=no
META_CLASS=download
EOF

cat >%{buildroot}%{_sysconfdir}/%{vendor_tag}-release <<EOF
%{new_distribution} release %{version} (%{new_codename}) %{distrib} for %{_target_cpu}
EOF
cat >%{buildroot}%{_sysconfdir}/version.%{vendor_tag} <<EOF
%{version} %{release} (%{new_codename}) %{distrib}
EOF

# (tpg) follow standard specifications http://www.freedesktop.org/software/systemd/man/os-release.html
cat >%{buildroot}%{_prefix}/lib/os-release <<EOF
NAME="%{new_distribution}"
VERSION="%{version} (%{new_codename}) %{distrib}"
ID="%{vendor_tag}"
VERSION_ID="%{version}"
PRETTY_NAME="%{new_distribution} %{version} (%{new_codename}) %{distrib}"
BUILD_ID="%(printf "%s\n" %(date +"%Y%m%d.%H"))"
VERSION_CODENAME="%(printf "%s\n" %{new_codename} |tr A-Z a-z)"
ANSI_COLOR="1;43"
LOGO="%{vendor_tag}"
CPE_NAME="cpe:/o:%{vendor_tag}:%{distribution_tag}:%{version}"
HOME_URL="%{new_disturl}"
BUG_REPORT_URL="%{new_bugurl}"
SUPPORT_URL="https://forum.openmandriva.org"
PRIVACY_POLICY_URL="https://www.openmandriva.org/tos"
EOF

ln -s %{_prefix}/lib/os-release %{buildroot}%{_sysconfdir}/os-release
ln -s %{_prefix}/lib/os-release %{buildroot}%{_sysconfdir}/os-release.%{vendor_tag}
ln -s %{vendor_tag}-release %{buildroot}%{_sysconfdir}/release
ln -s product.id.%{new_vendor} %{buildroot}%{_sysconfdir}/product.id
ln -s version.%{vendor_tag} %{buildroot}%{_sysconfdir}/version

mkdir -p %{buildroot}%{_datadir}/common-licenses/*
cp -a common-licenses %{buildroot}%{_datadir}/

### DESKTOP ###

## Install backgrounds
# User & root's backgrounds
install -d -m 0755 %{buildroot}%{_datadir}/mdk/backgrounds

# for easy access for users looking for wallpapers at expected location
install -d -m 0755 %{buildroot}%{_datadir}/wallpapers
ln -s %{_datadir}/mdk/backgrounds %{buildroot}%{_datadir}/wallpapers/mdk

## Install scripts
install -d -m 0755 %{buildroot}/%{_bindir}/
install -m 0755 desktops/bin/editor %{buildroot}/%{_bindir}/
install -m 0755 desktops/bin/www-browser %{buildroot}/%{_bindir}/
install -m 0755 desktops/bin/xvt %{buildroot}/%{_bindir}/

## Install faces
install -d -m 0755 %{buildroot}/%{_datadir}/mdk/faces/
install -d -m 0755 %{buildroot}/%{_datadir}/faces/
cp -a desktops/faces/*.png %{buildroot}/%{_datadir}/mdk/faces/

# David - 9.0-5mdk - For KDE
ln -s %{_datadir}/mdk/faces/default.png %{buildroot}%{_datadir}/faces/default.png

# David - 9.0-5mdk - For GDM
ln -s %{_datadir}/mdk/faces/default.png %{buildroot}%{_datadir}/faces/user-default-mdk.png

# (tpg) default desktop files (do not place them in /etc/skel/Desktop !)
install -d -m 0755 %{buildroot}%{_datadir}/applications
install -m 0644 desktops/applications/*.desktop %{buildroot}%{_datadir}/applications

# icons
install -d -m 0755 %{buildroot}%{_iconsdir}/hicolor/scalable/apps
cp -a theme/icons/*.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/

# install bookmarks
install -d -m 0755 %{buildroot}%{_datadir}/mdk/bookmarks/konqueror
for i in desktops/bookmarks/konqueror/*.html ; do
  install -m 0644 $i %{buildroot}%{_datadir}/mdk/bookmarks/konqueror
done

install -d -m 0755 %{buildroot}%{_datadir}/mdk/bookmarks/mozilla
for i in desktops/bookmarks/mozilla/*.html ; do
    install -m 0644 $i %{buildroot}%{_datadir}/mdk/bookmarks/mozilla
done

mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus
ln -s ../kde5/menus/kde-applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/applications.menu
ln -s ../kde5/menus/kde-applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/kde-applications.menu
ln -s ../kde5/menus/kde-applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/gnome-applications.menu
### DESKTOP END ###

%if %{without bootstrap}
### DESKTOP PLASMA ###

mkdir -p %{buildroot}%{_sysconfdir}/xdg
mkdir -p %{buildroot}%{_sysconfdir}/xdg/KDE
mkdir -p %{buildroot}%{_sysconfdir}/xdg/QtProject
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart-scripts
mkdir -p %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env
mkdir -p %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/shutdown
mkdir -p %{buildroot}%{_datadir}/kservices5
mkdir -p %{buildroot}%{_datadir}/plasma/shells/org.kde.plasma.desktop/contents
mkdir -p %{buildroot}%{_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.defaultPanel/contents
mkdir -p %{buildroot}%{_datadir}/konsole

for i in kcmdisplayrc kcmfonts kcminputrc kdeglobals kscreenlockerrc ksplashrc kwinrc plasmarc startupconfig startupconfigfiles kcm-about-distrorc ksmserverrc kiorc dolphinrc konsolerc klaunchrc discoverabstractnotifier.notifyrc plasma_workspace.notifyrc powermanagementprofilesrc; do
    install -m 0644 desktops/Plasma/$i %{buildroot}%{_sysconfdir}/xdg/$i
done

install -m 0644 desktops/Plasma/metadata.desktop %{buildroot}%{_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.defaultPanel/metadata.desktop
install -m 0644 desktops/Plasma/metadata.desktop %{buildroot}%{_datadir}/kservices5/plasma-layout-template-org.openmandriva.plasma.desktop.defaultPanel.desktop
install -m 0644 desktops/Plasma/org.kde.plasma.desktop-layout.js %{buildroot}%{_datadir}/plasma/shells/org.kde.plasma.desktop/contents/layout.js
install -m 0644 desktops/Plasma/org.openmandriva.plasma.desktop.defaultPanel-layout.js %{buildroot}%{_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.defaultPanel/contents/layout.js
install -m 0644 desktops/Plasma/plasma-firstsetup.sh %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env/plasma-firstsetup.sh
ln -sf %{_sysconfdir}/xdg/plasma-workspace/env/plasma-firstsetup.sh %{buildroot}%{_sysconfdir}/xdg/autostart-scripts/plasma-firstsetup.sh
install -m 0644 desktops/Plasma/Sonnet.conf %{buildroot}%{_sysconfdir}/xdg/KDE/Sonnet.conf
install -m 0644 desktops/Plasma/kdeglobals.sh %{buildroot}%{_sysconfdir}/xdg/plasma-workspace/env/kdeglobals.sh
ln -sf %{_sysconfdir}/xdg/plasma-workspace/env/kdeglobals.sh %{buildroot}%{_sysconfdir}/xdg/autostart-scripts/kdeglobals.sh
install -m 0644 desktops/Plasma/qtlogging.ini %{buildroot}%{_sysconfdir}/xdg/QtProject/qtlogging.ini
install -m 0644 desktops/Plasma/OM.profile %{buildroot}%{_datadir}/konsole/OM.profile
mkdir -p %{buildroot}%{_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.globalMenuPanel/contents
install -m 0644 desktops/Plasma/org.openmandriva.plasma.desktop.globalMenuPanel-layout.js %{buildroot}%{_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.globalMenuPanel/contents/layout.js
install -m 0644 desktops/Plasma/metadata-globalMenu.desktop %{buildroot}%{_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.globalMenuPanel/metadata.desktop
mkdir -p %{buildroot}%{_datadir}/plasma/look-and-feel
cp -a desktops/Plasma/org.openmandriva5.desktop %{buildroot}%{_datadir}/plasma/look-and-feel/org.openmandriva5.desktop

### DESKTOP PLASMA END ###
%endif

### THEME ###

# Make sure the logo can be found where modern applications expect it
mkdir -p %{buildroot}%{_iconsdir}/hicolor/scalable/apps
cp theme/icons/openmandriva.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
for i in 16 22 24 32 36 48 64 72 96 128 192 256 512; do
    mkdir -p %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
    convert -background none theme/icons/openmandriva.svg %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/openmandriva.png
done
ln -s hicolor/scalable/apps/openmandriva.svg %{buildroot}%{_iconsdir}/

# Default wallpaper should be available without browsing file system
mkdir -p %{buildroot}%{_datadir}/wallpapers
cp -a theme/backgrounds/*.*g %{buildroot}%{_datadir}/mdk/backgrounds
cp -r theme/wallpapers/OpenMandriva %{buildroot}%{_datadir}/wallpapers
[ ! -f %{buildroot}%{_datadir}/wallpapers/OpenMandriva/contents/images/2560x1600.png ] && printf '%s\n' "Default wallpaper file is missing!" && exit 1

ln -s %{_datadir}/wallpapers/OpenMandriva/contents/images/2560x1600.png %{buildroot}%{_datadir}/wallpapers/default.jpg
ln -s %{_datadir}/wallpapers/OpenMandriva/contents/images/2560x1600.png %{buildroot}%{_datadir}/wallpapers/default.png
ln -s %{_datadir}/wallpapers/OpenMandriva/contents/images/2560x1600.png %{buildroot}%{_datadir}/mdk/backgrounds/default.jpg
ln -s %{_datadir}/wallpapers/OpenMandriva/contents/images/2560x1600.png %{buildroot}%{_datadir}/mdk/backgrounds/default.png

mkdir -p %{buildroot}%{_datadir}/mdk/screensaver
cp -a theme/screensaver/*.jpg %{buildroot}%{_datadir}/mdk/screensaver

mkdir -p %{buildroot}%{_datadir}/pixmaps
cp -a theme/pixmaps/*.*g %{buildroot}%{_datadir}/pixmaps

# (tpg) we are using bgrt plymouth theme
%ifnarch %{armx} %{riscv}
mkdir -p %{buildroot}%{_datadir}/plymouth/themes
cp -a theme/plymouth/%{vendor} %{buildroot}%{_datadir}/plymouth/themes/
%endif

# (tpg) currently our os-image-builder tool supports:
# uboot with extlinux
# systemd-boot

%ifnarch %{armx} %{riscv}
mkdir -p %{buildroot}/boot/grub2/themes/%{vendor}
cp -a theme/grub/%{vendor}/* %{buildroot}/boot/grub2/themes/%{vendor}
rm -rf %{buildroot}/boot/grub2/themes/%{vendor}/05_theme
mkdir -p %{buildroot}%{_sysconfdir}/grub.d
install -m755 theme/grub/%{vendor}/05_theme %{buildroot}%{_sysconfdir}/grub.d/05_theme
mkdir -p %{buildroot}%{_sysconfdir}/default/
cat > %{buildroot}%{_sysconfdir}/default/grub.%{vendor} << EOF
GRUB_THEME=/boot/grub2/themes/%{vendor}/theme.txt
GRUB_BACKGROUND=/boot/grub2/themes/%{vendor}/background.png
GRUB_DISTRIBUTOR="%{distribution}"
EOF
%endif

### THEME END ###

### REPOS ###
ARCH=%{_target_cpu}
echo $ARCH |grep -q arm && ARCH=armv7hnl
[ "$ARCH" = "i386" ] && ARCH=i686
[ "$ARCH" = "i586" ] && ARCH=i686

# Install the GPG key
mkdir -p %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install rpm/RPM-GPG-KEY-%{vendor} -pm 0644 %{buildroot}%{_sysconfdir}/pki/rpm-gpg

# Install the repositories
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d

%if %{defined secondary_distarch}
SECONDARY_ARCH=%{secondary_distarch}
%else
SECONDARY_ARCH=""
%endif

for arch in ${ARCH} ${SECONDARY_ARCH}; do
    for release in release rock rolling cooker; do
	for repo in main unsupported restricted non-free; do
	    case "$repo" in
			main)
				REPO=""
				REPONAME=""
                                ;;
			*)
				REPO="-$repo"
				REPONAME=" - $(echo $repo |cut -b1 |tr a-z A-Z)$(echo $repo |cut -b2-)"
				;;
			esac

			vertag=$release
			case "$release" in
			release)
				NAME='OpenMandriva $releasever'"$REPONAME - $arch"
				HAS_UPDATES=true
				vertag='$releasever'
				;;
			rock)
				NAME="OpenMandriva Rock$REPONAME - $arch"
				HAS_UPDATES=true
				;;
			rolling)
				NAME="OpenMandriva Rolling$REPONAME - $arch"
				HAS_UPDATES=false
				;;
			cooker)
				NAME="OpenMandriva Cooker$REPONAME - $arch"
				HAS_UPDATES=false
				;;
                        esac
                        cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-$arch$REPO]
name="$NAME"
baseurl=http://mirror.openmandriva.org/${vertag}/repository/${arch}/${repo}/release/
	http://abf-downloads.openmandriva.org/${vertag}/repository/${arch}/${repo}/release/
# Alternative if mirror.openmandriva.org is down
# mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=${repo}&release=release
# fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
type=rpm-md
enabled=0

EOF

if $HAS_UPDATES; then
    cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-updates-$arch$REPO]
name="$NAME - Updates"
baseurl=http://mirror.openmandriva.org/${vertag}/repository/${arch}/${repo}/updates/
	http://abf-downloads.openmandriva.org/${vertag}/repository/${arch}/${repo}/updates/
# Alternative if mirror.openmandriva.org is down
#mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=${repo}&release=updates
#fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF
fi

    cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-testing-$arch$REPO]
name="$NAME - Testing"
baseurl=http://mirror.openmandriva.org/${vertag}/repository/${arch}/${repo}/testing/
	http://abf-downloads.openmandriva.org/${vertag}/repository/${arch}/${repo}/testing/
# Alternative if mirror.openmandriva.org is down
#mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=${repo}&release=testing
#fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF

    cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-$arch$REPO-debuginfo]
name="$NAME - Debug"
baseurl=http://mirror.openmandriva.org/${vertag}/repository/${arch}/debug_${repo}/release/
	http://abf-downloads.openmandriva.org/${vertag}/repository/${arch}/debug_${repo}/release/
# Alternative if mirror.openmandriva.org is down
#mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=debug_${repo}&release=release
#fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF

if $HAS_UPDATES; then
    cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-updates-$arch$REPO-debuginfo]
name="$NAME - Updates - Debug"
baseurl=http://mirror.openmandriva.org/${vertag}/repository/${arch}/debug_${repo}/updates/
	http://abf-downloads.openmandriva.org/${vertag}/repository/${arch}/debug_${repo}/updates/
# Alternative if mirror.openmandriva.org is down
#mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=debug_${repo}&release=updates
#fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF
fi

cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch.repo <<EOF
[$release-testing-$arch$REPO-debuginfo]
name="$NAME - Testing - Debug"
baseurl=http://mirror.openmandriva.org/${vertag}/repository/${arch}/debug_${repo}/testing/
	http://abf-downloads.openmandriva.org/${vertag}/repository/${arch}/debug_${repo}/testing/
# Alternative if mirror.openmandriva.org is down
#mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=${arch}&repo=debug_${repo}&release=testing
#fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF

cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch-source.repo <<EOF
[$release-$arch$REPO-source]
name="$NAME - Source"
baseurl=http://mirror.openmandriva.org/${vertag}/repository/SRPMS/${repo}/release/
	http://abf-downloads.openmandriva.org/${vertag}/repository/SRPMS/${repo}/release/
# Alternative if mirror.openmandriva.org is down
#mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=SRPMS&repo=${repo}&release=release
#fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF

if $HAS_UPDATES; then
    cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch-source.repo <<EOF
[$release-updates-$arch$REPO-source]
name="$NAME - Updates - Source"
baseurl=http://mirror.openmandriva.org/${vertag}/repository/SRPMS/${repo}/updates/
	http://abf-downloads.openmandriva.org/${vertag}/repository/SRPMS/${repo}/updates/
# Alternative if mirror.openmandriva.org is down
#mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=SRPMS&repo=${repo}&release=updates
#fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF
fi

cat >>%{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-$release-$arch-source.repo <<EOF
[$release-testing-$arch$REPO-source]
name="$NAME - Testing - Source"
baseurl=http://mirror.openmandriva.org/${vertag}/repository/SRPMS/${repo}/testing/
	http://abf-downloads.openmandriva.org/${vertag}/repository/SRPMS/${repo}/testing/
# Alternative if mirror.openmandriva.org is down
#mirrorlist=http://mirrors.openmandriva.org/mirrors.php?platform=$vertag&arch=SRPMS&repo=${repo}&release=testing
#fastestmirror=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva
enabled=0
type=rpm-md

EOF
                done
        done
done
sed -i '$ d' %{buildroot}%{_sysconfdir}/yum.repos.d/*.repo

## And enable the one we're installing from
%if %am_i_cooker
sed -e '0,/enabled=0/s//enabled=1/' -i %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-cooker-${ARCH}.repo
%else
%if %am_i_rolling
sed -e '0,/enabled=0/s//enabled=1/' -i %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-rolling-${ARCH}.repo
%else
# Second occurence in $RELEASE and Rock is updates/
sed -e '0,/enabled=0/s//enabled=1/' -i %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-rock-${ARCH}.repo
sed -e '0,/enabled=0/s//enabled=1/' -i %{buildroot}%{_sysconfdir}/yum.repos.d/openmandriva-rock-${ARCH}.repo
%endif
%endif

chmod 0644 %{buildroot}%{_sysconfdir}/yum.repos.d/*.repo

### REPOS END ###

### RPM SETUP ###
mkdir -p %{buildroot}%{_rpmconfigdir}/{openmandriva,fileattrs,macros.d}
cp -a rpm/user/openmandriva/* %{buildroot}%{_rpmconfigdir}/openmandriva
cp -a rpm/build/openmandriva/* %{buildroot}%{_rpmconfigdir}/openmandriva
cp -a rpm/build/fileattrs/* %{buildroot}%{_rpmconfigdir}/fileattrs
cp -a rpm/build/macros.d/* %{buildroot}%{_rpmconfigdir}/macros.d

mkdir -p %{buildroot}%{_rpmluadir}/fedora/srpm
cp -a rpm/build/fedora/common.lua %{buildroot}%{_rpmluadir}/fedora
cp -a rpm/build/fedora/forge.lua %{buildroot}%{_rpmluadir}/fedora/srpm

### RPM SETUP END ###

### INSTALLER ###
mkdir -p %{buildroot}%{_sysconfdir}/calamares/modules
install -m644 installer/settings.conf %{buildroot}%{_sysconfdir}/calamares/settings.conf
for i in bootloader.conf displaymanager.conf finished.conf fstab.conf grubcfg.conf keyboard.conf locale.conf machineid.conf mount.conf packages.conf partition.conf preservefiles.conf removeuser.conf services-systemd.conf shellprocess.conf umount.conf unpackfs.conf users.conf webview.conf welcome.conf ; do
    install -m644 installer/$i %{buildroot}%{_sysconfdir}/calamares/modules/$i
done

mkdir -p %{buildroot}%{_sysconfdir}/calamares/branding/auto
for i in 2015-ads_01.png 2015-ads_02.png 2015-ads_03.png 2015-ads_04.png 2015-ads_05.png 2015-ads_06.png 2015-ads_07.png adverts.qml ; do
    install -m644 installer/$i %{buildroot}%{_sysconfdir}/calamares/branding/auto/$i
done

cat > %{buildroot}%{_sysconfdir}/calamares/branding/auto/branding.desc <<EOF
---
componentName:  auto

strings:
    productName:         "%{new_distribution}"
    shortProductName:    "%{new_distribution}"
    version:             "%{version} (%{new_codename})"
    shortVersion:        "%{version} (%{new_codename})"
    versionedName:       "%{new_distribution} %{version} (%{new_codename})"
    shortVersionedName:  "%{new_distribution} %{version} (%{new_codename})"
    bootloaderEntryName: "openmandriva"
    productUrl:          "%{new_disturl}"
    supportUrl:          "%{new_bugurl}"
    knownIssuesUrl:      "https://wiki.openmandriva.org/en/distribution/releases/current"
    releaseNotesUrl:     "https://wiki.openmandriva.org/en/distribution/releases/current"

images:
    productLogo:         "%{_iconsdir}/hicolor/scalable/apps/openmandriva.svg"
    productIcon:         "%{_iconsdir}/hicolor/scalable/apps/openmandriva.svg"
# (tpg) need to decide what show here
#    productWelcome:      "languages.png"

slideshow:               "adverts.qml"
slideshowAPI: 2

style:
   sidebarBackground:    "#263039"
   sidebarText:          "#FFFFFF"
   sidebarTextSelect:    "#292F34"
EOF

### INSTALLER END ###

### INDEXHTML ###
cd doc/indexhtml/about
./create_html.sh
cd -

install -d -m755 %{buildroot}%{_datadir}/mdk/indexhtml/
cp -a doc/indexhtml/HTML/* %{buildroot}%{_datadir}/mdk/indexhtml/

install -d -m755 %{buildroot}%{_datadir}/mdk/mail/text/
install -d -m755 %{buildroot}%{_datadir}/mdk/mail/html/
for lang in $(find doc/indexhtml/mail/header-* -type f | sed "s|doc/indexhtml/mail/header-||" ); do
    cat doc/indexhtml/mail/header-$lang &> tmpfile
    cat doc/indexhtml/mail/mail-$lang.txt >> tmpfile
    install -m 0644 tmpfile %{buildroot}%{_datadir}/mdk/mail/text/mail-$lang
    cat doc/indexhtml/mail/header-$lang &> tmpfile
    printf "%s\n" "Content-Type: multipart/related; type=\"multipart/alternative\";" >>tmpfile
    printf "%s\n" "   boundary=\"=-tThpx1YEZqL4gn53WjQ1\"" >> tmpfile
    printf "%s\n" "" >> tmpfile
    printf "%s\n" "--=-tThpx1YEZqL4gn53WjQ1" >> tmpfile
    printf "%s\n" "Content-Type: multipart/alternative; boundary=\"=-aFPGjTr5jUHhXPWxbLcT\"" >>tmpfile
    printf "%s\n" "" >> tmpfile
    printf "%s\n" "--=-aFPGjTr5jUHhXPWxbLcT" >> tmpfile
    cat doc/indexhtml/mail/mail-$lang.txt >> tmpfile
    cat doc/indexhtml/mail/mail-$lang.html >> tmpfile
#    cat doc/indexhtml/mail/mail-images >> tmpfile
    install -m 0644 tmpfile %{buildroot}%{_datadir}/mdk/mail/html/mail-$lang
done

# about OpenMandriva
install -d -m755 %{buildroot}%{_datadir}/mdk/about
install -d -m755 %{buildroot}%{_datadir}/applications
install -d -m755 %{buildroot}%{_bindir}
cp doc/indexhtml/about/html/* %{buildroot}%{_datadir}/mdk/about
cp -r doc/indexhtml/about/style %{buildroot}%{_datadir}/mdk/about/
cp doc/indexhtml/about/about-openmandriva-lx.desktop %{buildroot}%{_datadir}/applications
cp doc/indexhtml/about/about-openmandriva-lx %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/doc/HTML/
ln -s %{_datadir}/mdk/indexhtml/index.html %{buildroot}%{_datadir}/doc/HTML/index.html

### INDEXHTML END ###

### RPMLINT POLICY ###
install -d -m755 %{buildroot}%{_datadir}/rpmlint/config.d
cp -f rpm/rpmlint/distribution.error.conf %{buildroot}%{_datadir}/rpmlint/config.d/
cp -f rpm/rpmlint/distribution.error.list %{buildroot}%{_datadir}/rpmlint/config.d/
cp -f rpm/rpmlint/distribution.exceptions.conf %{buildroot}%{_datadir}/rpmlint/config.d/

## RPMLINT POLICY END

%post theme
%ifnarch %{armx} %{riscv}
%{_sbindir}/plymouth-set-default-theme %{vendor}

if test -f %{_sysconfdir}/default/grub ; then
    . %{_sysconfdir}/default/grub
    if [ "x\${GRUB_DISABLE_VENDOR_CONF}" = "x" ] || [ "x\${GRUB_DISABLE_VENDOR_CONF}" = "xfalse" ]; then
	sed -e '/GRUB_DISTRIBUTOR/d' -e '/GRUB_THEME/d' -e '/GRUB_BACKGROUND/d' -i %{_sysconfdir}/default/grub
	if [ "x\${GRUB_DISABLE_VENDOR_CONF}" = "x" ]; then
	    echo -e "\n" >> %{_sysconfdir}/default/grub
	    echo "GRUB_DISABLE_VENDOR_CONF=false" >> %{_sysconfdir}/default/grub
	fi
    fi
fi

update-alternatives --install %{_sysconfdir}/default/grub.vendor grub.vendor %{_sysconfdir}/default/grub.%{vendor} 10
%endif

%postun theme
%ifnarch %{armx} %{riscv}
if [ "$1" = "0" ]; then
    update-alternatives --remove grub.vendor %{_sysconfdir}/default/grub.%{vendor}
fi
%endif

%post indexhtml
# done to prevent excludedocs to ignore the doc/HTML
mkdir -p %{_datadir}/doc/HTML
sed -i -e "s/#PRODUCT_ID/$(cat /etc/product.id)/" -e "s/#LANG/${LC_NAME/[-_]*}/g" %{_datadir}/mdk/indexhtml/index.html ||:

%files common
%doc doc/CREDITS doc/distro.txt doc/release-notes.*
%{_sysconfdir}/redhat-release
%{_sysconfdir}/mandrake-release
%{_sysconfdir}/mandriva-release
%{_sysconfdir}/mandrakelinux-release
%{_sysconfdir}/system-release
%{_sysconfdir}/profile.d/10distro-release.sh
%{_sysconfdir}/profile.d/10distro-release.csh
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/system
%{_datadir}/common-licenses

%files desktop
%{_bindir}/*
%dir %{_sysconfdir}/xdg/menus
%config(noreplace) %{_sysconfdir}/xdg/menus/*.menu
%dir %{_datadir}/faces/
%{_datadir}/faces/default.png
%{_datadir}/faces/user-default-mdk.png
%dir %{_datadir}/mdk
%dir %{_datadir}/mdk/faces
%dir %{_datadir}/mdk/backgrounds
%{_datadir}/mdk/faces/*.png
%{_datadir}/applications/*.desktop
%dir %{_datadir}/wallpapers
%{_datadir}/wallpapers/mdk
%dir %{_datadir}/mdk/bookmarks
%dir %{_datadir}/mdk/bookmarks/konqueror
%{_datadir}/mdk/bookmarks/konqueror/*.html
%dir %{_datadir}/mdk/bookmarks/mozilla
%{_datadir}/mdk/bookmarks/mozilla/*.html
%{_iconsdir}/hicolor/scalable/apps/*.svg
%{_iconsdir}/openmandriva.svg

%if %{without bootstrap}
%files desktop-Plasma
%{_sysconfdir}/xdg/*
%{_datadir}/konsole/OM.profile
%{_datadir}/kservices5/plasma-layout-template-org.openmandriva.plasma.desktop.defaultPanel.desktop
%{_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.defaultPanel
%{_datadir}/plasma/shells/org.kde.plasma.desktop/contents/layout.js
%{_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.globalMenuPanel
%{_datadir}/plasma/look-and-feel/org.openmandriva5.desktop
%endif

%files theme
%{_datadir}/mdk/backgrounds/*.*g
%dir %{_datadir}/wallpapers/OpenMandriva
%{_datadir}/wallpapers/OpenMandriva/*
%{_datadir}/wallpapers/*.*g
%{_iconsdir}/hicolor/scalable/apps/openmandriva.svg
%{_iconsdir}/hicolor/*/apps/openmandriva.png
%dir %{_datadir}/mdk/screensaver
%{_datadir}/mdk/screensaver/*.jpg
%optional %{_datadir}/pixmaps/system-logo-white.png

%ifnarch %{armx} %{riscv}
%{_datadir}/plymouth/themes/%{vendor}
%{_sysconfdir}/default/grub.%{vendor}
%dir /boot/grub2/themes/%{vendor}
/boot/grub2/themes/%{vendor}/*
%{_sysconfdir}/grub.d/*
%endif

%files repos
%dir %{_sysconfdir}/yum.repos.d
%config(noreplace) %{_sysconfdir}/yum.repos.d/openmandriva*.repo

%files repos-keys
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-OpenMandriva

%files repos-pkgprefs

%files rpm-setup
# We should own this directory
%dir %{_rpmconfigdir}/openmandriva
%{_rpmconfigdir}/openmandriva/macros
%{_rpmconfigdir}/openmandriva/rpmrc

%files rpm-setup-build
%attr(755,root,root) %{_rpmconfigdir}/openmandriva/devel.prov
%attr(755,root,root) %{_rpmconfigdir}/openmandriva/kmod-deps.sh
%{_rpmluadir}/fedora/common.lua
%{_rpmluadir}/fedora/srpm/forge.lua
%{_rpmconfigdir}/macros.d/macros.forge
%{_rpmconfigdir}/macros.d/macros.dwz
%{_rpmconfigdir}/macros.d/macros.kernel
%{_rpmconfigdir}/macros.d/macros.perl
%{_rpmconfigdir}/macros.d/macros.python
%{_rpmconfigdir}/macros.d/macros.selinux
%{_rpmconfigdir}/fileattrs/devel.attr
%{_rpmconfigdir}/fileattrs/kmod.attr

%files installer
%{_sysconfdir}/calamares/*.conf
%{_sysconfdir}/calamares/modules/*.conf
%{_sysconfdir}/calamares/branding/auto/*

%files indexhtml
%dir %{_datadir}/mdk/about
%dir %{_datadir}/mdk/indexhtml
%dir %{_datadir}/mdk/mail
%{_datadir}/mdk/about/*
%{_datadir}/mdk/indexhtml/*
%{_datadir}/mdk/mail/*
%dir %{_datadir}/doc/HTML/
%{_datadir}/doc/HTML/index.html
%{_datadir}/applications/about-openmandriva-lx.desktop
%{_bindir}/about-openmandriva-lx

%files rpmlint-policy
%{_datadir}/rpmlint/config.d/*
