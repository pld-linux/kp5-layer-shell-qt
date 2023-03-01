#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	5.27.2
%define		qtver		5.15.2
%define		kf5ver		5.82.0
%define		kpname		layer-shell-qt
Summary:	layer-shell-qt
Name:		kp5-%{kpname}
Version:	5.27.2
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	deaf8f0c7b47020f3e53135f66831c28
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Qml-devel >= %{qtver}
BuildRequires:	Qt5Quick-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5WaylandClient-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5X11Extras-devel >= %{qtver}
BuildRequires:	Qt5XkbCommonSupport-devel >= %{qtver}
BuildRequires:	cmake >= 2.8.12
BuildRequires:	gettext-devel
BuildRequires:	kf5-kcmutils-devel >= %{kf5ver}
BuildRequires:	kf5-kcrash-devel >= %{kf5ver}
BuildRequires:	kf5-kdeclarative-devel >= %{kf5ver}
BuildRequires:	kf5-kdelibs4support-devel >= %{kf5ver}
BuildRequires:	kf5-kglobalaccel-devel >= %{kf5ver}
BuildRequires:	kf5-kidletime-devel >= %{kf5ver}
BuildRequires:	kf5-kwayland-devel
BuildRequires:	kf5-plasma-framework-devel >= %{kf5ver}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	wayland-protocols
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
kscreenlocker

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	../
%ninja_build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%ghost %{_libdir}/libLayerShellQtInterface.so.5
%attr(755,root,root) %{_libdir}/libLayerShellQtInterface.so.*.*.*
%attr(755,root,root) %{_libdir}/qt5/plugins/wayland-shell-integration/liblayer-shell.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/LayerShellQt
%{_libdir}/cmake/LayerShellQt
%{_libdir}/libLayerShellQtInterface.so
