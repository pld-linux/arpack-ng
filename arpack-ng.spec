# TODO: MPI, iso_c_binding
#
# Conditional build:
%bcond_without	static_libs

Summary:	Subroutines for solving large scale eigenvalue problems
Summary(pl.UTF-8):	Rozwiązywanie zagadnienia własnego dla dużych macierzy
Name:		arpack-ng
Version:	3.9.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/opencollab/arpack-ng/tags
Source0:	https://github.com/opencollab/arpack-ng/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e28fdbe33ee44a16e2733c180ec2a2bd
URL:		https://github.com/opencollab/arpack-ng
BuildRequires:	blas-devel
BuildRequires:	cmake >= 3.0
BuildRequires:	gcc-g77
BuildRequires:	lapack-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
Provides:	arpack = %{version}-%{release}
Obsoletes:	arpack < 3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ARPACK software is capable of solving large scale symmetric,
nonsymmetric, and generalized eigenproblems from significant
application areas. The software is designed to compute a few (k)
eigenvalues with user specified features such as those of largest real
part or largest magnitude. Storage requirements are on the order of
n*k locations. No auxiliary storage is required. A set of Schur basis
vectors for the desired k-dimensional eigen-space is computed which is
numerically orthogonal to working precision. Numerically accurate
eigenvectors are available on request.

%description -l pl.UTF-8
Rozwiązywanie zagadnienia własnego (symetrycznego, niesymetrycznego,
ogólnego) dla dużych macierzy. Macierz może być dowolna, przy czym
procedury działają szczególnie dobrze w przypadku dużych macierzy
rzadkich bądź macierzy ze znaną strukturą. Biblioteka służy do
obliczenia kilku (k) wartości własnych o zadanych z góry własnościach,
takich jak największa (najmniejsza) część rzeczywista albo największy
(najmniejszy) moduł. Wymagania pamięciowe są rzędu n*k, żadna
dodatkowa pamięć (np. dyskowa) nie jest wymagana.

%package devel
Summary:	ARPACK development files
Summary(pl.UTF-8):	Pliki programistyczne ARPACK
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	blas-devel
Requires:	lapack-devel
Provides:	arpack-devel = %{version}-%{release}
Obsoletes:	arpack-devel < 3

%description devel
ARPACK development files.

%description devel -l pl.UTF-8
Pliki programistyczne ARPACK.

%package static
Summary:	Static ARPACK library
Summary(pl.UTF-8):	Statyczna biblioteka ARPACK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	arpack-static = %{version}-%{release}
Obsoletes:	arpack-static < 3

%description static
Static ARPACK library.

%description static -l pl.UTF-8
Statyczna biblioteka ARPACK.

%prep
%setup -q

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DICB=ON
%{__make}
cd ..
%endif
install -d build
cd build
%cmake .. \
	-DICB=ON
%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# not installed by cmake
cp -p build/{arpackSolver,parpack}.pc $RPM_BUILD_ROOT%{_pkgconfigdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES COPYING PARPACK_CHANGES README.md TODO
%attr(755,root,root) %{_libdir}/libarpack.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libarpack.so.2

%files devel
%defattr(644,root,root,755)
%doc DOCUMENTS/*.doc
%attr(755,root,root) %{_libdir}/libarpack.so
%{_includedir}/arpack-ng
%{_pkgconfigdir}/arpack.pc
%{_pkgconfigdir}/arpackSolver.pc
%{_pkgconfigdir}/parpack.pc
%{_libdir}/cmake/arpackng

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libarpack.a
%endif
