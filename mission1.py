
#No loops!
# :)

def Yn_pow4(Yn_list):
    if not Yn_list:
        return 0
    
    Yn, *Yn_rest = Yn_list
    #Splits off first value and keeps the rest for the next call
    Yn_valid = -100 <= Yn <= 100
    Yn_contrib = Yn ** 4 if (Yn_valid and Yn <= 0) else 0
    #Only counts Yn^4 IF the Yn is NOT a positive number(zero or negative ONLY)
    
    return Yn_contrib + Yn_pow4(Yn_rest)


def process(count, results):
    if count == 0:
        return results
    #Handles one test case at a time then calls itself again instead of using a loop
    #and once count hits 0, it returns the collected results
    
    X = int(input().strip())
    Yn_tokens = input().split()
    #X is the expected number of Yn values for the test case
    #Yn_tokens are the values as text but split apart to see if the count is right
    
    if len(Yn_tokens) != X or not (0 < X <= 100):
        results.append(-1)
    else:
        Yn_list = list(map(int, Yn_tokens))
        results.append(Yn_pow4(Yn_list))
        
    return process(count - 1, results)


def main():
    N = int(input().strip())
    #The above is for the total number of test cases
    N = N if (1 <= N <= 100) else 0
    #Safe guard for the range
    results = process(N, [])
    #Process all N test cases, giving ONE result per case
    
    if results:
        print("\n".join(map(str, results)))
        
        
if __name__ == "__main__":
    main()
    
