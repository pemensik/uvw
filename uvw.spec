%global forgeurl0 https://github.com/skypjack/uvw
%global libuv_ver 1.41
%global tag0 v%{version}_libuv_v%{libuv_ver}
%global distprefix %{nil}

%undefine __cmake_in_source_build
%global debug_package %{nil}

Name:           uvw
Version:        2.9.0
%forgemeta
Release:        %autorelease
Summary:        Header-only easy to use libuv C++ wrapper

License:        MIT
URL:            https://github.com/skypjack/uvw
Source0:        %forgesource

Patch1:         uvw-2.9-test-libuv-dynamic.patch

BuildRequires:  gcc-c++, cmake
BuildRequires:  libuv-devel >= %{libuv_ver}
BuildRequires:  libcxx-devel
BuildRequires:  doxygen
BuildRequires:  gtest-devel
BuildRequires:  sed

%description
Not used.

%package        devel
Summary:        %{summary}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkg-config
Requires:       libuv-devel >= %{libuv_ver}
Provides:       %{name}-static
Suggests:       %{name}-doc

%description    devel
uvw started as a header-only, event based, tiny and easy to use
wrapper for libuv written in modern C++.
Now it's finally available also as a compilable static library.

The basic idea is to hide completely the C-ish interface of libuv behind a graceful C++ API.
Currently, no uv_*_t data structure is actually exposed by the library.
Note that uvw stays true to the API of libuv and it doesn't add anything
to its interface. For the same reasons, users of the library must follow
the same rules which are used with libuv.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        %{summary} API documentation
BuildArch:      noarch

%description    doc
uvw started as a header-only, event based, tiny and easy to use
wrapper for libuv written in modern C++.

The %{name}-doc package contains API documentation in HTML format.

%prep
%forgeautosetup -p1

echo "%{_docdir}"
sed -e 's,DESTINATION share/${PROJECT_NAME},DESTINATION share/doc/${PROJECT_NAME},' \
    -i docs/CMakeLists.txt
# Make uvw semi-dynamic. libuv should be linked dynamic, uvw static way.
echo 'Requires: libuv' >> libuvw-static.pc.in

%build
%cmake -DFETCH_LIBUV=OFF -DBUILD_TESTING=ON -DBUILD_DOCS=ON -DFIND_GTEST_PACKAGE=ON
%cmake_build


%install
%cmake_install


%check
%ctest


%{?ldconfig_scriptlets}


%files devel
%license LICENSE
%doc README.md
%{_includedir}/%{name}*
%{_libdir}/pkgconfig/libuvw*

%files doc
%license LICENSE
%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/html


%changelog
%autochangelog
