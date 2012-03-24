# Please update release notes:
# make -C SOURCES release-notes.{html,txt}
#

%define am_i_cooker 1
%if %am_i_cooker
%define distrib Cooker
%else
%define distrib Official
%endif
%define version 2012.0
%define rel 0.4
%define distname cooker
%define distsuffix mdv
%define distribution Mandriva Linux

%define product_vendor Mandriva
%define product_distribution %distribution
%define product_type Basic
%define product_version %version
%if %am_i_cooker
%define product_branch Devel
%else
%define product_branch Official
%endif
%define product_release 1
%define product_arch %{_target_cpu}

%define product_id_base vendor=%product_vendor,distribution=%product_distribution,type=%product_type,version=%product_version,branch=%product_branch,release=%product_release,arch=%product_arch

%if %am_i_cooker
    %define unstable %%_with_unstable --with-unstable
%endif

# The mandriva release, what is written on box
%define mandriva_release %version

# The mandriva branch: Cooker, Community or Official
%define mandriva_branch %distrib

# The mandriva arch, notice: using %_target_cpu is bad
# elsewhere because this depend of the config of the packager
# _target_cpu => package build for
# mandriva_arch => the distribution we are using
%define mandriva_arch %_target_cpu

# To be coherent with %mandriva_arch I provide os too
# be I wonder it will be linux for a long time
%define mandriva_os %_target_os

%define realversion %version
%define mdkver %(echo %version | sed 's/\\.//')0

Summary:	Mandriva release file
Name:		mandriva-release
Version:	%version
Release:	%rel
Epoch:		1
License:	GPL
URL:		http://www.mandrivalinux.com/
Group:		System/Configuration/Other
Source:		%name.tar.bz2
Source3:	CREDITS
# edited lynx -dump of wiki:
Source4:	release-notes.txt
Source5:	release-notes.html
BuildRoot:	%{_tmppath}/%{name}-root

%description
Mandriva Linux release file.

%package common
Summary: Mandriva release common files
Group: System/Configuration/Other
Conflicts: %name < %version-%release
Obsoletes: mandriva-release-Discovery mandriva-release-Powerpack+
Obsoletes: %name < %version-%release
Obsoletes: rawhide-release redhat-release mandrake-release mandrakelinux-release

# cf mdvbz#32631
Provides: arch(%_target_cpu)
Provides: %arch_tagged mandriva-release-common

%description common
Common files for Mandriva Linux release packages.

%define release_package(s) \
%{-s:%package %1} \
Summary: Mandriva release file%{?1: for %1} \
Group: System/Configuration/Other \
Requires:	%{arch_tagged mandriva-release-common} \
Requires(post):	coreutils \
Provides:	redhat-release rawhide-release mandrake-release mandrakelinux-release \
Provides:	%name = %version-%release \

%define release_descr(s) \
%description %{-s:%1} \
Mandriva Linux release file for %1 flavor. \


%define release_post(s) \
%post %{-s:%1} \
ln -fs product.id.%1 /etc/product.id


%define release_install(s) \
cat > %buildroot/etc/product.id.%{1} << EOF \
%{product_id_base},product=%1\
EOF\
 \
mkdir -p %buildroot%_sys_macros_dir \
cat > %buildroot%_sys_macros_dir/%{1}.macros <<EOF \
%%distribution      %distribution\
%%mandriva_release  %mandriva_release\
%%mandriva_branch   %mandriva_branch\
%%mandriva_arch     %mandriva_arch\
%%mandriva_os       %mandriva_os\
%%mandriva_class    %%(. %_sysconfdir/sysconfig/system; echo \\\$META_CLASS)\
%%mdkver            %mdkver\
%%mdvver            %mdkver\
%%distsuffix        %distsuffix\
\
# productid variable\
%%product_id %{product_id_base},product=%{1}\
\
%%product_vendor        %product_vendor\
%%product_distribution  %product_distribution\
%%product_type          %product_type\
%%product_version       %product_version\
%%product_branch        %product_branch\
%%product_release       %product_release\
%%product_arch          %product_arch\
%%product_product       %1\
\
%{?unstable}\
EOF\
 \
mkdir -p %buildroot%_sysconfdir/sysconfig \
cat > %buildroot%_sysconfdir/sysconfig/system <<EOF \
SECURITY=3\
CLASS=beginner\
LIBSAFE=no\
META_CLASS=download\
EOF\


