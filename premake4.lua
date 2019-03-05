solution 'toxotidae'
    configurations {'release', 'debug'}
    location 'build'
    project 'toxotidae'
        kind 'ConsoleApp'
        language 'C++'
        location 'build'
        files {'source/toxotidae.hpp', 'applications/toxotidae.cpp'}
        configuration 'release'
            targetdir 'build/release'
            defines {'NDEBUG'}
            flags {'OptimizeSpeed'}
        configuration 'debug'
            targetdir 'build/debug'
            defines {'DEBUG'}
            flags {'Symbols'}
        configuration 'linux'
            links {'pthread'}
            buildoptions {'-std=c++11'}
            linkoptions {'-std=c++11'}
        configuration 'macosx'
            buildoptions {'-std=c++11'}
            linkoptions {'-std=c++11'}
