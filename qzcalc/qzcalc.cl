# Bo Milvang-Jensen (milvang@mpe.mpg.de), 14-Nov-2003

# Task to quickly calculate a redshift ...

procedure qzcalc (x1,y1,x2,y2,x3,y3,l1,l2,l3)

real    x1         {"", prompt="x-coordinate of left skyline"}
real    y1         {"", prompt="y-coordinate of left skyline (not used)"}
real    x2         {"", prompt="x-coordinate of emission line"}
real    y2         {"", prompt="y-coordinate of emission line (not used)"}
real    x3         {"", prompt="x-coordinate of right skyline"}
real    y3         {"", prompt="y-coordinate of right skyline (not used)"}
real    l1         {"", prompt="(rest-frame) wavelength of left skyline"}
real    l2         {"", prompt="(rest-frame) wavelength of emission line"}
real    l3         {"", prompt="(rest-frame) wavelength of right skyline"}

begin

real	disp, lobs, z

# Calculate "dispersion" (i.e. pixel scale) in angstrom/pixel
disp = (l3 - l1) / (x3 - x1)

# Calculate observed-frame wavelength of emission line
lobs = l1 + (x2 - x1) * disp

# Calculate redshift
z = lobs/l2 - 1.

# Print
print ("disp = ", disp, "lobs = ", lobs, "z = ", z)

end
