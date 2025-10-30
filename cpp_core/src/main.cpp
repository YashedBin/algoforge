#include <MemoryProfiler.hpp>
#include <Timer.hpp>
#include <vector>        // ← add this
#include <thread>
#include <chrono>

int main() {
    Timer t("C++ Task", true);
    MemoryProfiler m("C++ Task", true);


   std::vector<int> str(100'000'000);
for (size_t i = 0; i < str.size(); ++i){
    str[i] = i;  // sequentially touches all pages

}


    return 0;
}
