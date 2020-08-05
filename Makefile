
install:
	install -Dm0644 etc/zz-firecfg.py.sh $(DESTDIR)/etc/profile.d/zz-firecfg.py.sh
	install -Dm0755 etc/zz-firecfg.py.sh $(DESTDIR)/usr/lib/systemd/system-environment-generators/zz-firecfg.py.sh
	install -Dm0755 etc/zz-firecfg.py.sh $(DESTDIR)/usr/lib/systemd/user-environment-generators/zz-firecfg.py.sh
	# XXX: This overrides existing files
	install -Dm0644 -t $(DESTDIR)/etc/firejail etc/firejail/*.{local,profile}
	install -d -m 0755 $(DESTDIR)/etc/firecfg.py
	#Unimplemented: install -m 0644 etc/config $(DESTDIR)/etc/firecfg.py/config
	#Unimplemented: install -d -m 0755 $(DESTDIR)/etc/firecfg.py/config.d
	install -d -m 0755 $(DESTDIR)/etc/firecfg.py/groups
	install -m 0644 etc/groups/0-firecfg.config $(DESTDIR)/etc/firecfg.py/groups/0-firecfg.config
	install -m 0644 etc/groups/DBus $(DESTDIR)/etc/firecfg.py/groups/DBus
