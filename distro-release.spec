# Please update release notes:
# make -C SOURCES release-notes.{html,txt}
#

%define new_distribution OpenMandriva Lx
%define new_vendor OpenMandriva
%define new_product OpenMandriva Lx
# (tpg) use codename from here https://wiki.openmandriva.org/en/Codename
%define new_codename Argon
%define vendor_tag %(echo %{new_vendor} |tr A-Z a-z)
%define distribution_tag %(echo %{new_distribution} |tr A-Z a-z |sed -e 's,[ /!?],_,g')
%define product_tag %(echo %{new_product} |tr A-Z a-z |sed -e 's,[ /!?],_,g')
%define shorttag omv
%define new_disturl http://openmandriva.org/
%define new_bugurl http://issues.openmandriva.org/

%define am_i_cooker 1
%define am_i_rolling 0
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

%define major %(printf %u 0%(echo %{version}|cut -d. -f1))
%define minor %(printf %u 0%(echo %{version}|cut -d. -f2))
%define subminor %(printf %u 0%(echo %{version}|cut -d. -f3))
%define distro_tag %(echo $((%{major}*1000+%{minor})))
%define version_tag %(echo $((%{major}*1000000+%{minor}*1000+%{subminor})))
%define mdkver %{version_tag}

# Temporary...
%{!?_rpmmacrodir: %define _rpmmacrodir %{_prefix}/lib/rpm/macros.d}

Summary:	%{new_distribution} release file
Name:		distro-release
Version:	4.2
# (tpg) something needs to be done to make comparision 3.0 > 2015.0 came true
# 3001 = 3.1
# 3001 = 3.2 etc.
DistTag:	%{shorttag}%{distro_tag}
%if 0%am_i_cooker
Release:	0.4
%else
%if 0%am_i_rolling
Release:	0.1
%else
Release:	1
%endif
%endif
License:	GPLv2+
URL:		%{new_disturl}
Group:		System/Configuration/Other

%description
%{distribution} release file.

%package common
Summary:	%{new_distribution} release common files
Group:		System/Configuration/Other
%rename		rosa-release-common
%rename		mandriva-release-common
%rename		opemandriva-release-common
%rename		moondrake-release-common
%rename		mandriva-release
%rename		mandriva-release-Free
%rename		mandriva-release-One
%rename		mandriva-release-Powerpack
%rename		mandriva-release-Mini
# (tpg) older releases provides %{_sysconfdir}/os-release
Conflicts:	systemd < 37-5
Requires:	lsb-release
Requires:	setup
Requires:	filesystem
# cf mdvbz#32631
Provides:	arch(%{_target_cpu})
Provides:	%{arch_tagged distro-release-common}
# (tpg) remove after rpm5 to rpmv4 migration
%ifnarch x86_64
BuildRequires:	spec-helper
Requires:	spec-helper
%endif
# (tpg) get rid of it
%rename distro-release-Moondrake

%description common
Common files for %{new_distribution} release packages.

# build release flavour rpm
%package %{new_vendor}
Summary:	%{new_vendor} release file
Group:		System/Configuration/Other
Requires:	%{name}-common = %{EVRD}
Requires:	%{arch_tagged distro-release-common}
Requires:	%{name}-common >= %{version}
Provides:	mandriva-release = %{EVRD}
Provides:	distro-release = %{EVRD}
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
%{_sysconfdir}/release
%{_sysconfdir}/product.id
%{_sysconfdir}/version

# desktop-common-data
%package desktop
Summary:	Desktop common files
Group:		System/Configuration/Other
Epoch:		2
BuildArch:	noarch
#XDG stuff
Requires:	libxdg-basedir
Requires:	xdg-compliance
Requires:	xdg-user-dirs
Requires:	xdg-utils
Requires:	run-parts
Requires(post):	hicolor-icon-theme
Requires:	hicolor-icon-theme
Conflicts:	kdelibs-common < 30000000:3.5.2
Conflicts:	kdebase-kdm-config-file < 1:3.2-62mdk
Requires(post):	etcskel
Requires(post):	run-parts
Requires:	shared-mime-info
Obsoletes:	menu-messages
Obsoletes:	desktop-common-data < 1:4.2-4
%rename		mandrake_desk
%rename		menu
%rename		menu-xdg
%rename		faces-openmandriva
%rename		faces-icons
%rename		desktop-common-data

