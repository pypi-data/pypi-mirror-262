# TwoSamplesBinomial: Two-sample testing for counts data
Usually in the context of a multiple testing approach to compare two or more frequency tables. Combine with ``multiple-hypothesis-testing`` to
obtain a global test for the significance of the difference between the 
tables.

References:
- [1] D. L. Donoho and A. Kipnis. (2022) Higher criticism to compare two large frequency tables, with sensitivity to possible rare and weak differences. Annals of Statistics. 
- [2]  C. B. Dean. (1992) Testing for Overdispersion in Poisson and Binomial Regression Models. Journal of the American Statistical Association


## Methods:
- ``bin_allocation_test`` (the test from [1])
- ``bin_variance_test`` (test from [2])
- ``bin_variance_test_df`` the same as ``bin_variance_test`` plus additional information


### Additional auxiliary function of independent interest:
 - ``poisson_test`` Vectorized one-sided Poisson test with an option to do a randomized test
 - ``binom_test`` Vectorized one-sided binomial test with an option to do a randomized test
 - ``binom_test_two_sided`` Vectorized Two-sided binomial test with an option to do a randomized test
 - ``binom_test_two_sided_slow`` Vectorized two-sided binomial test using scipy.stats.binom_test

## Example:
```
from twosample import bin_allocation_test, bin_variance_test
from multitest import MultiTest
import numpy as np

N = 100
n = 500
eps = 0.1
mu = 0.01

P = np.ones(N) / N
Q = P.copy()
Q[np.random.rand(N) < eps] += mu
Q = Q / Q.sum()

  
smp1 = np.random.multinomial(n, P)  # sample form P
smp2 = np.random.multinomial(n, Q)  # sample from Q

pvals_alloc = bin_allocation_test(smp1, smp2) # binomial P-values
pvals_var = bin_variance_test(smp1, smp2) # binomial P-values

mt_alloc = MultiTest(pvals_alloc)
mt_var = MultiTest(pvals_var)

print("HC(binomial_allocation) = ", mt_alloc.hc()[0])
print("HC(varaince) = ", mt_var.hc()[0])
```
