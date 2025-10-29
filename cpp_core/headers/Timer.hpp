#pragma once
#include <iostream>
#include <chrono>
#include <string>

class Timer {
private:
    std::chrono::time_point<std::chrono::high_resolution_clock> startTime, endTime;
    std::string workDone;
    bool emitJSON;

public:
    Timer(std::string workDone, bool json = false)
        : workDone(workDone), emitJSON(json) {
        // Start the Time for the Scoped Block
        startTime = std::chrono::high_resolution_clock::now();
    }
    ~Timer() {
        endTime = std::chrono::high_resolution_clock::now();
        std::chrono::nanoseconds duration = std::chrono::duration_cast<std::chrono::nanoseconds>(endTime - startTime);
        // The Difference and Casting into Duration ( a scaled quantity of numbers )

        output(duration);
    }

    void output(std::chrono::nanoseconds duration){
    if(emitJSON){
        std::cout << "{\"type\":\"timing\",\"work\":\"" << workDone 
                  << "\",\"duration_ns\":" << duration.count() << "}\n";
    }
    else {
        std::cout << workDone << "\nTime: "
                  << duration.count() / 1e6 << " ms\n";
    }
    
};