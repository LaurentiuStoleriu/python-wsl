
val_ini = 0.0
val_fin = 200.0
step = 0.005

myrange = [(x / 1000.0) for x in range(int(val_ini*1000.0), int(val_fin*1000.0), int(step*1000.0))]

for i in myrange:
  if ( i % 1 == 0 ):
    print(f"Going from {val_ini} to {val_fin} - we are now at {i}")