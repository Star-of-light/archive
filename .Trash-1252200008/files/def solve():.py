def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
        
    t = int(data[0])
    results = []
    
    idx = 1
    for _ in range(t):
        n = int(data[idx])
        k = int(data[idx+1])
        idx += 2
        
        # Calculate the maximum possible money using the derived formula
        ans = (1 << (n - k + 1)) + 2 * (k - 1)
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()



