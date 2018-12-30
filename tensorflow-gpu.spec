Name:           tensorflow-gpu
Version:		%{VERSION}
Release:        %{RELEASE}%{?dist}
Summary:        An Open Source Machine Learning Framework for Everyone 
License:        Apache 2
Group:          Development/Libraries/C and C++
Url:            https://www.tensorflow.org/
Source0:        tensorflow-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  patch
BuildRequires:  libcudnn7-devel
BuildRequires:  cuda-10-0

%description
TensorFlow is an open source software library for numerical computation using data flow graphs.

%package devel
Summary:    Development headers and library for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   eigen3-devel
Requires:   protobuf-devel >= 3.6.0
Requires:   abseil-cpp-devel

%description devel
This package contains the development headers for %{name}.

%prep
%setup -n tensorflow-%{version}

%build
bazel clean
bazel build --action_env=TF_NEED_CUDA="1" --action_env=CUDA_TOOLKIT_PATH="/usr/local/cuda" --action_env=TF_CUDA_VERSION="10.0" --action_env=CUDNN_INSTALL_PATH="/usr/lib64" --action_env=TF_CUDNN_VERSION="7" --action_env=TF_CUDA_COMPUTE_CAPABILITIES="5.2" --define=grpc_no_ares=true --copt=-mavx2 //tensorflow:libtensorflow.so
bazel build --action_env=TF_NEED_CUDA="1" --action_env=CUDA_TOOLKIT_PATH="/usr/local/cuda" --action_env=TF_CUDA_VERSION="10.0" --action_env=CUDNN_INSTALL_PATH="/usr/lib64" --action_env=TF_CUDNN_VERSION="7" --action_env=TF_CUDA_COMPUTE_CAPABILITIES="5.2" --define=grpc_no_ares=true --copt=-mavx2 //tensorflow:libtensorflow_cc.so

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/lib64
cp bazel-bin/tensorflow/*.so $RPM_BUILD_ROOT/usr/lib64

mkdir -p $RPM_BUILD_ROOT%{_includedir}/tensorflow
cp -r bazel-genfiles/tensorflow/* $RPM_BUILD_ROOT%{_includedir}/tensorflow
cp -r tensorflow/c $RPM_BUILD_ROOT%{_includedir}/tensorflow
cp -r tensorflow/cc $RPM_BUILD_ROOT%{_includedir}/tensorflow
cp -r tensorflow/core $RPM_BUILD_ROOT%{_includedir}/tensorflow
find $RPM_BUILD_ROOT%{_includedir}/tensorflow -type f  ! -name "*.h" -delete

mkdir -p $RPM_BUILD_ROOT%{_includedir}/tensorflow/third_party/eigen3
cp -r third_party/eigen3 $RPM_BUILD_ROOT%{_includedir}/tensorflow/third_party

%clean
rm -rf $RPM_BUILD_ROOT

%post
ldconfig

%postun
ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README.md AUTHORS ACKNOWLEDGMENTS
%{_libdir}/libtensorflow.so
%{_libdir}/libtensorflow_cc.so
%{_libdir}/libtensorflow_framework.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/tensorflow/*

%changelog
