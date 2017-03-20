//designed to fit JUICEBANK JB78

use <MCAD/boxes.scad>;
use <MCAD/metric_fastners.scad>;

wall = 2.5;
corner_radius = 5.0;
height = 21.2;
width = 62.9;
clearance = 0.2;
depth = 12.0;
button_depth = 1.3;
button_width = 5.0;
e=0.01;
screw_hole = 3.5;
nut_size = 3.5;
nut_depth = 2.4;
servo_holder_width = 16.0;
nora_holder_width = 56.0;
holder_base = 2.0;
rim = 3.0;
$fn=100;

back_support = true;

inner_shell = [width+clearance*2, height+clearance*2, depth];
outer_shell = inner_shell + [wall*2,wall*2,-e];
button_shell = [button_depth, button_width, depth];
button_offset = [(inner_shell[0]+button_depth)/2-e,0,0];
nut_offset = [0,inner_shell[1]/2-e,0];

module slot(width) {
    d = outer_shell[2];
    r = rim;
    w = width + r*2;
    base = [w,holder_base, d];
    translate([-base[0]/2,0,-base[2]/2]) {
        cube(base);
        translate([0,holder_base,0]) cube([r,r,d]);
        translate([w-r,holder_base,0]) cube([r,r,d]);
    }
}



difference() {
    union() {
        roundedBox(outer_shell, corner_radius+wall, true);
        translate([0,-outer_shell[1]/2,0]) rotate([0,0,180]) slot(nora_holder_width);
        if (back_support) {
            translate([0,outer_shell[1]/2,0]) slot(servo_holder_width);
        }
    }
    roundedBox(inner_shell, corner_radius, true);
    rotate([90,0,0]) cylinder(d=screw_hole, h=width, center=false);    
    translate(-nut_offset) rotate([90,0,0]) flat_nut(nut_size);
    if (back_support) {
        translate(nut_offset) rotate([-90,0,0]) flat_nut(nut_size);
        rotate([-90,0,0]) cylinder(d=screw_hole, h=width, center=false);
        translate(button_offset) cube(button_shell, center=true);
    }
}