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
                /*
                intersection() {
                    inner_homepod();
                    
                    rotate([0, 0, -90])
                    translate([0, 50 + 15, 40])
                    rotate([-90, 0, 0])
                    cube([100, 90, 10], center = true);
                }
                */
                
                // Sound Card PCB
                intersection() {
                    inner_homepod();
                    
                    rotate([0, 0, 90])
                    translate([0, 50 + 15, 40])
                    rotate([-90, 0, 0])
                    cube([100, 90, 10], center = true);
                }
                
                
                // Pi Holder
                intersection() {
                    inner_homepod();
                    
                    translate([-14, -25, 38])
                    cube([56.3, 100, 3]);
                }
            }
            
            // micro
            translate([0, -width / 2 + 20, 20])
            rotate([110, 0, 0])
            cylinder(20, d = 7.53);
            
            // Charing port
            rotate([90, 0, 0])
            translate([0, 30, -width / 2])
            cylinder(20, r = 7);
            
            // Air ventilation
            for (x = [-2:6])
                rotate([0, -8, 360 / 10 * x + 15])
                translate([57 + thickness, 0, -5])
                cube([3, thickness * 3, 25]);
        }
        
        // Cut top 30 % off
        translate([0, 0, height - height * 0.2])
        cylinder(r = width / 2 - 1.5, h = height, center = true);
        
        translate([0, 0, height - height * 0.2])
        cylinder(r = width / 2 + 1.5, h = height - 5, center = true);
    }
}

thickness = 3;

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
        //import_stl("Homepod_bottom.stl");
      
        homepod_bottom();
        
        cube([width, width, 100], center = true);
        
        // Cut top
        translate([0, 0, height])
        cube([width, width, 80], center = true);
        
        translate([0, 0, height + 30])
        cylinder(r = width / 2 - 1.5, h = height, center = true);    
        
        
        translate([70, 0, height - 60])
        cube([10, 7, 50], center = true);
        
        translate([70, 0, height - 63])
        rotate([0, 20, 0])
        cube([10, 7, 120], center = true);
        
        for (y = [0:2])
            translate([0, 0, 105 + y * 5])
            for (x = [1,2,3,6,7,8])
                rotate([0, 0, 360 / 10 * x + 15])
                translate([50 + thickness, 0, -50])
                rotate([0, 40, 0])
                cube([5, thickness * 3, 50]);
    }    
}


// homepod_bottom();

top_half();





