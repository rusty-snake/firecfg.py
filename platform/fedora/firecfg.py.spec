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
install -Dm0644 etc/zz-firecfg.py.sh $RPM_BUILD_ROOT/etc/profile.d/zz-firecfg.py.sh
install -Dm0755 etc/zz-firecfg.py.sh $RPM_BUILD_ROOT%_systemd_system_env_generator_dir/zz-firecfg.py.sh
install -Dm0755 etc/zz-firecfg.py.sh $RPM_BUILD_ROOT%_systemd_user_env_generator_dir/zz-firecfg.py.sh
# XXX: This overrireds an existsing files
install -Dm0644 -t $RPM_BUILD_ROOT/etc/firejail etc/firejail/*.{local,profile}
install -d -m 0755 $RPM_BUILD_ROOT/etc/firecfg.py
#Unimplemented: install -m 0644 etc/config $RPM_BUILD_ROOT/etc/firecfg.py/config
#Unimplemented: install -d -m 0755 $RPM_BUILD_ROOT/etc/firecfg.py/config.d
install -d -m 0755 $RPM_BUILD_ROOT/etc/firecfg.py/groups
install -m 0644 etc/groups/0-firecfg.config $RPM_BUILD_ROOT/etc/firecfg.py/groups/0-firecfg.config
install -m 0644 etc/groups/DBus $RPM_BUILD_ROOT/etc/firecfg.py/groups/DBus
rm -rf $RPM_BUILD_ROOT%{python3_sitelib}/firecfg.py-*.egg-info


%files
%license COPYING
%{_bindir}/firecfg.py
%{python3_sitelib}/firecfg
%{_sysconfdir}/firecfg.py
%{_sysconfdir}/firejail/disable-common.local
%{_sysconfdir}/firejail/org.gnome.Maps.profile
%{_sysconfdir}/profile.d/zz-firecfg.py.sh
%_systemd_system_env_generator_dir/zz-firecfg.py.sh
%_systemd_user_env_generator_dir/zz-firecfg.py.sh
