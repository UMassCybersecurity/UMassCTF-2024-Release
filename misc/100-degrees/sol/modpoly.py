from typing import List


class Polynomial:
    def __init__(self, coefficients: List[int], p: int):
        self.coefficients = coefficients
        self.p = p

    def __add__(self, other: 'Polynomial'):
        assert self.p == other.p, "Polynomials are over different base fields"

        result = [0] * max(len(self.coefficients), len(other.coefficients))
        for i in range(len(self.coefficients)):
            result[i] = (result[i] + self.coefficients[i]) % self.p
        for i in range(len(other.coefficients)):
            result[i] = (result[i] + other.coefficients[i]) % self.p
        return Polynomial(result, self.p)

    def __mul__(self, other: 'Polynomial'):
        assert self.p == other.p, "Polynomials are over different base fields"
        result = [0] * (len(self.coefficients) + len(other.coefficients) - 1)
        for i, a in enumerate(self.coefficients):
            for j, b in enumerate(other.coefficients):
                result[i + j] = (result[i + j] + a * b) % self.p
        return Polynomial(result, self.p)

    def __neg__(self):
        return Polynomial([-x for x in self.coefficients], self.p)

    def __sub__(self, other: 'Polynomial'):
        assert self.p == other.p, "Polynomials are over different base fields"

        return self + (-other)

    def __str__(self):
        return f'{self.coefficients} (mod {self.p})'

    def __call__(self, *args, **kwargs):
        x_to_i = 1
        y = self.coefficients[0]
        for a_i in self.coefficients[1:]:
            x_to_i = (x_to_i * args[0]) % self.p
            y += (a_i * x_to_i) % self.p
        return y % self.p

    def scalar_multiply(self, scalar: int):
        return Polynomial([(a_i * scalar) % self.p for a_i in self.coefficients], self.p)

    def degree(self):
        d = len(self.coefficients)
        while d > 0:
            d -= 1
            if self.coefficients[d]:
                break
        return d


def lagrange_interpolation(points, p):
    def lagrange_basis(k):
        # Constructs the k-th Lagrange basis polynomial
        basis = Polynomial([1], p)
        for j, (x_j, _) in enumerate(points):
            if j != k:
                basis = basis * Polynomial([-x_j, 1], p)
                denominator = (points[k][0] - x_j) % p
                inv_denominator = pow(denominator, -1, p)  # Modular inverse
                basis = basis.scalar_multiply(inv_denominator)
        return basis

    # Initialization of the interpolation polynomial
    interpolation_poly = Polynomial([0], p)

    # Constructing the interpolation polynomial
    for i, (_, y_i) in enumerate(points):
        # basis_poly = lagrange_basis(k).scalar_multiply(y_k)
        # term = basis_poly
        interpolation_poly = interpolation_poly + lagrange_basis(i).scalar_multiply(y_i)

    return interpolation_poly
