import math
WIDTH =  40
HEIGHT = 40

R1 = 1  
R2 = 2

K2 = 5
K1 = (WIDTH*K2*3)/(8*(R1+R2))  


THETA_STEP = 0.07
PHI_STEP = 0.02

def render_frame(A, B,RTX_ON):
    zbuffer = [[0]*(WIDTH+0) for _ in range(HEIGHT+1)]
    output = [[' ']*(WIDTH+0) for _ in range(HEIGHT+1)]
 
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    theta = 0
    while theta < 2 * math.pi:
        theta += THETA_STEP
        
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        #circlex = R1 * (1+costheta) * costheta
        #circley = R1 * (1+costheta) * sintheta

        circlex = R2 + R1 * costheta
        circley = R1 * sintheta
        phi = 0
        while phi < math.pi * 2:
            phi += PHI_STEP
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)
            #原始代码把circlex、circley放到这里了，我觉得重复计算了移到外面了
            
            x = circlex*(cosB*cosphi + sinA*sinB*sinphi) - circley*cosA*sinB
            y = circlex*(sinB*cosphi - sinA*cosB*sinphi) + circley*cosA*cosB
            z = K2 + cosA*circlex*sinphi + circley*sinA

            ooz = 1/z

            xp = int(WIDTH/2 + K1 * ooz * x)
            yp = int(HEIGHT/2 - K1 * ooz * y)

            L = cosphi*costheta*sinB - cosA*costheta*sinphi - sinA*sintheta + cosB*(cosA*sintheta - costheta*sinA*sinphi)

            if L > 0:
                if ooz > zbuffer[xp][yp]:
                    zbuffer[xp][yp] = ooz
                    luminance_index = int(L*8)
                    output[xp][yp] = ".,-~:;=!*#$@"[luminance_index] if RTX_ON else '.'
                    

    print('\x1b[H')
    for i in range(HEIGHT):
        for j in range(WIDTH):
            print('\033[1;36m{}\033[0m'.format(output[i][j]),end=' ')
        print()

 
if __name__ == "__main__":
    A = 0.0  
    B = 0
    RTX_ON = True
    while True:
        render_frame(A, B, RTX_ON)
        A += 0.08
        B += 0.03         