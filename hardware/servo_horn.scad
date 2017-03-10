wall_size = 1.5;
pcb_width = 26.0;
shaft_diameter = 5.0;
outer_shaft_diameter = shaft_diameter + wall_size * 2;
wing_offset = 3.5;
shaft_height = 3.0;
pcb_thickness = 1.5;
pcb_grip_size = 2.0;
total_height = shaft_height+wall_size;
grip_width = pcb_width+wall_size *2;

$fn = 100;
difference() {
    union() {
        hull() {
            cylinder(total_height, d=outer_shaft_diameter, center=true);
            translate([wing_offset+outer_shaft_diameter/2,0,0]) cube([wall_size, pcb_width-10, total_height], center=true);
        }
        translate([wing_offset+outer_shaft_diameter/2,0,0]) {
            cube([wall_size, pcb_width, total_height], center=true);
            translate([-wall_size/2,-pcb_width/2-wall_size,(-total_height/2)])          cube([wall_size*2+pcb_thickness, wall_size, total_height]);
            translate([wall_size/2+pcb_thickness, -pcb_width/2-wall_size,(-total_height/2)])          cube([wall_size, pcb_grip_size+wall_size, total_height]);
            
            translate([-wall_size/2,pcb_width/2,(-total_height/2)])          cube([wall_size*2+pcb_thickness, wall_size, total_height]);
            translate([wall_size/2+pcb_thickness, pcb_width/2-pcb_grip_size,(-total_height/2)])          cube([wall_size, pcb_grip_size+wall_size, total_height]);
            
            translate([-wall_size/2, -grip_width/2, total_height/2]) cube([wall_size*2+pcb_thickness, wall_size+ pcb_grip_size, wall_size/2]);
            translate([-wall_size/2, grip_width/2 - wall_size -pcb_grip_size, total_height/2]) cube([wall_size*2+pcb_thickness, wall_size+ pcb_grip_size, wall_size/2]);
        }
    };
    union () {
        cylinder(total_height+1, d=wall_size, center=true);
        translate([0,0,wall_size]) cylinder(total_height, d=shaft_diameter, center=true);
    };
};