%release_package -s One
Conflicts: mandriva-release-Flash mandriva-release-Free mandriva-release-Powerpack mandriva-release-Mini
%release_package -s Flash
Conflicts: mandriva-release-Free mandriva-release-One mandriva-release-Powerpack mandriva-release-Mini
%release_package -s Free
Conflicts: mandriva-release-Flash mandriva-release-One mandriva-release-Powerpack mandriva-release-Mini
%release_package -s Powerpack
Conflicts: mandriva-release-Flash mandriva-release-Free mandriva-release-One mandriva-release-Mini
%release_package -s Mini
Conflicts: mandriva-release-Flash mandriva-release-Free mandriva-release-One mandriva-release-Powerpack

%release_descr -s Flash
%release_descr -s One
%release_descr -s Free
%release_descr -s Powerpack
%release_descr -s Mini

%triggerpostun -n mandriva-release-common -- mandriva-release < 2007.1
perl -pi -e "s/(META_CLASS=)server$/\\1powerpack/" %_sysconfdir/sysconfig/system

%triggerpostun -n mandriva-release-common -- mandriva-release-common < 2008.0-0.17
perl -pi -e "s/(META_CLASS=)server$/\\1powerpack/" %_sysconfdir/sysconfig/system

%prep
%setup -q -n %{name}
cp -a %SOURCE3 CREDITS
cp -a %SOURCE4 release-notes.txt
cp -a %SOURCE5 release-notes.html
cat > README.urpmi <<EOF
This is Mandriva Linux %version

You can find the release notes in %_docdir/%name-common/release-notes.txt

or on the web at http://wiki.mandriva.com/en/%{version}_Notes
EOF

# check that CREDITS file is in UTF-8, fail otherwise
if iconv -f utf-8 -t utf-8 < CREDITS > /dev/null
then
	true
else
	echo "the CREDITS file *MUST* be encoded in UTF-8"
	echo "please fix it before continuing"
	false
fi

%install
rm -rf %{buildroot}
mkdir -p %buildroot/etc
echo "Mandriva Linux release %{realversion} (%{distrib}) for %{_target_cpu}" > %{buildroot}/etc/mandriva-release
ln -sf mandriva-release %{buildroot}/etc/redhat-release
ln -sf mandriva-release %{buildroot}/etc/mandrake-release
ln -sf mandriva-release %{buildroot}/etc/release
ln -sf mandriva-release %{buildroot}/etc/mandrakelinux-release
ln -sf mandriva-release %{buildroot}/etc/os-release
echo "%{version}.0 %{rel} %{distname}" > %{buildroot}/etc/version

mkdir -p %buildroot%_sysconfdir/profile.d
cat > %buildroot%_sysconfdir/profile.d/10mandriva-release.csh<<'EOF'
if ( -r /etc/sysconfig/system ) then
	eval `sed 's|^#.*||' /etc/sysconfig/system | sed 's|\([^=]*\)=\([^=]*\)|set \1=\2|g' | sed 's|$|;|' `
	setenv META_CLASS $META_CLASS
else
	setenv META_CLASS unknown
endif
EOF

cat > %buildroot%_sysconfdir/profile.d/10mandriva-release.sh<<'EOF'
if [ -r /etc/sysconfig/system ]; then
	. /etc/sysconfig/system
	export META_CLASS
else
	export META_CLASS=unknown
fi
EOF

%release_install Free
%release_install Flash Flash
%release_install One One
%release_install Powerpack Powerpack
%release_install Mini Mini

touch %buildroot%_sysconfdir/product.id


%check
%if %am_i_cooker
case %release in
    0.*) ;;
    *)
    echo "Cooker distro should have this package with release < %{mkrel 1}"
    exit 1
    ;;
esac
%endif

%release_post -s Flash
%release_post -s Free
%release_post -s One 
%release_post -s Powerpack
%release_post -s Mini

%define release_files(s:) \
%files %{-s:%{-s*}} \
%defattr(-,root,root) \
%_sys_macros_dir/%{1}.macros \
/etc/product.id.%1 \
%ghost /etc/product.id\
\

%release_files -s Flash Flash
%release_files -s Free Free
%release_files -s One One
%release_files -s Powerpack Powerpack
%release_files -s Mini Mini


%files common
%doc CREDITS distro.txt README.urpmi release-notes.*
/etc/mandrake-release
/etc/mandrakelinux-release
/etc/redhat-release
/etc/mandriva-release
/etc/release
/etc/version
/etc/profile.d/10mandriva-release.sh
/etc/profile.d/10mandriva-release.csh
%config(noreplace) %verify(not md5 size mtime) %_sysconfdir/sysconfig/system



