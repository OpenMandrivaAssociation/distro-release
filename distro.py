import sys,rpm

def release_package(distribution):
    print(rpm.expandMacro("""
%%package 	"""+distribution+"""
Summary:	%{distribution} release file for """+distribution+"""
Group:		System/Configuration/Other
Requires:	%{arch_tagged %{_vendor}-release-common}
Requires(post):	coreutils
Provides:	redhat-release rawhide-release mandrake-release
Provides:	mandrakelinux-release
Provides:	%{name} = %{version}-%{release}
Provides:	mandriva-release = %{version}-%{release}

%%description """+distribution+"""
%{distribution} release file for """+distribution+""" flavor.

%%post		"""+distribution+"""
ln -fs product.id."""+distribution+""" %{_sysconfdir}/product.id

%%files		"""+distribution+"""
%{_sys_macros_dir}/"""+distribution+""".macros
%{_sysconfdir}/product.id."""+distribution))
    sys.stdout.flush()

def release_install(distribution,product,Vendor):
    vendor = Vendor.lower()
    print(rpm.expandMacro("""
cat > %{buildroot}%{_sysconfdir}/product.id."""+product+""" << EOF
%{product_id_base},product="""+product+"""
EOF

mkdir -p %{buildroot}%{_sys_macros_dir}
cat > %{buildroot}%{_sys_macros_dir}/"""+Vendor+""".macros << EOF
%%mandriva_release  %mandriva_release
%%mandriva_branch   %mandriva_branch
%%mandriva_arch     %mandriva_arch
%%mandriva_os       %mandriva_os
%%mandriva_class    %%(. %{_sysconfdir}/sysconfig/system; echo \\\$META_CLASS)
%%mdkver            %mdkver
%%mdvver            %%mdkver

# productid variable
%%product_id vendor="""+vendor+",distribution="+distribution+",type=%product_type,version=%product_version,branch=%product_branch,release=%product_release,arch=%product_arch,product="+Vendor+"""

%%product_vendor        """+vendor+"""
%%product_distribution  """+distribution+"""
%%product_type          %product_type
%%product_version       %product_version
%%product_branch        %product_branch
%%product_release       %product_release
%%product_arch          %product_arch
%%product_product       """+product+"""

EOF

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat > %{buildroot}%{_sysconfdir}/sysconfig/system << EOF
SECURITY=3
CLASS=beginner
LIBSAFE=no
META_CLASS=download
EOF"""))
