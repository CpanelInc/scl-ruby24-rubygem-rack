# Defining the package namespace
%global ns_name ea
%global ns_dir /opt/cpanel
%global pkg ruby24
%global gem_name rack

# Force Software Collections on
%global _scl_prefix %{ns_dir}
%global scl %{ns_name}-%{pkg}
# HACK: OBS Doesn't support macros in BuildRequires statements, so we have
#       to hard-code it here.
# https://en.opensuse.org/openSUSE:Specfile_guidelines#BuildRequires
%global scl_prefix %{scl}-
%{?scl:%scl_package rubygem-%{gem_name}}

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define release_prefix 1

Name:           %{?scl_prefix}rubygem-%{gem_name}
Summary:        Common API for connecting web frameworks, web servers and layers of software
Version:        2.2.2
Release:        %{release_prefix}%{?dist}.cpanel
Group:          Development/Languages
# lib/rack/backports/uri/* are taken from Ruby which is (Ruby or BSD)
License:        MIT and (Ruby or BSD)
URL:            http://rubyforge.org/projects/%{gem_name}/
Source0:        http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
Requires:       %{?scl_prefix}ruby(rubygems)
Requires:       %{?scl_prefix}ruby(release)
%{?scl:Requires:%scl_runtime}

BuildRequires:  %{?scl_prefix}ruby
BuildRequires:  %{?scl_prefix}rubygems-devel
BuildRequires:  scl-utils
BuildRequires:  scl-utils-build
%{?scl:BuildRequires: %{scl}-runtime}

BuildArch:      noarch
Provides:       %{?scl_prefix}rubygem(%{gem_name}) = %{version}
Provides:       bundled(okjson) = 20130206

%description
Rack provides a common API for connecting web frameworks,
web servers and layers of software in between

%prep
%setup -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}


%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{gem_instdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{gem_instdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

%clean
rm -rf %{buildroot}

%files
%dir %{gem_instdir}
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/SPEC.rdoc
%doc %{gem_instdir}/example
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/contrib
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/%{gem_name}.gemspec
%{gem_libdir}
%{gem_instdir}/bin
%{_bindir}/rackup
%exclude %{gem_cache}
%{gem_spec}

%changelog
* Thu Apr 16 2020 Cory McIntire <cory@cpanel.net> - 2.2.2-1
- EA-9011: Update scl-ruby24-rubygem-rack from v2.0.1 to v2.2.2

* Mon Apr 17 2017 Rishwanth Yeddula <rish@cpanel.net> 2.0.1-1
- initial packaging
