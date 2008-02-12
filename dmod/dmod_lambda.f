      PROGRAM DMOD_LAMBDA
c
c     Valid for Omega+lambda=1
C
      REAL*8 C,H0,OM0,Z,MU,DL,DC
C
      C=299792.50
 100  WRITE (6,1000)
      READ (5,*,END=200) H0,OM0,Z

c	do z=0.01,1.0,0.01
               DL=(1.+Z)*C/H0*DC(OM0,Z)
               MU=5.*LOG10(DL*1.E6)-5.
               WRITE (6,*) Z,DL,MU
c	end do
      GOTO 100
 200	STOP
 1000 FORMAT (' Ho, Omega, z?')
      END
C
      REAL*8 FUNCTION DC(OM0,Z)
      REAL*8 OM0,Z,DZ,Z1
      INTEGER I
C
      DZ=0.00001
      DC=0.0
C
      DO Z1=0.,Z,DZ
          DC=DC+1./SQRT(OM0)*DZ/SQRT((1.+Z1)**3.-1.+1./OM0)
      END DO
      END
