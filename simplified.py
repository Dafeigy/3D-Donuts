WIDTH =  40
HEIGHT = 40

R1 = 1  
R2 = 2

K2 = 5
K1 = (WIDTH*K2*3)/(8*(R1+R2))  

cosA,cosB = 1.0, 1.0
sinA,sinB = 0.0, 0.0

def R(t,x,y):
    f = x
    x -= t * y
    y += t * f
    f = (3- x*x - y*y)/2
    x *= f
    y *= f
    return x,y

if __name__ == "__main__":
    while True:
        zbuffer = [[0]*(WIDTH+0) for _ in range(HEIGHT+1)]
        output = [[' ']*(WIDTH+0) for _ in range(HEIGHT+1)]
        sintheta = 0
        costheta = 1

        for j in range(90):
            sinphi = 0
            cosphi = 1

            for i in range(324):
                circlex = R1 * costheta + R2
                circley = R1 * sintheta

                x = circlex*(cosB*cosphi + sinA*sinB*sinphi) - circley*cosA*sinB
                y = circlex*(sinB*cosphi - sinA*cosB*sinphi) + circley*cosA*cosB
                ooz = 1/(K2 + cosA*circlex*sinphi + circley*sinA)

                xp = int(WIDTH/2 + K1 * ooz * x)
                yp = int(HEIGHT/2 - K1 * ooz * y)

                L = cosphi*costheta*sinB - cosA*costheta*sinphi - sinA*sintheta + cosB*(cosA*sintheta - costheta*sinA*sinphi)
                
                if L > 0:
                    if ooz > zbuffer[xp][yp]:
                        zbuffer[xp][yp] = ooz
                        output[xp][yp] = ".,-~:;=!*#$@"[int(L*8)]
                cosphi,sinphi = R(0.02,cosphi,sinphi)
            costheta,sintheta = R(0.07,costheta,sintheta)

        for ii in range(HEIGHT):
            for jj in range(WIDTH):
                print(output[ii][jj],end=' ')
            print()

        cosA,sinA = R(0.08,cosA,sinA)
        cosB,sinB = R(0.03,cosB,sinB)

        