%description desktop
This package contains useful icons, menu structure and others goodies for the
%{distribution} desktop.

%package desktop-Plasma
Summary:	Plasma desktop configuration
Group:		Graphical desktop/KDE
BuildRequires:	cmake(ECM)
Requires:	distro-theme >= 1.4.41-4
Requires:	breeze
Requires:	breeze-gtk
Requires:	breeze-icons
Requires:	noto-sans-fonts
Provides:	kde4-config-file
Provides:	distro-kde4-config-OpenMandriva = 2015.0
Provides:	distro-kde4-config-OpenMandriva-common = 2015.0
Obsoletes:	distro-kde4-config-OpenMandriva < 2015.0
Obsoletes:	distro-kde4-config-OpenMandriva-common < 2015.0
Provides:	mandriva-kde4-config = 2014.0
Obsoletes:	mandriva-kde4-config < 2014.0
Provides:	distro-kde4-config-common = 2015.0
Obsoletes:	distro-kde4-config-common < 2015.0
BuildArch:	noarch


%description desktop-Plasma
KDE Plasma desktop configuration.

#package desktop-Xfce
#description desktop-Xfce

%if 0
%package theme
%description theme

%package repos
%description repos

%package repos-keys
%description repos-keys

%package repos-pkgprefs
%description repos-pkgprefs

%package rpm-setup
%description rpm-setup

%package rpm-setup-build
%description rpm-setup-build
%endif

%prep
cp -a %{_topdir}/doc/CREDITS CREDITS
cp -a %{_topdir}/doc/distro.txt distro.txt
cp -a %{_topdir}/doc/release-notes.txt release-notes.txt
cp -a %{_topdir}/doc/release-notes.html release-notes.html

# check that CREDITS file is in UTF-8, fail otherwise
if iconv -f utf-8 -t utf-8 < CREDITS > /dev/null
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
ln -sf release %{buildroot}%{_sysconfdir}/rosa-release
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
cat > %{buildroot}%{_sysconfdir}/sysconfig/system <<EOF
SECURITY=3
CLASS=beginner
LIBSAFE=no
META_CLASS=download
EOF

cat >%{buildroot}%{_sysconfdir}/%{vendor_tag}-release <<EOF
%{new_distribution} release %{version} (%{new_codename}) for %{_target_cpu}
EOF
cat >%{buildroot}%{_sysconfdir}/version.%{vendor_tag} <<EOF
%{version} %{release} (%{new_codename})
EOF

# (tpg) follow standard specifications http://www.freedesktop.org/software/systemd/man/os-release.html
cat >%{buildroot}%{_sysconfdir}/os-release.%{vendor_tag} <<EOF
NAME="%{new_distribution}"
VERSION="%{version} (%{new_codename})"
ID="%{vendor_tag}"
VERSION_ID="%{version}"
BUILD_ID="%(echo `date +"%Y%m%d.%H"`)"
PRETTY_NAME="%{new_distribution} %{version} (%{new_codename})"
VERSION_CODENAME="(%{new_codename})"
ANSI_COLOR="1;43"
CPE_NAME="cpe:/o:%{vendor_tag}:%{distribution_tag}:%{version}"
HOME_URL="%{new_disturl}"
BUG_REPORT_URL="%{new_bugurl}"
SUPPORT_URL="https://forum.openmandriva.org"
PRIVACY_POLICY_URL="https://www.openmandriva.org/tos"
EOF

ln -s os-release.%{vendor_tag} %{buildroot}%{_sysconfdir}/os-release
ln -s %{vendor_tag}-release %{buildroot}%{_sysconfdir}/release
ln -s product.id.%{new_vendor} %{buildroot}%{_sysconfdir}/product.id
ln -s version.%{vendor_tag} %{buildroot}%{_sysconfdir}/version

### DESKTOP ###
## Install backgrounds
# User & root's backgrounds
install -d -m 0755 %{buildroot}%{_datadir}/mdk/backgrounds/

# for easy access for users looking for wallpapers at expected location
install -d %{buildroot}%{_datadir}/wallpapers
ln -sr %{buildroot}%{_datadir}/mdk/backgrounds %{buildroot}%{_datadir}/wallpapers/mdk

