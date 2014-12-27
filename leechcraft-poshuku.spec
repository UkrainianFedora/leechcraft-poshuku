%define product_name leechcraft
%define plugin_dir %{_libdir}/%{product_name}/plugins
%define translations_dir %{_datadir}/%{product_name}/translations
%define settings_dir %{_datadir}/%{product_name}/settings
%define full_version %{version}-%{release}

Name:           leechcraft-poshuku
Summary:        IM Client for LeechCraft
Version:        0.6.70
Release:        2%{?dist}
License:        GPLv2+
Url:            http://leechcraft.org
Source0:        http://dist.leechcraft.org/LeechCraft/0.6.70/leechcraft-0.6.70.tar.xz 


BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: qt4-devel
BuildRequires: qt-webkit-devel
BuildRequires: bzip2-devel
BuildRequires: qwt-devel
BuildRequires: pcre-devel
BuildRequires: leechcraft-devel >= %{version}
BuildRequires: qjson-devel


%description
This package contains an IM client for LeechCraft.


%package devel
Summary:    Leechcraft Azoth Development Files
Requires:   %{name}%{?_isa} = %{full_version}

%description devel
This package contains header files required to develop new modules for
LeechCraft Azoth.


%prep
%setup -qn %{product_name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DLEECHCRAFT_VERSION="%{version}" \
    $(cat ../src/CMakeLists.txt | egrep "^(cmake_dependent_)?option \(ENABLE" | awk '{print $2}' | sed 's/^(/-D/;s/$/=False/;s/\(POSHUKU[^=]*=\)False/\1True/' | xargs) \
    $(cat ../src/plugins/poshuku/CMakeLists.txt | egrep "^option \(ENABLE" | awk '{print $2}' | sed 's/^(/-D/;s/$/=True/' | xargs) \
    ../src

cd plugins/poshuku
make %{?_smp_mflags} 
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd %{_target_platform}/plugins/poshuku/
make install/fast DESTDIR=$RPM_BUILD_ROOT
popd

declare -a arr=("leechcraft_poshuku"\
                )

for i in "${arr[@]}"
do
   %find_lang $i --with-qt --without-mo
done

cat *.lang > poshuku.lang


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f poshuku.lang
%{plugin_dir}/libleechcraft_poshuku*.so 
%{settings_dir}/*.xml


%files devel
%{_includedir}/%{product_name}/*

%changelog
* Sat Dec 27 2014 Minh Ngo <minh@fedoraproject.org> - 0.6.70-2
- 0.6.70-2

