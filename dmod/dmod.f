      PROGRAM DMOD
C
      REAL*8 C,H0,Q0,QQ0,Z,MU,DL
C
      C=299792.50
 100  WRITE (6,1000)
      READ (5,*,END=200) H0,Q0,Z
               QQ0=ABS(Q0)
               DL=C/H0/Q0/Q0*(Q0*Z+(Q0-1.)*(SQRT(1.+2.*Q0*Z)-1.))
               MU=5.*LOG10(DL*1.E6)-5.
               WRITE (6,*) Z,MU
      GOTO 100
 200	STOP
 1000 FORMAT (' Ho, qo, z?')
      END
