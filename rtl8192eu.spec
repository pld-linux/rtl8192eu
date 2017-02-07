# TODO
# - add (switch?) https://github.com/Mange/rtl8192eu-linux-driver sources

# Conditional build:
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		pname	rtl8192eu
%define		rel		0.1
Summary:	rtl8192eu Linux Drivers
Name:		%{pname}
Version:	4.3.1.1
Release:	%{rel}
License:	GPL
Group:		Base/Kernel
Source0:	ftp://files.dlink.com.au/products/DWA-131/REV_E/Drivers/DWA-131_Linux_driver_v%{version}.zip
# Source0-md5:	3a344df88a21b0f1b971ff485c09da9e
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The official drivers for D-Link DWA-131 Rev E, with patches to keep it
working on newer kernels. Also works on Rosewill RNX-N180UBE v2 N300
Wireless Adapter.

%package -n kernel%{_alt_kernel}-net-rtl8192eu
Summary:	Linux driver for rtl8192eu
Summary(pl.UTF-8):	Sterownik dla Linuksa do rtl8192eu
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-net-rtl8192eu
The official drivers for D-Link DWA-131 Rev E, with patches to keep it
working on newer kernels. Also works on Rosewill RNX-N180UBE v2 N300
Wireless Adapter.

%prep
%setup -qc -n %{pname}-%{version}
install -d drv
tar -C drv -xf 20140812_rtl8192EU_linux_v%{version}_11320.tar.gz
mv drv/*/* .

%build
%build_kernel_modules -m 8192eu

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m 8192eu -d kernel/drivers/net/wireless

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-rtl8192eu
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-rtl8192eu
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-net-rtl8192eu
%defattr(644,root,root,755)
%doc *.pdf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*ko*
