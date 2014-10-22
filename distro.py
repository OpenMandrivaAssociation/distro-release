import sys,rpm

def release_package(distribution, Vendor):
    vendor = Vendor.lower()
    print(rpm.expandMacro("""
%%package 	"""+Vendor+"""
Summary:	"""+Vendor+""" release file
Group:		System/Configuration/Other
Requires:	%{arch_tagged %{_vendor}-release-common}
Requires(post):	coreutils
Requires(post,postun): update-alternatives
Requires(pre):	distro-release-common
Requires(pre):	bash
Provides:	redhat-release rawhide-release mandrake-release
Provides:	mandrakelinux-release
Provides:	%{name} = %{version}-%{release}
Provides:	mandriva-release = %{version}-%{release}

%%description """+Vendor+"""
"""+distribution+""" release file for """+Vendor+""" flavor.

%%post		"""+Vendor+"""
update-alternatives --install /etc/os-release os-release /etc/os-release."""+vendor+""" 10
update-alternatives --install /etc/release release /etc/"""+vendor+"""-release 10
update-alternatives --install /etc/product.id product.id /etc/product.id."""+Vendor+""" 10
update-alternatives --install /etc/version version /etc/version."""+vendor+""" 10


%%postun	"""+Vendor+"""
if [ "$1" = "0" ]; then
update-alternatives --remove os-release /etc/os-release."""+vendor+"""
update-alternatives --remove release /etc/"""+vendor+"""-release
update-alternatives --remove product.id /etc/product.id."""+Vendor+"""
update-alternatives --remove version /etc/version."""+Vendor+"""
fi

%%files		"""+Vendor+"""
%{_sys_macros_dir}/"""+Vendor+""".macros
%{_sysconfdir}/os-release."""+vendor+"""
%{_sysconfdir}/"""+vendor+"""-release
%{_sysconfdir}/product.id."""+Vendor+"""
%{_sysconfdir}/version."""+vendor))
    sys.stdout.flush()

def release_install(distribution,product,Vendor,codename,disturl,disttag,ansiColor="1;43"):
    vendor = Vendor.lower()
    _distribution = distribution.lower().replace(" ","_").replace("/","_").replace("!","_").replace("?","_")

    print(rpm.expandMacro("""
cat > %{buildroot}%{_sysconfdir}/product.id."""+product+""" << EOF
vendor="""+Vendor+""",distribution="""+distribution+""",type=%{product_type},version=%{distepoch},branch=%{product_branch},release=%{product_release},arch=%{product_arch},product="""+product+"""
EOF

mkdir -p %{buildroot}%{_sys_macros_dir}
cat > %{buildroot}%{_sys_macros_dir}/"""+Vendor+""".macros << EOF
%%distro_release  %{distepoch}
%%distro_branch   %distro_branch
%%distro_arch     %distro_arch
%%distro_os       %distro_os
%%distro_class    %%(. %{_sysconfdir}/sysconfig/system; echo \\\$META_CLASS)
%%disver          %distro_ver

# (tpg) legacy stuff should be removed after all packages do not use macros begining with %%mandriva\
%%mandriva_release  %{distepoch}
%%mandriva_branch   %mandriva_branch
%%mandriva_arch     %mandriva_arch
%%mandriva_os       %mandriva_os
%%mandriva_class    %%(. %{_sysconfdir}/sysconfig/system; echo \\$META_CLASS)
%%mdkver            %mdkver
%%mdvver            %%mdkver

# productid variable
%%product_id vendor="""+vendor+",distribution="+distribution+",type=%product_type,version=%{distepoch},branch=%{product_branch},release=%{product_release},arch=%{product_arch},product="+product+"""

%%product_vendor        """+vendor+"""
%%product_distribution  """+distribution+"""
%%product_type          %product_type
%%product_version       %distepoch
%%product_branch        %product_branch
%%product_release       %product_release
%%product_arch          %product_arch
%%product_product       """+product+"""
%%distribution		"""+distribution+"""
 %%_distribution		"""+_distribution+"""
%%disturl		"""+disturl+"""
%%vendor		"""+Vendor+"""
 %%_vendor		"""+vendor+"""
%%disttag		"""+disttag+"""
EOF

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat > %{buildroot}%{_sysconfdir}/sysconfig/system << EOF
SECURITY=3
CLASS=beginner
LIBSAFE=no
META_CLASS=download
EOF

echo \""""+distribution+""" release %{distepoch} """+codename+""" for %{_target_cpu}" > %{buildroot}%{_sysconfdir}/"""+vendor+"""-release
if [ ! -f %{buildroot}%{_sysconfdir}/version"""+vendor+""" ]; then
echo \"%{distepoch} %{release} """+codename+"""\" > %{buildroot}%{_sysconfdir}/version."""+vendor+"""
fi

# (tpg) follow standard specifications http://0pointer.de/blog/projects/os-release
cat > %{buildroot}%{_sysconfdir}/os-release."""+vendor+""" << EOF
NAME=\""""+distribution+"""\"
VERSION=\"%{distepoch} """+codename+"""\"
ID=\""""+vendor+"""\"
VERSION_ID=\"%{distepoch}\"
BUILD_ID=\"%(echo `date +"%Y%m%d.%H"`)\"
PRETTY_NAME=\""""+distribution+""" %{distepoch} """+codename+"""\"
ANSI_COLOR=\""""+ansiColor+"""\"
CPE_NAME=\"cpe:/o:"""+vendor+":"+_distribution+""":%{distepoch}\"
HOME_URL=\""""+disturl+"""\"
BUG_REPORT_URL=\"%{bugurl}\"
EOF
"""))
