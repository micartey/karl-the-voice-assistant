charging_wires = 1;
inner_radius = 5.5;
walls = 5.5;

difference() {
    cylinder(16, r = 7, center = true);

    translate([0, 0, -10])
    cylinder(16, r = inner_radius);

    translate([3, 0, 0])
    cube([charging_wires, 3.5, 17], center = true);

    translate([-3, 0, 0])
    cube([charging_wires, 3.5, 17], center = true);
}

intersection() {
    translate([0, 0, -3])
    cylinder(9, r = inner_radius);

    translate([0, walls, 0])
    cube([20, 2, 100], center = true);
}

intersection() {
    translate([0, 0, -3])
    cylinder(9, r = inner_radius);

    translate([0, -walls, 0])
    cube([20, 2, 100], center = true);
}