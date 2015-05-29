%define product_name leechcraft
%define plugin_dir %{_libdir}/%{product_name}/plugins
%define translations_dir %{_datadir}/%{product_name}/translations
%define settings_dir %{_datadir}/%{product_name}/settings
%define full_version %{version}-%{release}
%define git_version 3466-g864bd1a
%global optflags %(echo %{optflags} | sed 's/-D_FORTIFY_SOURCE=2 //')

Name:           leechcraft-poshuku
Summary:        LeechCraft Web Browser Module
Version:        0.6.75
Release:        1%{?dist}
License:        GPLv2+
Url:            http://leechcraft.org
Source0:        http://dist.leechcraft.org/LeechCraft/%{version}/leechcraft-0.6.70-%{git_version}.tar.xz
Patch1: 001-fix-qwt-cmake-script.patch

BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtwebkit-devel
BuildRequires: qt5-qtx11extras-devel
BuildRequires: qt5-qtscript-devel
BuildRequires: qt5-qttools-devel
BuildRequires: bzip2-devel
BuildRequires: qwt-devel
BuildRequires: pcre-devel
BuildRequires: leechcraft-devel >= %{version}
BuildRequires: qjson-devel
BuildRequires: qrencode-devel
BuildRequires: libidn-devel
BuildRequires:  qwt-qt5-devel
BuildRequires:  clang


%description
This package provides a web browser plugin for LeechCraft.

It is an full-featured web browser based on WebKit.
Poshuku is fully extensible with plugins.

Currently it features:
* support for all major web-standards;
* integration with other plugins;
* autodiscovery;
* tagging bookmarks;
* support for SQLite or PostgreSQL storage.




%package devel
Summary:    Leechcraft Poshuku Development Files
Requires:   %{name}%{?_isa} >= %{version}

%description devel
This package contains header files required to develop new modules for
LeechCraft Poshuku.


%prep
%setup -qn %{product_name}-0.6.70-%{git_version}
%patch1 -p 0

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DLEECHCRAFT_VERSION="%{version}" \
    -DUSE_QT5=True \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
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
                "leechcraft_poshuku_autosearch"\
                "leechcraft_poshuku_cleanweb"\
                "leechcraft_poshuku_dcac"\
                "leechcraft_poshuku_fatape"\
                "leechcraft_poshuku_filescheme"\
                "leechcraft_poshuku_fua"\
                "leechcraft_poshuku_keywords"\
                "leechcraft_poshuku_onlinebookmarks"\
                "leechcraft_poshuku_onlinebookmarks_delicious"\
                "leechcraft_poshuku_onlinebookmarks_readitlater"\
                "leechcraft_poshuku_qrd"\
                "leechcraft_poshuku_speeddial"\
                )

for i in "${arr[@]}"
do
   %find_lang $i --with-qt --without-mo
done

cat *.lang > poshuku.lang


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f poshuku.lang
%{_datadir}/%{product_name}/installed/poshuku/LeechCraft.Poshuku

%{plugin_dir}/libleechcraft_poshuku*.so
%{settings_dir}/*.xml


%files devel
%{_includedir}/%{product_name}/*

%changelog
* Fri May 29 2015 Minh Ngo <minh@fedoraproject.org> - 0.6.75-1
- 0.6.75-1

* Sat Dec 27 2014 Minh Ngo <minh@fedoraproject.org> - 0.6.70-2
- 0.6.70-2

