Summary: Library providing the FAM File Alteration Monitor API
Name: gamin
Version: 0.1.10
Release: 9%{?dist}
License: LGPLv2
#some of the files (server/inotify-kernel.c) are GPLv2
#so https://fedoraproject.org/wiki/Licensing#GPL_Compatibility_Matrix
#says the whole is GPLv2
#License: GPLv2
Group: Development/Libraries
Source: http://ftp.gnome.org/pub/GNOME/sources/gamin/0.1/gamin-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-root
URL: http://www.gnome.org/~veillard/gamin/
Obsoletes: fam < 2.6.10-12
Provides: fam = 2.6.10-12
BuildRequires: glib2-devel python python-devel
BuildRequires: automake, libtool


# This fix addresses an issue with ARM, where the configuration triplet
# happens to be armv5tel-redhat-linux-gnueabi instead of armv5tel-redhat-linux-gnu.
# The patch declares HAVE_LINUX in case of linux-gnueabi as well.
# Patch by Kedar Sovani <kedars@marvell.com>
Patch1: gamin-0.1.10-gnueabi.patch


%description
This C library provides an API and ABI compatible file alteration
monitor mechanism compatible with FAM but not dependent on a system wide
daemon.

%package devel
Summary: Libraries, includes, etc. to embed the Gamin library
Group: Development/Libraries
Requires: gamin = %{version}-%{release}
Obsoletes: fam-devel < 2.6.10-12
Provides: fam-devel = 2.6.10-12

%description devel
This C library provides an API and ABI compatible file alteration
monitor mechanism compatible with FAM but not dependent on a system wide
daemon.

%package python
Summary: Python bindings for the gamin library
Group: Development/Libraries
Requires: gamin = %{version}-%{release}

%description python
The gamin-python package contains a module that allow monitoring of
files and directories from the Python language based on the support
of the gamin package.

%prep
%setup -q
%patch1 -p1 -b .gnueabi

# recode docs into UTF-8
for i in ChangeLog NEWS ; do 
   iconv -f iso-8859-1 -t utf-8 < $i > XXX
   touch -r $i XXX
   mv XXX $i
done

# https://fedoraproject.org/wiki/Features/SystemPythonExecutablesUseSystemPython
# replace "/usr/bin/env python" with a "/usr/bin/python"
for i in `find -name '*.py'`; do
   sed -i.bak 's|^#!/usr/bin/env python|#!/usr/bin/python|g' $i
   touch -r ${i}.bak $i
   rm ${i}.bak
done


%build
autoreconf --force --install
%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -fr %{buildroot}

make install DESTDIR=%{buildroot} INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f

%clean
rm -fr %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)

