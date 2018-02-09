import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
#norm.cdf(1.96)

def solve(m1,m2,std1,std2):
  a = 1/(2*std1**2) - 1/(2*std2**2)
  b = m2/(std2**2) - m1/(std1**2)
  c = m1**2 /(2*std1**2) - m2**2 / (2*std2**2) - np.log(std2/std1)
  return np.roots([a,b,c])

m1 = 2.5
std1 = 1.0
m2 = 5.0
std2 = 1.0

#Get point of intersect
result = solve(m1,m2,std1,std2)

#Get point on surface
x = np.linspace(-5,9,10000)
plot1=plt.plot(x,norm.pdf(x,m1,std1), label='User Distribution', color = 'r')
plot2=plt.plot(x,norm.pdf(x,m2,std2), label = 'Ranked Songs Distribution', color = 'b')
plot3=plt.plot(result,norm.pdf(result,m1,std1),'o', color = 'g')
plt.legend(loc=2, borderaxespad=0.)

#Plots integrated area
r = result[0]
olap = plt.fill_between(x[x>r], 0, norm.pdf(x[x>r],m1,std1),alpha=0.2, facecolor='r')
olap = plt.fill_between(x[x<r], 0, norm.pdf(x[x<r],m2,std2),alpha=0.2, facecolor='b')

# integrate
area = norm.cdf(r,m2,std2) + (1.-norm.cdf(r,m1,std1))

print 'Overlap Percentage:', area
plt.text(-5, 0.3, 'Overlap Percentage: %f' %(area*100), fontsize=12)
plt.show()
