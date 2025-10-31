#include <iostream>
#include <vector>
#include <algorithm>
#include <Timer.hpp>
#include <MemoryProfiler.hpp>

int Kadane(std::vector<int>& arr){
    Timer t("Kadane Core", true);
    MemoryProfiler m("Kadane Core", true);

    int max_sum = arr[0], curr = arr[0];
    for(size_t i=1;i<arr.size();i++){
        curr = std::max(arr[i], curr+arr[i]);
        max_sum = std::max(max_sum, curr);
    }
    return max_sum;
}

int main(){
    std::vector<int> a = {-2,1,-3,4,-1,2,1,-5,4};
    Timer t_all("Kadane Full Run", true);
    MemoryProfiler m_all("Kadane Full Run", true);
    std::cout << "Max Sum: " << Kadane(a) << "\n";
}
