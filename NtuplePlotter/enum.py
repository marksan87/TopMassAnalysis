def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

JER_var = enum('down', 'nom', 'up')
JER_var.down

w = JER_var.nom
x = JER_var.up
y = JER_var.down
z = JER_var.up

print "w ",w
print "x ",x
print "y ",y
print "z ",z
print "x == z  ", x == z
print "y == z  ", y == z
print "w == JER_var.nom  ", w == JER_var.nom
