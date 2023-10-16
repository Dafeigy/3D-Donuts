use std::thread;
use std::time::Duration;

fn main() {
    const WIDTH: i32 = 32;
    const HEIGHT: i32= 32;
    const R1: f32 = 1.0;
    const R2: f32 = 2.0;
    const K2: f32 = 5.0;
    const K1: f32 = (WIDTH as f32 * K2 * 3.0)/( 8.0  * (R1+R2));
    let mut cos_a: f32 = 1.0;
    let mut cos_b: f32 = 1.0;
    let mut sin_a: f32 = 0.0;
    let mut sin_b: f32 = 0.0;

    println!("Hello, world!");
    loop{
        let mut zbuffer: [[f32; WIDTH as usize]; WIDTH as usize] = [[0.0; WIDTH as usize]; WIDTH as usize];
        let mut output: [[char; WIDTH as usize]; WIDTH as usize] = [[' '; WIDTH as usize]; WIDTH as usize];
        let mut sintheta: f32 = 0.0;
        let mut costheta: f32 = 1.0;

        for _j in 0..90{
            let mut sinphi: f32 = 0.0;
            let mut cosphi: f32 = 1.0;
            for _i in 0..324{
                let circlex: f32 = R1 * costheta + R2;
                let circley: f32 = R1 * sintheta;

                let x: f32 = circlex * (cos_b*cosphi + sin_a*sin_b*sinphi) - circley*cos_a*sin_b;
                let y: f32 = circlex*(sin_b*cosphi - sin_a*cos_b*sinphi) + circley*cos_a*cos_b;
                let ooz:f32 = 1.0/(K2 + cos_a*circlex*sinphi + circley*sin_a);

                
                let xp: i32 = ((WIDTH/2) as f32 + K1 * ooz * x) as i32;
                let yp: i32 = ((HEIGHT/2) as f32 -K1 * ooz * y) as i32;

                let l:f32 = cosphi*costheta*sin_b - cos_a*costheta*sinphi - sin_a*sintheta + cos_b*(cos_a*sintheta - costheta*sin_a*sinphi);
                
                if l > 0.0{
                    if ooz > zbuffer[xp as usize][yp as usize]{
                        zbuffer[xp as usize][yp as usize] = ooz;
                        output[xp as usize][yp as usize] = ".,-~:;=!*#$@".as_bytes()[(l * 8.0)as i32 as usize] as char;
                    }
                } 
                (cosphi,sinphi) = r(0.02, cosphi, sinphi);
            }
            (costheta,sintheta) = r(0.07, costheta, sintheta);
        }
        // Draw
        for ii in 0..HEIGHT{
            for jj in 0..HEIGHT{
                let a:char = output[ii as usize][jj as usize];
                print!("{} ",a);
            }
            println!()
        }
        (cos_a,sin_a) = r(0.08, cos_a, sin_a);
        (cos_b,sin_b) = r(0.03, cos_b, sin_b);
        thread::sleep(Duration::from_millis(20));
    }

}

fn r(t: f32 ,mut x: f32 , mut y: f32) -> (f32,f32){
    let mut _f: f32 = x;
    x = x - t * y;
    y = y + t * _f;
    _f = (3.0 - x * x - y * y)/2.0;
    x *= _f;
    y *= _f;
    return (x,y);
}