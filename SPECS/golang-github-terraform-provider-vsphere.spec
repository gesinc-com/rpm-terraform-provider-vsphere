%global	owner	terraform-providers
%global	repo	terraform-provider-vsphere
%global	host	github.com
%global	archive	v%{version}.tar.gz
%global	dir	%{repo}-%{version}
%global	namespace github.com/%{owner}/%{repo}

%global	version	1.14.0
%global	release	0.1

# emulate mock bubblewrap dependency; delete with proper source
%if %{?rhel:0}%{!?rhel:1}
%global rhel	%(rpm -qf --qf "%{version}" /etc/issue)
%endif
%if %{?dist:0}%{!?dist:1}
%global dist	el%{?rhel}%{!?rhel:0}
%endif

# Actually, don't strip at all since we are not even building debug packages
%define	__strip /bin/true
%global	debug_package	%{nil}

Name:		golang-github-%{repo}
Summary:	Terraform provider for vSphere

Version:	%{version}
Release:	%{release}
Epoch:		0

Group:		Applications/System
License:	MPL2; info@terraform.io

%global	url	https://%{host}/%{owner}/%{repo}
URL:		%{url}
Source0:	%{url}/archive/%{archive}

BuildRequires:	%{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang} make
Requires:	terraform
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
Terraform provider for vSphere


%prep
%setup -q -n %{dir}

%build
export GOPATH=$PWD
export GOOS=linux
export GOARCH=amd64
mkdir -p src/%{namespace}/

shopt -s extglob dotglob
mv !(src) src/%{namespace}/
shopt -u extglob dotglob
pushd src/%{namespace}/
#go get %{namespace}/something
#go get github.com/Sirupsen/logrus

make build
popd


%install
[ "%{buildroot}" = "/" ] || [ ! -d %{buildroot} ] || rm -rf %{buildroot}
install -d -m 755 %{buildroot}
install -d -m 755 %{buildroot}%{_bindir}

# install binary
%{__install} \
	bin/%{repo} \
	%{buildroot}%{_bindir}/


%clean
[ "%{buildroot}" = "/" ] || [ ! -d %{buildroot} ] || rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
#doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/*


# %(date +"%a %b %d %Y") $Author: build $ %{version}-%{release}
%changelog
* Thu Jan 16 2020 bishopolis@gmail.com 1.14.0-0.1
- Initial

