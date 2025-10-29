#include "Timer.hpp"
#include "MemoryProfiler.hpp"
#include <vector>
#include <iostream>

int main() {
    std::cout << "Testing Timer and MemoryProfiler\n\n";
    
    {
        Timer t("Vector allocation", true);
        MemoryProfiler mp("Vector allocation", true);
        
        std::vector<int> huge(1000000);
        for(int i = 0; i < 1000000; i++) {
            huge[i] = i * 2;
        }
    }
    
    std::cout << "\nTest complete!\n";
    return 0;
}