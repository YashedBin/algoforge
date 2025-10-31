# SOME CODE TO TEST on User's Dehalf

```
from Timer import Timer
from MemoryProfiler import MemoryProfiler

def lrs(s):
    with Timer("LRS - DP Table Build", emit_json=True), MemoryProfiler("LRS - DP Table Build", emit_json=True):
        n = len(s)
        dp = [[0 for _ in range(n+1)] for _ in range(n+1)]
        
        for i in range(1,n+1):
            for j in range(1,n+1):
                if s[i-1] == s[j-1] and i != j:
                    dp[i][j] = 1 + dp[i-1][j-1]
                else:
                    dp[i][j] = max(dp[i-1][j],dp[i][j-1])
    
    print("Matrix")
    for row in dp:
        print(row)
    
    with Timer("LRS - Backtrack", emit_json=True), MemoryProfiler("LRS - Backtrack", emit_json=True):
        i,j = n,n 
        lrs_result=[]
        while i > 0 and j > 0:
            if s[i-1] == s[j-1] and i != j:
                lrs_result.append(s[i-1])
                i -= 1 
                j -= 1 
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1 
            else:
                j -= 1 
        
        lrs_result.reverse()
        return "".join(lrs_result)

with Timer("LRS - Full Algorithm", emit_json=True), MemoryProfiler("LRS - Full Algorithm", emit_json=True):
    string = "AABCBDC"
    longest_repeating_subsequence = lrs(string)
    print("Longest repeating subsequence for the string "+string+": "+longest_repeating_subsequence)

```



```
from Timer import Timer
from MemoryProfiler import MemoryProfiler

def optimal_bst_algorithm(P):
    with Timer("OBST - Initialization", emit_json=True), MemoryProfiler("OBST - Initialization", emit_json=True):
        n = len(P)
        C = [[0]*(n+2) for _ in range(n+2)]
        R = [[0]*(n+2) for _ in range(n+2)]
        
        for i in range(1, n+1):
            C[i][i-1] = 0
            C[i][i] = P[i-1]
            R[i][i] = i
        C[n+1][n] = 0
    
    with Timer("OBST - Main Loop", emit_json=True), MemoryProfiler("OBST - Main Loop", emit_json=True):
        for d in range(1, n):
            for i in range(1, n-d+1):
                j = i + d
                minval = float('inf')
                kmin = 0
                
                for k in range(i, j+1):
                    val = C[i][k-1] + C[k+1][j]
                    if val < minval:
                        minval = val
                        kmin = k
                
                R[i][j] = kmin
                sum_prob = sum(P[i-1:j])
                C[i][j] = minval + sum_prob
    
    return round(C[1][n], 4), R

with Timer("OBST - Full Algorithm", emit_json=True), MemoryProfiler("OBST - Full Algorithm", emit_json=True):
    P = [0.1, 0.2, 0.4, 0.3]
    cost, roots = optimal_bst_algorithm(P)

print(f"Minimum expected cost: {cost:.4f}")

```