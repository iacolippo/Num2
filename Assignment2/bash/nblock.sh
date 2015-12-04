#! /bin/sh
#number of step is divided by delta in python script --> gets higher or lower in function of delta
#this is because bash doesn't allow floating point arithmetic
#I have to make more cycles with more dense points
for x in 1 2 5 10 20 25 50 100 250 500 1000 2500 5000 10000 25000 50000 100000 250000 500000

do

cat > in-block-$x.txt << EOF
delta 1
nsteps 1000000
q0 0.0
nblock $x
EOF

time python mcmc.py in-block-$x.txt out-block-$x.txt

done