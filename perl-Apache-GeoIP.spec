%define upstream_name    Apache-GeoIP
%define upstream_version 1.99
Name:		perl-%{upstream_name}
Version:	1.99
Release:	1

Summary:	Apache::Geo::IP - Look up country by IP Address
License:	GPL+ or Artistic
Group:		Development/Perl
Url:		http://github.com/rkobes/apache-geoip/tree/master
Source0:	https://cpan.metacpan.org/authors/id/R/RK/RKOBES/Apache-GeoIP-1.99.tar.gz

BuildRequires:	make
BuildRequires:	apache-devel
BuildRequires:	apache-mod_perl
BuildRequires:	apache-mod_perl-devel
BuildRequires:	perl-devel
BuildRequires:	perl(Apache::Test) >= 1.25
BuildArch:	noarch

%description
This module constitutes a mod_perl (both versions 1 and 2) interface 
to the Geo::IP and Geo::Mirror modules. Geo::IP is used to look up in 
a database a country of origin of an IP address, while Geo::Mirror
is used to select a mirror by country from a specified list. See
the documentation for Apache::Geo::IP and Apache::Geo::Mirror
for more details.

The included tests require Apache::Test, which can be obtained
in the mod_perl-2 sources or in the httpd-test distribution.
These tests need a network connection to run; some may fail
due to timeouts upon doing certain name lookups.

The mod_perl-2 modules included here, with prefix Apache2::*,
will only work with mod_perl-1.999022 and above (RC5 or greater
of the CPAN distribution).

%prep
%setup -q -n %{upstream_name}-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor </dev/null
%make

%check
# requires network, and test suite rework
# make test

%install
%makeinstall_std

%files
%doc Changes README
%{perl_vendorlib}/Apache2
%{_mandir}/*/*

