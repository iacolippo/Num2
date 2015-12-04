#! /bin/sh

for x in 0 0.25 0.5 0.75 1 2.5 5 7.5 10 25 50 75 100

do

cat > in-q0-$x.txt << EOF
delta 0.1
nsteps 100000
q0 $x
nblock 1000
EOF

time python mcmc.py in-q0-$x.txt out-q0-$x.txt

done