## Install scripts
install -d -m 0755 %{buildroot}/%{_bindir}/
install -m 0755 %{_topdir}/desktops/bin/editor %{buildroot}/%{_bindir}/
install -m 0755 %{_topdir}/desktops/bin/www-browser %{buildroot}/%{_bindir}/
install -m 0755 %{_topdir}/desktops/bin/xvt %{buildroot}/%{_bindir}/

## Install faces
install -d -m 0755 %{buildroot}/%{_datadir}/mdk/faces/
install -d -m 0755 %{buildroot}/%{_datadir}/faces/
cp -a %{_topdir}/desktops/faces/*.png %{buildroot}/%{_datadir}/mdk/faces/

# David - 9.0-5mdk - For KDE
ln -s %{_datadir}/mdk/faces/default.png %{buildroot}%{_datadir}/faces/default.png

# David - 9.0-5mdk - For GDM
ln -s %{_datadir}/mdk/faces/default.png %{buildroot}%{_datadir}/faces/user-default-mdk.png

# (tpg) default desktop files (do not place them in /etc/skel/Desktop !)
install -d -m 0755 %{buildroot}%{_datadir}/applications
install -m 0644 %{_topdir}/desktops/applications/*.desktop %{buildroot}%{_datadir}/applications

# icons
install -d -m 0755 %{buildroot}%{_iconsdir}/hicolor/scalable/apps
cp -a %{_topdir}/theme/icons/*.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/

#install theme for GDM/KDM
install -d -m 0755 %{buildroot}/%{_datadir}/mdk/dm
for i in %{_topdir}/desktops/dm/*.png %{_topdir}/desktops/dm/*.desktop %{_topdir}/desktops/dm/*.xml ; do
  install -m 0644 $i %{buildroot}/%{_datadir}/mdk/dm/
done

# install bookmarks
install -d -m 0755 %{buildroot}%{_datadir}/mdk/bookmarks/konqueror
for i in %{_topdir}/desktops/bookmarks/konqueror/*.html ; do
  install -m 0644 $i %{buildroot}%{_datadir}/mdk/bookmarks/konqueror
done

install -d -m 0755 %{buildroot}%{_datadir}/mdk/bookmarks/mozilla
for i in %{_topdir}/desktops/bookmarks/mozilla/*.html ; do
    install -m 0644 $i %{buildroot}%{_datadir}/mdk/bookmarks/mozilla
done

mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus
ln -s ../kde5/menus/kde-applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/applications.menu
ln -s ../kde5/menus/kde-applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/kde-applications.menu
ln -s ../kde5/menus/kde-applications.menu %{buildroot}%{_sysconfdir}/xdg/menus/gnome-applications.menu
### DESKTOP END ###


### DESKTOP PLASMA ###

mkdir -p %{buildroot}%{_kde5_sysconfdir}/xdg
mkdir -p %{buildroot}%{_kde5_sysconfdir}/xdg/KDE
mkdir -p %{buildroot}%{_kde5_sysconfdir}/xdg/QtProject
mkdir -p %{buildroot}%{_kde5_sysconfdir}/xdg/plasma-workspace/env
mkdir -p %{buildroot}%{_kde5_sysconfdir}/xdg/plasma-workspace/shutdown
mkdir -p %{buildroot}%{_kde5_datadir}/kservices5
mkdir -p %{buildroot}%{_kde5_datadir}/plasma/shells/org.kde.plasma.desktop/contents
mkdir -p %{buildroot}%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.defaultPanel/contents
mkdir -p %{buildroot}%{_datadir}/konsole

for i in kcmdisplayrc kcmfonts kcminputrc kdeglobals kscreenlockerrc ksplashrc kwinrc plasmarc startupconfig startupconfigfiles kcm-about-distrorc ksmserverrc kiorc dolphinrc konsolerc klaunchrc discoverabstractnotifier.notifyrc plasma_workspace.notifyrc powermanagementprofilesrc; do
    install -m 0644 %{_topdir}/desktops/Plasma/$i %{buildroot}%{_kde5_sysconfdir}/xdg/$i
done

install -m 0644 %{_topdir}/desktops/Plasma/metadata.desktop %{buildroot}%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.defaultPanel/metadata.desktop
install -m 0644 %{_topdir}/desktops/Plasma/metadata.desktop %{buildroot}%{_kde5_datadir}/kservices5/plasma-layout-template-org.openmandriva.plasma.desktop.defaultPanel.desktop
install -m 0644 %{_topdir}/desktops/Plasma/org.kde.plasma.desktop-layout.js %{buildroot}%{_kde5_datadir}/plasma/shells/org.kde.plasma.desktop/contents/layout.js
install -m 0644 %{_topdir}/desktops/Plasma/org.openmandriva.plasma.desktop.defaultPanel-layout.js %{buildroot}%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.defaultPanel/contents/layout.js
install -m 0644 %{_topdir}/desktops/Plasma/plasma-firstsetup.sh %{buildroot}%{_kde5_sysconfdir}/xdg/plasma-workspace/env/plasma-firstsetup.sh
install -m 0644 %{_topdir}/desktops/Plasma/Sonnet.conf %{buildroot}%{_kde5_sysconfdir}/xdg/KDE/Sonnet.conf
install -m 0644 %{_topdir}/desktops/Plasma/kdeglobals.sh %{buildroot}%{_kde5_sysconfdir}/xdg/plasma-workspace/env/kdeglobals.sh
install -m 0644 %{_topdir}/desktops/Plasma/qtlogging.ini %{buildroot}%{_kde5_sysconfdir}/xdg/QtProject/qtlogging.ini
install -m 0644 %{_topdir}/desktops/Plasma/OMV.profile %{buildroot}%{_datadir}/konsole/OMV.profile
mkdir -p %{buildroot}%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.globalMenuPanel/contents
install -m 0644 %{_topdir}/desktops/Plasma/org.openmandriva.plasma.desktop.globalMenuPanel-layout.js %{buildroot}%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.globalMenuPanel/contents/layout.js
install -m 0644 %{_topdir}/desktops/Plasma/metadata-globalMenu.desktop %{buildroot}%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.globalMenuPanel/metadata.desktop

### DESKTOP PLASMA END ###

%check
%if %{am_i_cooker}
case %{release} in
0.*)
    ;;
*)
    printf '%s\n' "Cooker distro should have this package with release < %{mkrel 1}"
    exit 1
    ;;
esac
%endif

%files common
%doc CREDITS distro.txt release-notes.*
%{_sysconfdir}/redhat-release
%{_sysconfdir}/mandrake-release
%{_sysconfdir}/mandriva-release
%{_sysconfdir}/mandrakelinux-release
%{_sysconfdir}/rosa-release
%{_sysconfdir}/system-release
%{_sysconfdir}/profile.d/10distro-release.sh
%{_sysconfdir}/profile.d/10distro-release.csh
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/system

%files desktop
%{_bindir}/*
%dir %{_sysconfdir}/xdg
%dir %{_sysconfdir}/xdg/menus
%config(noreplace) %{_sysconfdir}/xdg/menus/*.menu
%dir %{_datadir}/faces/
%{_datadir}/faces/default.png
%{_datadir}/faces/user-default-mdk.png
%dir %{_datadir}/mdk/
%dir %{_datadir}/mdk/faces/
%{_datadir}/mdk/faces/*.png
%{_datadir}/applications/*.desktop
%dir %{_datadir}/mdk/backgrounds
%{_datadir}/wallpapers/mdk
%dir %{_datadir}/mdk/bookmarks
%dir %{_datadir}/mdk/bookmarks/konqueror
%{_datadir}/mdk/bookmarks/konqueror/*.html
%dir %{_datadir}/mdk/bookmarks/mozilla
%{_datadir}/mdk/bookmarks/mozilla/*.html
%{_datadir}/mdk/dm
%{_iconsdir}/hicolor/scalable/apps/*.svg

%files desktop-Plasma
%{_kde5_sysconfdir}/xdg/*
%{_datadir}/konsole/OMV.profile
%{_kde5_datadir}/kservices5/plasma-layout-template-org.openmandriva.plasma.desktop.defaultPanel.desktop
%{_kde5_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.defaultPanel
%{_kde5_datadir}/plasma/shells/org.kde.plasma.desktop/contents/layout.js
%{_datadir}/plasma/layout-templates/org.openmandriva.plasma.desktop.globalMenuPanel
