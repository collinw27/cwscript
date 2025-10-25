
# Should change upon executing

print "Unseeded:";
print irandom 10;
print random;

# Should be consistent

print "\nSeeded:";
rng_seed 12345;
print irandom_range 10 20;
print random_range 0.1 0.2;
.seed = rng_get;

# Should change upon executing

print "\nReset:";
rng_reset;
print irandom 10;
print random;

# Should be consistent

print "\nRe-seeded";
print join ["Seed = ", rng_seed .seed] "";
print irandom 10;
print random;