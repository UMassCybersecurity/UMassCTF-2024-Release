from modpoly import lagrange_interpolation

with open('../static/journal.txt', 'r') as f:
    p = int(f.readline().split('p = ')[1])

    f.readline()  # Dump the empty line

    given_points = []

    for i in range(101):  # Read in the 101 points
        line = f.readline().strip()
        # Extract the value, and convert to integers
        # We know the x values will just count up so no need to extract them
        value = int(line.split('= ')[1])
        # Append the tuple to the list
        given_points.append((i, value))

# Compute the polynomial
DAY = lagrange_interpolation(given_points, p)

x_vals = [i for i in range(101, 133)]
y_vals = [DAY(x) for x in x_vals]
flag = "".join([chr(y) for y in y_vals])

print(flag)
