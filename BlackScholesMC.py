import random
import math

##########################################################################
# Using basic Python

def blackScholesMonteCarlo(numPaths,s0,k,T,r,sigma):

    payoffs = []
    
    for i in range(1,numPaths):
        z = random.gauss(0.0,1.0)
        sT = s0 * math.exp((r-0.5*sigma**2) * T + sigma * math.sqrt(T) * z)
        payoffs.append(max(sT-k,0))
        
    value = math.exp(-r*T) * sum(payoffs)/numPaths
    
    return value    

##########################################################################

numPaths = 50000; 
s0 = 100.0; 
k = 100.0 ; 
T=1.0 ; 
r=0.05; 
sigma = 0.20;

price = blackScholesMonteCarlo(numPaths,s0,k,T,r,sigma)

print(price)
