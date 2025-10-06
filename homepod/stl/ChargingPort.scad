$fn = 50;

charging_wires = 1;
inner_radius = 5.5;
walls = 5.5;

difference() {
    cylinder(21, r = 7, center = true);

    translate([0, 0, -10])
    cylinder(21, r = inner_radius);

    translate([3, 0, 0])
    cube([charging_wires, 3.5, 22], center = true);

    translate([-3, 0, 0])
    cube([charging_wires, 3.5, 22], center = true);
    
    translate([0, 0, 5.4])
    cylinder(5.2, d = 12);
}

intersection() {
    translate([0, 0, -10])
    cylinder(9, r = inner_radius + 0.1);

    translate([0, walls, 0])
    cube([20, 2, 100], center = true);
}

intersection() {
    translate([0, 0, -10])
    cylinder(9, r = inner_radius + 0.1);

    translate([0, -walls, 0])
    cube([20, 2, 100], center = true);
}