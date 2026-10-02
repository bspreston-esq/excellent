%global srcname triumphant

Name:           triumphant
Version:        0.1.0
Release:        1%{?dist}
Summary:        A most excellent Bill and Ted quote machine

License:        GPL-3.0-only
URL:            https://github.com/bspreston-esq/triumphant
Source0:        https://files.pythonhosted.org/packages/source/t/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  pyproject-rpm-macros

%description
A most excellent Bill and Ted quote machine, dudes! Prints righteous quotes
from Bill and Ted's Excellent Adventure. The installed 'triumphant' command
hands you a random quote, or a careful/bogus one with the right flag.
Party on!

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files triumphant

%files -f %{pyproject_files}
%license LICENSE
%{_bindir}/triumphant

%changelog
* Fri Oct 02 2026 bspreston-esq <bspreston-esq@users.noreply.github.com> - 0.1.0-1
- Initial package
