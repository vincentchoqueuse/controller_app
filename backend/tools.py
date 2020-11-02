import numpy as np
from numpy import angle, array, empty, finfo, ndarray, ones, \
    polyadd, polymul, polyval, roots, sqrt, zeros, squeeze, exp, pi, \
    where, delete, real, poly, nonzero
from scipy.signal import dlti,lti, cont2discrete, bode, step,freqresp
import scipy
from copy import deepcopy
import json

class TransferFunction():

    def __init__(self, num,den,dt=None):
        self.num = num
        self.den = den
        self.dt = dt

    def __neg__(self):
        num = deepcopy(self.num)
        num *= -1
        return TransferFunction(num, self.den, self.dt)

    def __add__(self, other):
        dt = self.dt
        num1 = self.num
        num2 = other.num
        den1 = self.den
        den2 = other.den
        num = polyadd(polymul(num1, den2), polymul(num2, den1))
        den = polymul(den1, den2)
        return TransferFunction(num, den, dt)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __mul__(self, other):
        num = polymul(other.num, self.num)
        den = polymul(other.den, self.den)
        dt = self.dt
        return TransferFunction(num, den, dt)

    def __rmul__(self, other):
        num = polymul(other.num, self.num)
        den = polymul(other.den, self.den)
        dt = self.dt
        return TransferFunction(num, den, dt)

    def __truediv__(self, other):
        num = polymul(self.num, other.den)
        den = polymul(self.den, other.num)
        return TransferFunction(num, den, dt)

    def __div__(self, other):
        return TransferFunction.__truediv__(self, other)

    def __rtruediv__(self, other):
        return other / self

    def __rdiv__(self, other):
        return TransferFunction.__rtruediv__(self, other)

    def __pow__(self, other):
        if not type(other) == int:
            raise ValueError("Exponent must be an integer")
        if other == 0:
            return TransferFunction([1], [1])  # unity
        if other > 0:
            return self * (self**(other - 1))
        if other < 0:
            return (TransferFunction([1], [1]) / self) * (self**(other + 1))

    def __str__(self):
        return "num: {}\nden: {}".format(self.num,self.den)

    def poles(self):
        return roots(self.den)

    def zeros(self):
        return roots(self.num)
    
    @property
    def lti(self):
        if self.dt == None:
            sys = lti(self.num,self.den)
        else:
            sys = dlti(self.num,self.den,dt=self.dt)
        return sys


    def bode(self, w=None, n=10000):
        w,Hjw = self.lti.freqresp(w=w, n=n)
        if self.dt is not None:
            w = w/self.dt
        mag = np.abs(Hjw)
        phase = 180*np.angle(Hjw)/np.pi
        return w,mag,phase

    def step(self,X0=None, T=None, N=None):
        if self.dt == None:
            t,s = self.lti.step(X0=X0, T=T, N=N)
        else:
            t, s = self.lti.step(t=T, n=N)
            s = np.ravel(s)
            t = np.arange(len(s))*self.dt
        return t,s

def tf(*args):
    return TransferFunction(*args)

def feedback(sys1,sys2,sign=-1):
    
    dt = sys1.dt
    num1 = sys1.num
    den1 = sys1.den

    if isinstance(sys2, TransferFunction):
        num2 = sys2.num
        den2 = sys2.den
    else:
        num2 = sys2
        den2 = 1
    
    num = polymul(num1, den2)
    den = polyadd(polymul(den2, den1), -sign * polymul(num2, num1))
    
    return TransferFunction(num, den, dt)


def get_controller_sys(type,Ki,Ti,dt=None):
    
    if dt == None:
        if type == "none":
            sys = TransferFunction([1],[1])
        if type == "P":
            sys = TransferFunction([Ki],[1])
        if type == "PI":
            sys = TransferFunction([Ki*Ti,Ki],[Ti,0])
    
    else:
        if type == "none":
            sys = TransferFunction([1],[1],dt=dt)
        if type == "P":
            sys = TransferFunction([Ki],[1],dt=dt)
        if type == "PI":
            sys1 = TransferFunction([Ki],[1],dt=dt)
            sys2 = TransferFunction([Ki*dt/Ti,0],[1,-1],dt=dt)
            sys = sys1+sys2
    return sys


def system(num,den,type,Ki,Ti,CL,Ts=None):
    Fp = TransferFunction(num,den,dt=Ts)
    Cp = get_controller_sys(type,Ki,Ti,dt=Ts)
    H = Cp*Fp
    if CL == True:
        H = feedback(H,1)
    return H

