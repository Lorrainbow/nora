base = 2.5;
length = 25.0;
width = 7.0;
height = 15.0;
wall = 2.5;



channel = [length, width, height];
shell = channel+[wall-0.1, wall*2, base-0.1];
channel_offset = [-width/2, -width/2, 0];
shell_offset = channel_offset - [wall, wall, base];

module outer() {
    translate(shell_offset) {
        difference() {
            cube(shell);
        }
    }
}

module inner() {
    translate(channel_offset) {
        cube(channel-[wall,0,0]);
        translate([0,0,height/2]) 
            cube(channel);
    }
}


module rotater(angles) {
    for (a = angles) {
        rotate([0,0,a]) children(0);
    }    
}

module create(angles) {
    difference() {
        hull() rotater(angles) outer();
        cylinder(h=height*2, r=length*2);
    }    
    difference() {
        rotater(angles) outer();
        rotater(angles) inner();
    }
}

//L-shape
//create([0, 90]);
//T-shape
create([0,90,180]);
//I-shape
//create([0,180]);