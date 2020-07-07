Name:           firecfg.py
Version:        0.0.3
Release:        1%{?dist}
Summary:        An improved firecfg written in python

License:        GPLv3+
URL:            https://github.com/rusty-snake/firecfg.py
Source0:        firecfg.py.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
Requires:       python3

%define py3_shbang_opts %{nil}

%description
An improved firecfg written in python


%prep
%autosetup -c


%build
%py3_build


%install
%py3_install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{python3_sitelib}/firecfg.py-*.egg-info


%files
%license COPYING
%{_bindir}/firecfg.py
%{python3_sitelib}/firecfg
%{_sysconfdir}/firecfg.py
%{_sysconfdir}/firejail/disable-common.local
%{_sysconfdir}/firejail/org.gnome.Maps.profile
%{_sysconfdir}/firejail/org.gnome.Weather.profile
%{_sysconfdir}/profile.d/zz-firecfg.py.sh
%_systemd_system_env_generator_dir/zz-firecfg.py.sh
%_systemd_user_env_generator_dir/zz-firecfg.py.sh
