%global         pkgname        OpenXR-SDK-Source
%global         libmajor 1

%define libname %mklibname %{name} %{libmajor}
%define devname %mklibname -d %{name}


Name:           openxr
Version:        1.1.36
Release:        1
Summary:        An API for writing VR and AR software
License:        ASL 2.0
URL:            https://github.com/KhronosGroup/%{pkgname}
Source:         https://github.com/KhronosGroup/OpenXR-SDK-Source/archive/refs/tags/release-%{version}/OpenXR-SDK-Source-release-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  glslang
BuildRequires:  glslang-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-glx)
BuildRequires:  pkgconfig(xcb-randr)
BuildRequires:  pkgconfig(xcb-dri2)
BuildRequires:  pkgconfig(xrandr) 
BuildRequires:  python3dist(jinja2)

Requires:       %{libname}%{?_isa} = %{version}-%{release}

%description
OpenXR is an API specification for writing portable, cross-platform,
virtual reality (VR) and augmented reality (AR) software.

%package -n %{libname}
Summary:        Libraries for writing VR and AR software

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with OpenXR.

%package -n %{devname}
Summary:        Headers and development files of the OpenXR library
Requires:       %{libname}%{?_isa} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for the OpenXR library. Install this package if you
want to compile applications using the OpenXR library.

%prep
%autosetup -n %{pkgname}-release-%{version}

%build
%cmake \
    -DBUILD_ALL_EXTENSIONS=ON \
    -DBUILD_LOADER=ON \
    -DBUILD_TESTS=ON \
    -DBUILD_WITH_STD_FILESYSTEM=OFF \
    -DBUILD_WITH_WAYLAND_HEADERS=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_FLAGS="%{optflags} -Wl,--as-needed" \
    -DCMAKE_CXX_FLAGS="%{optflags} -Wl,--as-needed" \
    -DCMAKE_CXX_STANDARD=17 \
    -DDYNAMIC_LOADER=ON
%make_build


%install
%make_install -C build

# We do not want static file .a
rm -fr %{buildroot}%{_libdir}/*.a

%files
%license LICENSE
# Include license in doc otherwise build complains
%doc CHANGELOG.SDK.md LICENSE README.md 
%{_bindir}/*
%{_datadir}/%{name}
%{_libdir}/lib*.so
%{_mandir}/man1/*.1*

%files -n %{libname}
%{_libdir}/lib%{name}_loader.so.%{libmajor}{,.*}

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%{_libdir}/pkgconfig/*.pc
