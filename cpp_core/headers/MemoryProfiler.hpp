/* as Timer.hpp can run on any OS because of Chrono 
Supporting it, Memory usage isnt the same
So we have a Different Approach here Considering Linux 
(I'm using WSL to program this whole project)
and Windows to also get a Demo like feel*/

#pragma once
#include <chrono>
#include <iostream>
#include <string>

#ifdef __linux__
    #include <sys/resource.h>
    #include <unistd.h>
    #include <cstdio>
#elif _WIN32
    #include <windows.h>
    #include <psapi.h>
#endif

class MemoryProfiler {
private:
    std::string workDone;
    bool emitJSON;
    size_t startMemoryKB;

    size_t getCurrentMemoryKB() {
    #ifdef __linux__
        // Read from /proc/self/statm for accurate RSS (resident set size)
        long rss = 0L;
        FILE* fp = fopen("/proc/self/statm", "r");
        if (fp) {
            if (fscanf(fp, "%*s%ld", &rss) != 1)
                rss = 0L;
            fclose(fp);
        }
        return (size_t)rss * (size_t)sysconf(_SC_PAGESIZE) / 1024; 
    #elif _WIN32
        PROCESS_MEMORY_COUNTERS_EX pmc;
        GetProcessMemoryInfo(GetCurrentProcess(), (PROCESS_MEMORY_COUNTERS*)&pmc, sizeof(pmc));
        return pmc.WorkingSetSize / 1024;
    #else
        return 0;
    #endif
    }

public:
    MemoryProfiler(std::string work, bool json = false)
        : workDone(work), emitJSON(json) {
        startMemoryKB = getCurrentMemoryKB();
    }

    ~MemoryProfiler() {
        size_t endMemoryKB = getCurrentMemoryKB();
        long long deltaKB = static_cast<long long>(endMemoryKB) - static_cast<long long>(startMemoryKB);

        if (emitJSON) {
            std::cout << "{\"type\":\"memory\",\"work\":\"" << workDone
                      << "\",\"start_kb\":" << startMemoryKB
                      << ",\"end_kb\":" << endMemoryKB
                      << ",\"delta_kb\":" << deltaKB << "}\n";
        } else {
            std::cout << workDone << "\n"
                      << "Memory Start: " << startMemoryKB << " KB\n"
                      << "Memory End: " << endMemoryKB << " KB\n"
                      << "Memory Delta: " << deltaKB << " KB\n";
        }
    }
};
