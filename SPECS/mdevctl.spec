Name:		mdevctl
Version:	1.1.0
Release:	4%{?dist}
Summary:	Mediated device management and persistence utility

Group:		System Environment/Kernel
License:	LGPLv2
URL:		https://github.com/mdevctl/mdevctl

Source0:	https://github.com/mdevctl/mdevctl/archive/%{version}/%{name}-%{version}.tar.gz
Source1:	https://github.com/mdevctl/mdevctl/archive/%{version}/%{name}-%{version}-vendor.tar.gz

ExclusiveArch:  %{rust_arches}

BuildRequires: bash
BuildRequires: git
BuildRequires: make
BuildRequires: systemd
BuildRequires: rust-toolset
Requires(post,postun): %{_sbindir}/udevadm

Patch0: 0001-Report-root-error-when-a-callout-can-t-be-executed.patch
Patch1: 0002-tests-read-stdin-in-callout-test-scripts.patch

%description
mdevctl is a utility for managing and persisting devices in the
mediated device device framework of the Linux kernel.  Mediated
devices are sub-devices of a parent device (ex. a vGPU) which
can be dynamically created and potentially used by drivers like
vfio-mdev for assignment to virtual machines.

%prep
%autosetup -S git_am -n %{name}-%{version}
%cargo_prep -V 1

%build
%cargo_build

%install
%make_install

%check
export MDEVCTL_LOG=debug RUST_BACKTRACE=full
%cargo_test

%files
%license COPYING
%doc README.md
%{_sbindir}/mdevctl
%{_sbindir}/lsmdev
%{_udevrulesdir}/60-mdevctl.rules
%dir %{_sysconfdir}/mdevctl.d
%dir %{_sysconfdir}/mdevctl.d/scripts.d/callouts
%dir %{_sysconfdir}/mdevctl.d/scripts.d/notifiers
%{_mandir}/man8/mdevctl.8*
%{_mandir}/man8/lsmdev.8*
%{_datadir}/bash-completion/completions/mdevctl
%{_datadir}/bash-completion/completions/lsmdev

%changelog
* Thu Jan 20 2022 Jonathon Jongsma <jjongsma@redhat.com> - 1.1.0-4
- fix gating.yaml indentation and rebuild

* Thu Jan 13 2022 Jonathon Jongsma <jjongsma@redhat.com> - 1.1.0-3
- add gating.yml and rpminspect.yml and rebuild
  Related: rhbz#1999686

* Wed Dec 01 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 1.1.0-2
- Create additonal directories required by installation.
  Related: rhbz#1999686

* Thu Nov 18 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 1.1.0-1
- Rebase mdevctl to 1.1.0
  Resolves: rhbz#1999686

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 0.78-4
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 0.78-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild


* Tue Nov 24 2020 Alex Williamson <alex.williamson@redhat.com> - 0.78-1
- e029640033d3 ("Automatic version commit for tag 0.78")
- e32f506656fd ("use standard bash path")
- 70690b64401f ("avoid other tags spilling into the .spec changelog")
- 70b89c18cf5b ("Merge pull request #31 from awilliam/20201113.0")
- 80187bc9ba03 ("Merge pull request #30 from fiuczy/fix-error-cleanup")
- 97ea8bbeefb7 ("mdevctl: fix cleanup on error when creating and removing mdev")
- b45d33dfd36c ("version support")
- 2b1c16ce6fb0 ("Fix attributes getting applied via start-parent-mdevs")
- 25d5e8d24d57 ("mdevctl: fix cleanup on error when writing to attribute")

* Fri Jul 17 2020 Cornelia Huck <cohuck@redhat.com> - 0.69-1
- a2621934aa37 ("Merge pull request #18 from cohuck/validate")
- ffbcef5a1c84 ("Merge pull request #25 from etrunko/master")
- 5ec75a83bf30 ("Remove never used 'available' option")
- d49b0f0db6b3 ("Merge pull request #23 from eskultety/man-fix")
- 4cfe37eb2d99 ("man: Point --verbose to the 'list' command rather than 'types'")
- a0ae49eb7178 ("Merge pull request #17 from cohuck/install_symlinks")
- 504beba6e8f9 ("Force symlink cretion")
- 522c5ded00ff ("Fix attribute validation")

* Thu Dec 19 2019 Alex Williamson <alex.williamson@redhat.com> - 0.61-1
- d7dfac5f5bfb ("Merge pull request #15 from cohuck/attr_sanity")
- 28a9fa17b51e ("validate attribute names")

* Thu Dec 05 2019 Alex Williamson <alex.williamson@redhat.com> - 0.59-1
- 3e10c587173c ("Restore BuildRequires")

