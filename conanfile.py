from conans import ConanFile, CMake, tools,AutoToolsBuildEnvironment
from shutil import copyfile
import os

class LibdvConan(ConanFile):
    name = "libdv"
    version = "1.0.0"
    description = "The Quasar DV Codec (libdv) is a software CODEC for DV video, the encoding format used by most digital camcorders"
    url = "https://github.com/conanos/libdv"
    license = "LGPLv2_1Plus"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    source_subfolder = "source_subfolder"

    def source(self):
        url_ = 'http://sourceforge.net/projects/libdv/files/{name}/{version}/{name}-{version}.tar.gz'.format(name=self.name,version=self.version)
        tools.get(url_)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            #self.run("autoreconf -f -i")
            autotools = AutoToolsBuildEnvironment(self)
            _args = ["--prefix=%s/builddir"%(os.getcwd())]
            if self.options.shared:
                _args.extend(['--enable-shared=yes','--enable-static=no'])
            else:
                _args.extend(['--enable-shared=no','--enable-static=yes'])
            autotools.configure(args=_args)
            autotools.make(args=["-j4"])
            autotools.install()

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir"%(os.getcwd()))


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

