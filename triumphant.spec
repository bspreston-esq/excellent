%global srcname triumphant

Name:           triumphant
Version: 0.1.3
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

%package collections
Summary:        Additional quote collections for triumphant
Requires:       triumphant = %{version}-%{release}

%description collections
Extra quote collections for the triumphant command. Includes the Austin
Powers collection. Data files land in %{_localstatedir}/lib/triumphant and
are marked %config(noreplace), so your edits survive package upgrades.

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files triumphant
mkdir -p %{buildroot}%{_localstatedir}/lib/triumphant
cp -a %{buildroot}%{python3_sitelib}/triumphant/collections/default %{buildroot}%{_localstatedir}/lib/triumphant/default
cp -a %{buildroot}%{python3_sitelib}/triumphant/collections/austin-powers %{buildroot}%{_localstatedir}/lib/triumphant/austin-powers

%files -f %{pyproject_files}
%license LICENSE
%{_bindir}/triumphant
%dir %{_localstatedir}/lib/triumphant
%dir %{_localstatedir}/lib/triumphant/default
%config(noreplace) %{_localstatedir}/lib/triumphant/default/standard
%config(noreplace) %{_localstatedir}/lib/triumphant/default/careful
%config(noreplace) %{_localstatedir}/lib/triumphant/default/bogus
%config(noreplace) %{_localstatedir}/lib/triumphant/default/description

%files collections
%dir %{_localstatedir}/lib/triumphant/austin-powers
%config(noreplace) %{_localstatedir}/lib/triumphant/austin-powers/standard
%config(noreplace) %{_localstatedir}/lib/triumphant/austin-powers/careful
%config(noreplace) %{_localstatedir}/lib/triumphant/austin-powers/bogus
%config(noreplace) %{_localstatedir}/lib/triumphant/austin-powers/description

%changelog
* Fri Oct 02 2026 bspreston-esq <bspreston-esq@users.noreply.github.com> - 0.1.2-1
- Add quote collections: default and austin-powers (triumphant-collections)
- Data files installed under %{_localstatedir}/lib/triumphant with %config(noreplace)
* Fri Oct 02 2026 bspreston-esq <bspreston-esq@users.noreply.github.com> - 0.1.0-1
- Initial package
