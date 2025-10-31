#include <iostream>
#include <vector>
#include <limits>
#include <algorithm>
#include <Timer.hpp>
#include <MemoryProfiler.hpp>

int maxCross(const std::vector<int>& a,int l,int m,int r){
    Timer t("MaxCrossSum", true);
    MemoryProfiler m("MaxCrossSum", true);

    int sum=0,left=-1e9,right=-1e9;
    for(int i=m;i>=l;i--){ sum+=a[i]; left=std::max(left,sum); }
    sum=0;
    for(int i=m+1;i<=r;i++){ sum+=a[i]; right=std::max(right,sum); }
    return left+right;
}

int maxSubArrayDC(std::vector<int>& a,int l,int r){
    if(l==r) return a[l];
    int m=(l+r)/2;
    int left,right,cross;
    {
        Timer t("Divide Step", true);
        MemoryProfiler m("Divide Step", true);
        left=maxSubArrayDC(a,l,m);
        right=maxSubArrayDC(a,m+1,r);
        cross=maxCross(a,l,m,r);
    }
    return std::max({left,right,cross});
}

int main(){
    std::vector<int> v={-2,1,-3,4,-1,2,1,-5,4};
    Timer t_all("MaxSubArrayDC", true);
    MemoryProfiler m_all("MaxSubArrayDC", true);
    std::cout<<"Max Sum: "<<maxSubArrayDC(v,0,v.size()-1)<<"\n";
}
