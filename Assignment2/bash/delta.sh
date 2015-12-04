#! /bin/sh
#number of step is divided by delta in python script --> gets higher or lower in function of delta
#this is because bash doesn't allow floating point arithmetic

for x in 0.001 0.005 0.01 0.05 0.1 0.5 1 2.5 5 7.5 10 13 14 15 16 17.5 18 19 20 21 22 25 30 37.5 45 50 55 60 65 70 75 80 85 90 95 100

do

cat > in-delta-$x.txt << EOF
delta $x
nsteps 1000000
q0 0.0
nblock 1000
EOF

time python mcmc.py in-delta-$x.txt out-delta-$x.txt

done