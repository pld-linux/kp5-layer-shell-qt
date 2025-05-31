#
# Conditional build:
%bcond_with	tests		# unit tests

%define		kp_ver		5.27.12
%define		qt_ver		5.15.2
%define		kf_ver		5.102.0
%define		kpname		layer-shell-qt
Summary:	LayerShellQt - component to easily use clients based on wlr-layer-shell
Summary(pl.UTF-8):	LayerShellQt - komponent pozwalający łatwo używać klientów opartych na wlr-layer-shell
Name:		kp5-%{kpname}
Version:	5.27.12
Release:	1
License:	LGPL v3+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kp_ver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	40e1124956912a0fd6ad2757ac6032e4
URL:		https://kde.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	Qt5Qml-devel >= %{qt_ver}
BuildRequires:	Qt5WaylandClient-devel >= %{qt_ver}
BuildRequires:	Qt5XkbCommonSupport-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf5-extra-cmake-files >= %{kf_ver}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	wayland-devel >= 1.3
BuildRequires:	wayland-protocols
BuildRequires:	xorg-lib-libxkbcommon-devel
BuildRequires:	xz
Requires:	Qt5Core >= %{qt_ver}
Requires:	Qt5Gui >= %{qt_ver}
Requires:	Qt5WaylandClient >= %{qt_ver}
Requires:	wayland >= 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LayerShellQt component is meant for applications to be able to easily
use clients based on wlr-layer-shell.

%description -l pl.UTF-8
Celem komponentu LayerShellQt jest umożliwienie aplikacjom łatwego
używania klientów opartych na wlr-layer-shell.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qt_ver}
Requires:	Qt5Gui-devel >= %{qt_ver}

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libLayerShellQtInterface.so.*.*.*
%ghost %{_libdir}/libLayerShellQtInterface.so.5
%attr(755,root,root) %{_libdir}/qt5/plugins/wayland-shell-integration/liblayer-shell.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libLayerShellQtInterface.so
%{_includedir}/LayerShellQt
%{_libdir}/cmake/LayerShellQt
