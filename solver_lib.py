import numpy as np
import time

def J_cal(m_axle, m_disk, r_axle, r_disk):
	m_axle, m_disk, r_axle, r_disk = float(m_axle), float(m_disk), float(r_axle), float(r_disk)
	return 0.5 * (m_axle * r_axle ** 2 + m_disk * (r_axle ** 2 + r_disk ** 2))

def c_cal(r_disk, r_axle, m_disk, m_axle, l, J, mu=0.000178, rho=0.001225, g=9.81):

	r_disk, r_axle, m_disk, m_axle, l = float(r_disk), float(r_axle), float(m_disk), float(m_axle), float(l)

	c1 = 2 * np.pi * rho * l * (r_axle ** 2) * r_disk * ((2 * mu) ** 0.5)
	c1 = c1 / ((J + (m_axle + m_disk) * (r_axle ** 2)) * (r_axle ** 0.5))

	c2 = 2 * np.pi * rho * l * (r_axle ** 2) * mu
	c2 = c2 / (J + (m_axle + m_disk) * (r_axle ** 2))

	c3 = (m_disk + m_axle) * g * (r_axle ** 2)
	c3 = c3 / (J + (m_axle + m_disk) * (r_axle ** 2))

	return (c1, c2, c3)

def phi(v):
	return v
def ksi(c, v, s):
    v = -v if v < 0 else v
    return -c[0] * s * v ** 1.5 - c[1] * s * v + c[2]

def one_step(z, v, s, c, l):
	dt = 0.01
	k1 = dt * phi(v)
	m1 = dt * ksi(c, v, s)
	k2 = dt * phi(v + m1 / 2)
	m2 = dt * ksi(c, v + m1 / 2, s)
	k3 = dt * phi(v + m2 / 2)
	m3 = dt * ksi(c, v + m2 / 2, s)
	k4 = dt * phi(v + m3)
	m4 = dt * ksi(c, v + m3, s)

	dv = (m1 + 2 * m2 + 2 * m3 + m4) / 6
	dz = (k1 + 2 * k2 + 2 * k3 + k4) / 6

	if s == 1:
		if z + dz > l:
			v = -v
			s = -1
			return (z, v, s)
		z += dz
		v += dv
		return (z, v, s)
	if v + dv > 0:
		v = 0
		s = 1
		return (z, v, s)
	v += dv
	z += dz
	return (z, v, s)
