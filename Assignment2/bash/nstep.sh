#! /bin/sh

for x in 1000 5000 10000 50000 100000 500000 1000000 5000000 10000000

do

cat > in-nstep-$x.txt << EOF
delta 0.1
nsteps $x
q0 0.0
nblock 1000
EOF

time python mcmc.py in-nstep-$x.txt out-nstep-$x.txt

done