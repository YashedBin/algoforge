// kruskal.cpp
#include <iostream>
#include <algorithm>
#include <vector>
#include <tuple>
//ignore these Im handling these with G++ headers throwing
#include "MemoryProfiler.hpp"
#include "Timer.hpp"

int parent[1000];

void make_set(int v){ parent[v]=v; }
int find_set(int v){ return parent[v]==v ? v : parent[v]=find_set(parent[v]); }
void union_sets(int a,int b){ a=find_set(a); b=find_set(b); if(a!=b) parent[b]=a; }

int main(){
    std::vector<std::tuple<int,int,int>> cost;
    cost.push_back({28,1,2});
    cost.push_back({16,2,3});
    cost.push_back({16,2,7});
    cost.push_back({24,5,7});
    cost.push_back({12,3,4});
    cost.push_back({22,5,4});
    cost.push_back({10,1,6});
    cost.push_back({26,5,6});
    std::sort(cost.begin(), cost.end()); // sort by cost (tuple first element)

    int V = 7;
    for(int i=1;i<=V;i++) make_set(i);

    int mincost=0;
    std::vector<std::vector<int>> tree;
    int i=0, edgeCount=0;
    while(edgeCount < V-1 && i < (int)cost.size()){
        int w = std::get<0>(cost[i]);
        int u = std::get<1>(cost[i]);
        int v = std::get<2>(cost[i]);
        if(find_set(u) != find_set(v)){
            union_sets(u,v);
            tree.push_back({u,v,w});
            mincost += w;
            edgeCount++;
        }
        i++;
    }

    std::cout << "Minimum Cost: " << mincost << std::endl;
    for(auto &e: tree) std::cout << e[0] << " - " << e[1] << " : " << e[2] << '\n';
    return 0;
}