* Thu Dec 05 2019 Alex Williamson <alex.williamson@redhat.com> - 0.58-1
- 3d6d2b1780f3 ("Remove systemd reference from README")

* Thu Dec 05 2019 Alex Williamson <alex.williamson@redhat.com> - 0.57-1
- 13f1322e576c ("Remove systemd support")
- d84a2737e79c ("Fix device udev tagging")
- 68c92c7beaca ("Tag before generating spec file")
- c34c4f1ade60 ("Update mdevctl.spec.in for lsmdev.8")
- ed86d345aae0 ("Fix systemd UUID escaping")
- d4e83f08161d ("Merge pull request #13 from cpaelzer/fix-lsmdev-man-page")
- 3c0d285b75ab ("lsmdev - add the alternative name to the man page")

* Wed Oct 02 2019 Alex Williamson <alex.williamson@redhat.com> - 0.50-1
- 18c33dfd136d ("Reformat changelog to match Linux commit reference style")

* Tue Oct 01 2019 Alex Williamson <alex.williamson@redhat.com> - 0.49-1
- e2bda0996bd3 ("Fedora integration")

* Fri Sep 27 2019 Alex Williamson <alex.williamson@redhat.com> - 0.48-1
- a6372fc0bd9e ("Create an lsmdev alias")

* Wed Jul 17 2019 Alex Williamson <alex.williamson@redhat.com> - 0.47-1
- 52654b4f6f85 ("Update spec Source0 url")

* Mon Jul 15 2019 Alex Williamson <alex.williamson@redhat.com> - 0.46-1
- 6bfe7b0a22c4 ("Add back BuildRequires for systemd")
- 9cf1afc50b2c ("Allow advanced JSON output from the list command")
- 1c98f58ff505 ("Fixup Makefile and spec for README.md")
- 838cac5ac9f0 ("Merge pull request #12 from cohuck/markdown")
- 2eeda7456288 ("README: convert to markdown")
- 70efa0a3a2ab ("Merge pull request #11 from cohuck/example-verbose")
- 28fe248613c8 ("fix attribute output examples")
- 37bb8f26d1c2 ("Update man page")
- 8f9798a32884 ("Let --index be abbreviated with -i")
- 7ea03365a192 ("Split mdev types from list command")
- b323cf96e4e7 ("Consistent, gratuitous quoting")
- 84044a178502 ("Fix man page install")
- 4e4e45a03154 ("Merge pull request #10 from cohuck/manpage")
- f37b1aa5625d ("add a man page")
- 840c86d1f79c ("simplify attribute handling")
- 1226ba8e4b39 ("Merge pull request #7 from cohuck/json-import-export-doc")
- 02ddfca4d1a2 ("README: update with JSON")
- 0ca6019ba007 ("help text: fix typos")
- 02ca8f9756cd ("Dump and import support")
- a2417e68246d ("Merge pull request #6 from cohuck/print_index")
- a7c759ea3788 ("print index when listing attributes")
- 386af2db03a7 ("Interpret escapes")
- 88033494334e ("Attribute support")
- b08f4939634c ("Rework start logic, add uuidgen support and list active feature")
- b2cf2d1bf1f8 ("Note 'make rpm' support")
- d90876b93f5f ("JSON config files")
- ead45a253a2e ("Merge pull request #5 from cohuck/improve-comments")
- 4d533d8adee5 ("Merge pull request #4 from cohuck/realpath")
- 2a101c6de4e4 ("tweak some comments")
- 387eb4fc84e0 ("use realpath for canonicalization")
- d74bf93dbc79 ("mdevctl: Respin")
- b8c98109e307 ("Merge pull request #3 from cohuck/readme-uuidgen")
- 47e4d255baf2 ("README: avoid inline `uuidgen`")
- 863417ee7a52 ("Merge pull request #2 from c3d/whitespace-and-usage-cleanup")
- dc1d6fc95118 ("Trailing whitespace cleanup")
- 97b393552ab4 ("Put usage message in a single large blob of text")
- b439f53017f3 ("Merge pull request #1 from cohuck/destdir")
- 205040b3c006 ("Makefile: drop extra '/'")
- c51ebb40d3f6 ("mdevctl: Move to https://github.com/mdevctl/mdevctl")
- 914c0076535b ("mdevctl: Don't start mdevs created with --manual")
- 9e84529a5ddd ("mdevctl: Implement defaults and per mdev start option")
- bb5135475bd8 ("mdevctl: Add RPM build support")
- d1f6110c59d4 ("mdevctl: Minor usage fixes")
- 42ba1670288f ("Merge pull request #1 from cohuck/improve_cmdline")
- d27ba583f77b ("mdevctl: improve commandline handling")
- 5114f9eb8268 ("mdevctl: Initial commit")
