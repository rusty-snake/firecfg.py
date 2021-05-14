Name:           firecfg.py
Version:        0.0.4
Release:        1%{?dist}
Summary:        An improved firecfg written in python

License:        GPLv3+
URL:            https://github.com/rusty-snake/firecfg.py
Source0:        firecfg.py-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
Requires:       python3
Enhances:       firejail

%description
An improved firecfg written in python


%prep
%autosetup


%build
%py3_build


%install
%py3_install


%post
firecfg.py setup


%preun
# https://docs.fedoraproject.org/hr/packaging-guidelines/Scriptlets/#_syntax
if [[ $1 -eq 0 ]]; then
	rm \
		/etc/profile.d/zz-firecfg.py.sh \
		/etc/systemd/system-environment-generators/zz-firecfg.py.sh \
		/etc/systemd/user-environment-generators/zz-firecfg.py.sh
fi


%files
%license AUTHORS COPYING
%{_bindir}/firecfg.py
%{python3_sitelib}/firecfgpy
%{python3_sitelib}/firecfg.py-*.egg-info