%doc AUTHORS ChangeLog NEWS README Copyright TODO COPYING
%doc doc/*.html
%doc doc/*.gif
%doc doc/*.txt
%{_libdir}/lib*.so.*
%{_libexecdir}/gam_server

%files devel
%defattr(-, root, root, -)

%{_libdir}/lib*.so
%{_includedir}/fam.h
%{_libdir}/pkgconfig/gamin.pc

%files python
%defattr(-, root, root, -)
%{_libdir}/python*/site-packages/gamin.py*
%{_libdir}/python*/site-packages/_gamin*
%doc python/tests/*.py
%doc doc/python.html

%changelog
* Wed Mar  3 2010 Tomas Bzatek <tbzatek@redhat.com> - 0.1.10-9
- Further cleanup for package review (#225776)

* Wed Jan  6 2010 Tomas Bzatek <tbzatek@redhat.com> - 0.1.10-8
- Fix source URL

* Mon Dec 21 2009 Tomas Bzatek <tbzatek@redhat.com> - 0.1.10-7
- Cleanup for package review (#225776)

* Mon Dec 14 2009 Tomas Bzatek <tbzatek@redhat.com> - 0.1.10-6
- Remove unneeded .a and .la files

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.1.10-5.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan  5 2009 Tomas Bzatek <tbzatek@redhat.com> - 0.1.10-3
- Fix build on gnueabi (patch by Kedar Sovani)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.10-2
- Rebuild for Python 2.6

* Mon Nov 24 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.1.10-1
- Update to 0.1.10
- Drop upstreamed patches

* Mon Jul 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.1.9-6
- fix license tag

* Wed Feb 14 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.1.9-5
- workaround for missing struct ucred in glibc headers (fixed x86_64 compilation)

* Fri Sep 14 2007 Matthias Clasen <mclasen@redhat.com> - 0.1.9-4
- Fix a memory leak

* Fri Sep 14 2007 Ray Strode <rstrode@redhat.com> - 0.1.9-3
- don't poll for non-existant watched files (bug 240385)

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.1.9-2
- Rebuild for selinux ppc32 issue.

* Fri Jul 27 2007 Daniel Veillard <veillard@redhat.com> - 0.1.9-1.fc8
- made new upstream release, that includes all the existing patches

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 0.1.8-6
- Don't ship static libraries

* Wed Apr 11 2007 Alexander Larsson <alexl@redhat.com> - 0.1.8-5
- Add patch that handles inotify failing fallback (#233316)

* Wed Mar  7 2007 Alexander Larsson <alexl@redhat.com> - 0.1.8-4
- Add patch to fix #204906

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.1.8-3
- rebuild for python 2.5

* Mon Nov 20 2006 Alexander Larsson <alexl@redhat.com> - 0.1.8-2.fc7
- Fix polling backend, making NFS work again
- Resolves: #212551

* Tue Oct 31 2006 Daniel Veillard <veillard@redhat.com> - 0.1.8-1
- made new upstream release, that should include all the existing patches

* Fri Sep  8 2006 Alexander Larsson <alexl@redhat.com> - 0.1.7-7
- Fix problems in new inotify backend (#205731)

* Tue Sep  5 2006 Alexander Larsson <alexl@redhat.com> - 0.1.7-6
- Remove last regular timers from gamin

* Tue Sep  5 2006 Alexander Larsson <alexl@redhat.com> - 0.1.7-5
- Use sigaction to reset old signal handler (from cvs)
- New inotify backend from cvs (based on gnome-vfs code)
- Only create timer on demand
- This should fix #204906

* Mon Aug 28 2006 Alexander Larsson <alexl@redhat.com> - 0.1.7-4
- Flush in-buffer on connection reset (#196444)
- Patch from Ariel T. Glenn

* Tue Aug 22 2006 Alexander Larsson <alexl@redhat.com> - 0.1.7-3
- Use /dev/null as stdin/out/err when spawning gam_server
- This could help if there is stdout output somewhere.

* Wed Aug 16 2006 Alexander Larsson <alexl@redhat.com> - 0.1.7-2
- Add patch that avoids closing the fd after FAMOpen, fixes some 100% cpu bugs

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.1.7-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.1.7-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.1.7-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Oct 27 2005 Daniel Veillard <veillard@redhat.com> 0.1.7-1
- hopefully fixes gam_server crashes
- some portability fixes
- removed a minor leak
* Thu Sep  8 2005 Daniel Veillard <veillard@redhat.com> 0.1.6-1
- revamp of the inotify back-end
- memory leak fix
- various fixes and cleanups
* Tue Aug  9 2005 Daniel Veillard <veillard@redhat.com> 0.1.5-1
- Improvement of configuration, system wide configuration files and
  per filesystem type default
- Rewrite of the inotify back-end, reduce resources usage, tuning in
  case of busy resources
- Documentation updates
- Changes to compile inotify back-end on various architectures
- Debugging output improvements
* Tue Aug  2 2005 Daniel Veillard <veillard@redhat.com> 0.1.3-1
- Fix to compile on older gcc versions
- Inotify back-end changes and optimizations
- Debug ouput cleanup, pid and process name reports
- Dropped kernel monitor bugfix
- Removed the old glist copy used for debugging
- Maintain mounted filesystems knowledge, and per fstype preferences
* Wed Jul 13 2005 Daniel Veillard <veillard@redhat.com> 0.1.2-1
- inotify back end patches, ready for the new inotify support in kernel
- lot of server code cleanup patches
- fixed an authentication problem
* Fri Jun 10 2005 Daniel Veillard <veillard@redhat.com> 0.1.1-1
- gamin_data_conn_event fix
- crash from bug gnome #303932
- Inotify and mounted media #171201
- mounted media did not show up on Desktop #159748
- write may not be atomic
- Monitoring a directory when it is a file
- Portability to Hurd/Mach and various code cleanups
- Added support for ~ as user home alias in .gaminrc
* Thu May 12 2005 Daniel Veillard <veillard@redhat.com> 0.1.0-1
- Close inherited file descriptors on exec of gam_server
- Cancelling a monitor send back a FAMAcknowledge
- Fixed for big files > 2GB
- Bug when monitoring a non existing directory
- Make client side thread safe
- Unreadable directory fixes
- Better flow control handling
- Updated to latest inotify version: 0.23-6
* Tue Mar 15 2005 Daniel Veillard <veillard@redhat.com> 0.0.26-1
- Fix an include problem showing up with gcc4</li>
- Fix the crash on failed tree assert bug #150471 based on patch from Dean Brettle
- removed an incompatibility with SGI FAM #149822
* Tue Mar  1 2005 Daniel Veillard <veillard@redhat.com> 0.0.25-1
- Fix a configure problem reported by Martin Schlemmer
- Fix the /media/* and /mnt/* mount blocking problems from 0.0.24 e.g. #142637
- Fix the monitoring of directory using poll and not kernel
* Fri Feb 18 2005 Daniel Veillard <veillard@redhat.com> 0.0.24-1
- more documentation
- lot of serious bug fixes including Gnome Desktop refresh bug
- extending the framework for more debug (configure --enable-debug-api)
- extending the python bindings for watching the same resource multiple times
  and adding debug framework support
- growing the regression tests a lot based on python bindings
- inotify-0.19 patch from John McCutchan
- renamed python private module to _gamin to follow Python PEP 8

* Tue Feb  8 2005 Daniel Veillard <veillard@redhat.com> 0.0.23-1
- memory corruption fix from Mark on the client side
- extending the protocol and API to allow skipping Exists and EndExists
  events to avoid deadlock on reconnect or when they are not used.

* Mon Jan 31 2005 Daniel Veillard <veillard@redhat.com> 0.0.22-1
- bit of python bindings improvements, added test
- fixed 3 bugs

* Wed Jan 26 2005 Daniel Veillard <veillard@redhat.com> 0.0.21-1
- Added Python support
- Updated for inotify-0.18 

* Thu Jan  6 2005 Daniel Veillard <veillard@redhat.com> 0.0.20-1
- Frederic Crozat seems to have found the GList corruption which may fix
  #132354 and related problems
- Frederic Crozat also fixed poll only mode

* Fri Dec  3 2004 Daniel Veillard <veillard@redhat.com> 0.0.19-1
- still chasing the loop bug, made another pass at checking GList,
  added own copy with memory poisonning of GList implementation.
- fixed a compile issue when compiling without debug

* Fri Nov 26 2004 Daniel Veillard <veillard@redhat.com> 0.0.18-1
- still chasing the loop bug, checked and cleaned up all GList use
- patch from markmc to minimize load on busy apps

* Wed Oct 20 2004 Daniel Veillard <veillard@redhat.com> 0.0.16-1
- chasing #132354, lot of debugging, checking and testing and a bit
  of refactoring

* Sat Oct 16 2004 Daniel Veillard <veillard@redhat.com> 0.0.15-1
- workaround to detect loops and avoid the nasty effects, see RedHat bug #132354

* Sun Oct  3 2004 Daniel Veillard <veillard@redhat.com> 0.0.14-1
- Found and fixed the annoying bug where update were not received
  should fix bugs ##132429, #133665 and #134413
- new mechanism to debug on-the-fly by sending SIGUSR2 to client or server
- Added documentation about internals

* Fri Oct  1 2004 Daniel Veillard <veillard@redhat.com> 0.0.13-1
- applied portability fixes
- hardened the code while chasing a segfault

* Thu Sep 30 2004 Daniel Veillard <veillard@redhat.com> 0.0.12-1
- potential fix for a hard to reproduce looping problem.

* Mon Sep 27 2004 Daniel Veillard <veillard@redhat.com> 0.0.11-1
- update to the latest version of inotify
- inotify support compiled in by default
- fix ABI FAM compatibility problems #133162 

* Tue Sep 21 2004 Daniel Veillard <veillard@redhat.com> 0.0.10-1
- more documentation
- Added support for a configuration file $HOME/.gaminrc
- fixes FAM compatibility issues with FAMErrno and FamErrlist #132944

* Wed Sep  1 2004 Daniel Veillard <veillard@redhat.com> 0.0.9-1
- fix crash with konqueror #130967
- exclude kernel (dnotify) monitoring for /mnt//* /media//*

* Thu Aug 26 2004 Daniel Veillard <veillard@redhat.com> 0.0.8-1
- Fixes crashes of the gam_server
- try to correct the kernel/poll switching mode

* Tue Aug 24 2004 Daniel Veillard <veillard@redhat.com> 0.0.7-1
- add support for both polling and dnotify simultaneously
- fixes monitoring of initially missing files
- load control on very busy resources #124361, desactivating
  dnotify and falling back to polling for CPU drain

* Thu Aug 19 2004 Daniel Veillard <veillard@redhat.com> 0.0.6-1
- fixes simple file monitoring should close RH #129974
- relocate gam_server in $(libexec)

* Thu Aug  5 2004 Daniel Veillard <veillard@redhat.com> 0.0.5-1
- Fix a crash when the client binary forks the gam_server and an
  atexit handler is run.

* Wed Aug  4 2004 Daniel Veillard <veillard@redhat.com> 0.0.4-1
- should fix KDE build problems
