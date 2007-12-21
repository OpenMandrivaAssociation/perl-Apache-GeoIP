%define real_name Apache-GeoIP

Summary:	Apache::Geo::IP - Look up country by IP Address
Name:		perl-%{real_name}
Version:	1.63
Release:	%mkrel 1
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{real_name}
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/Apache/%{real_name}-%{version}.tar.bz2
BuildRequires:	perl-devel
BuildRequires:	apache-devel
BuildRequires:	apache-mod_perl
BuildRequires:	apache-mod_perl-devel
BuildRequires:	perl(Apache::Test) >= 1.25
#Requires:	apache-mod_perl
#Requires(pre,postun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%setup -q -n %{real_name}-%{version} 

%build

# this is to fool this stupid makefile...
mkdir -p %{buildroot}%{_datadir}/perl-%{real_name}
cp GeoIP.dat %{buildroot}%{_datadir}/perl-%{real_name}/

%{__perl} Makefile.PL INSTALLDIRS=vendor <<EOF
%{buildroot}%{_datadir}/perl-%{real_name}
n
y
EOF

%make

# requires network, and test suite rework
#make test

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/perl-%{real_name}
cp GeoIP.dat %{buildroot}%{_datadir}/perl-%{real_name}/

# remove the hack here...
find %{buildroot}%{perl_vendorlib} -type f -name "*.pm" | xargs perl -pi -e "s|%{buildroot}||g"

# fix apache config...
#install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
#
#cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{real_name}.conf << EOF
#PerlModule Apache::HelloIP 
#<Location /ip> 
#    SetHandler perl-script 
#    PerlHandler Apache::HelloIP 
#    PerlSetVar GeoIPDBFile "%{_datadir}/GeoIP/GeoIP.dat" 
#    PerlSetVar GeoIPFlag Standard 
#</Location>
#EOF

#%%post
#if [ -f %{_var}/lock/subsys/httpd ]; then
#    %{_initrddir}/httpd restart 1>&2;
#fi
#
#%%postun
#if [ "$1" = "0" ]; then
#    if [ -f %{_var}/lock/subsys/httpd ]; then
#        %{_initrddir}/httpd restart 1>&2
#    fi
#fi

%clean 
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changes README
#%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{real_name}.conf
%dir %{perl_vendorlib}/*/Apache2/Geo
%dir %{perl_vendorlib}/*/Apache2/Geo/IP
%{perl_vendorlib}/*/Apache2/GeoIP.pm
%{perl_vendorlib}/*/Apache2/Geo/IP.pm
%{perl_vendorlib}/*/Apache2/Geo/Mirror.pm
%{perl_vendorlib}/*/Apache2/Geo/IP/Record.pm
%{perl_vendorlib}/*/auto/Apache2/GeoIP/GeoIP.so
%dir %{_datadir}/perl-%{real_name}
%{_datadir}/perl-%{real_name}/GeoIP.dat
%{_mandir}/*/*



