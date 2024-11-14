include <./Winkel.scad>

$fn = 50;


height = 165;
width  = 135;

curvature = 30;
radius = width / 2 - curvature;

thickness = 3;

module inner_homepod() {
    translate([0, 0, height / 2])
    color("#454545")
    minkowski() {
        cylinder(
            r = radius, 
            h = height - curvature * 2,
            center = true
        );
        
        sphere(r = curvature);
    }
}

module outer_homepod() {
    translate([0, 0, height / 2])
    color("#454545")
    minkowski() {
        cylinder(
            r = radius - thickness, 
            h = height - curvature * 2 - thickness,
            center = true
        );
        
        sphere(r = curvature);
    }
}

module homepod() {
    difference() {
        difference() {
            inner_homepod();
            
            outer_homepod();
        }
        
        translate([0, 0, height / 2])
        cylinder(
            r = radius,
            h = height + thickness * 3,
            center = true
        );
    }
}

module homepod_bottom() {
    difference() {
        difference() {
            group() {
                homepod();
                
                /*
                 * Add Supports
                 */
                
                // Power PCB
                intersection() {
                    inner_homepod();
                    
                    rotate([0, 0, -90])
                    translate([0, 50 + 15, 40])
                    rotate([-90, 0, 0])
                    cube([100, 90, 10], center = true);
                }
                
                // Sound Card PCB
                intersection() {
                    inner_homepod();
                    
                    rotate([0, 0, 90])
                    translate([0, 50 + 15, 40])
                    rotate([-90, 0, 0])
                    cube([100, 90, 10], center = true);
                }
                
                // Pi Support
                intersection() {
                    inner_homepod();
                    
                    translate([-3, 0, 0])
                    difference() {
                        winkel_breite = 60;
                        translate([15, 0, 0])
                        translate([-winkel_breite / 2, 70, 40])
                        rotate([0, 90, -90])
                        winkel(
                          seite_a = [50, 6, 1],
                          seite_b = [100, 0, 5],
                          breite  = winkel_breite,
                          dicke   = 5
                        );
                        
                        // USB-C Cutout
                        rotate([0, 0, 90])
                        translate([40, 25, 24])
                        cube([15, 300, 20], center = true);
                        
                        // USB-A Coutout
                        translate([15, 0, 28])
                        cube([50, 130, 20], center = true);
                    }
                }    
                
            }
            
            // micro
            translate([0, -width / 2 + 20, 20])
            rotate([110, 0, 0])
            cylinder(20, r = 3.5);
            
            // Charing port
            rotate([90, 0, 0])
            translate([0, 30, -width / 2])
            cylinder(20, r = 7);
            
            // Air ventilation
            for (x = [-2:6])
                rotate([0, -8, 360 / 10 * x + 15])
                translate([57 + thickness, 0, 0])
                cube([3, thickness * 3, 15]);
        }
        
        // Cut top 30 % off
        translate([0, 0, height - height * 0.2])
        cylinder(r = width / 2 - 1.5, h = height, center = true);
        
        translate([0, 0, height - height * 0.2])
        cylinder(r = width / 2 + 1.5, h = height - 5, center = true);
    }
}

//scale([1.01, 1.01, 1])
//homepod_bottom();
//scale([.99, .99, 1])
//homepod_bottom();


thickness = 5;

module top_half() {
    difference() {
        union() {
            homepod();
            
            // Ventilator wall
            intersection() {
                translate([0, 0, height / 2])
                minkowski() {
                    cylinder(
                        r = radius - thickness, 
                        h = height - curvature * 2 - thickness,
                        center = true
                    );
                    
                    sphere(r = curvature);
                }
                
                translate([-80, 0, 80])
                cube([50, 70, 70], center = true);
            }
            
            intersection() {
                translate([0, 0, height / 2])
                minkowski() {
                    cylinder(
                        r = radius - thickness, 
                        h = height - curvature * 2 - thickness,
                        center = true
                    );
                    
                    sphere(r = curvature);
                }
                
                translate([80, 0, 80])
                cube([50, 70, 70], center = true);
            }
        }
            
        // Cut bottom
        import_stl("Homepod_bottom_cutout.stl");
        cube([width, width, 100], center = true);
        
        // Cut top
        translate([0, 0, height])
        cube([width, width, 80], center = true);
        
        translate([0, 0, height + 30])
        cylinder(r = width / 2 - 1.5, h = height, center = true);    
        
        translate([-60, 0, 76])
        cube(40, center = true);
        
        
        // Camera
        translate([60, 0, 62])
        cube([15, 20, 5], center = true);
        
        translate([65, 0, 74])
        cube([5, 20, 20], center = true);
        
        // Cable channel
        translate([0, -(-width / 2 + thickness + 2), height / 2])
        cylinder(r = 5, h = height, center = true);
    }    
}

top_half();





