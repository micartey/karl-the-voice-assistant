module winkel( seite_a, seite_b, breite, dicke ) {

	module xloch_platte(groesse, l_dm, l_anz, randabstand) {
		
		difference(){

			cube(groesse);

			lochabstand = (groesse.x - randabstand) / (l_anz + 1);

            for (y = [-1,1])
                for (x = [1:l_anz])
                    translate ([
                        randabstand + x * lochabstand,
                        groesse.y / 2 + y * breite / 3,
                        -1
                    ]) cylinder( d = l_dm, h = groesse.z + 2, $fn=8);

		}		
	}

    diag   = sqrt( pow(seite_a[0], 2) + pow(seite_b[0], 2) );
    winkel = asin(seite_a[0] / diag);

    rotate( [0, drehen ? 90 + winkel : 0, 0] )
	difference() {

		union() {

			// Seite A
			xloch_platte(
				[seite_a[0], breite, dicke],
				seite_a[1],
				seite_a[2],
				dicke
			);

			// Seite B
		    translate([dicke,0,0])
		    rotate([0,-90,0])
			xloch_platte(
				[seite_b[0], breite, dicke],
				seite_b[1],
				seite_b[2],
				dicke
			);

			// Wangen
			cube( [seite_a[0], dicke, seite_b[0]] );

			translate( [0, breite-dicke, 0] )
			cube( [seite_a[0], dicke, seite_b[0]] );

		}

	  translate([seite_a[0],-1,0])
	  rotate([0,-(winkel),0])
	  cube([diag,breite+2,diag+2]);

	}

}