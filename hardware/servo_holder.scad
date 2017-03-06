length = 23.5+0.5;
width = 12.5+0.5;
height = 10;
wall_thickness = 1.5;
base_thickness = 1.0;
hole_width = 3.2;
notch_width = 4.5;
notch_height = 4.0;
$fn=100;

difference() {
    cube([length+wall_thickness*2,width+wall_thickness*2,height], center=true);
    translate([0,0,base_thickness]) cube([length,width,height],center=true);
    translate([4,0,0]) cylinder(h=height*2,d=hole_width, center=true);
    translate([4,0,base_thickness+notch_height]) cube([length,notch_width,height], center=true);
}