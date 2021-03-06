      SUBROUTINE SVDCMP(A,M,N,MP,NP,W,V)
      PARAMETER (NMAX=100)
      DIMENSION A(MP,NP),W(NP),V(NP,NP),RV1(NMAX)
      G=0.0
      SCALE=0.0
      ANORM=0.0
      DO 25 I=1,N
        L=I+1
        RV1(I)=SCALE*G
        G=0.0
        S=0.0
        SCALE=0.0
        IF (I.LE.M) THEN
          DO 11 K=I,M
            SCALE=SCALE+ABS(A(K,I))
11        CONTINUE
          IF (SCALE.NE.0.0) THEN
            DO 12 K=I,M
              A(K,I)=A(K,I)/SCALE
              S=S+A(K,I)*A(K,I)
12          CONTINUE
   adi.for                                                                                             100664  061334  061324  00000004757 06321132532 012450  0                                                                                                    ustar 00stephan                         ck                              000000  000000                                                                                                                                                                               SUBROUTINE ADI(A,B,C,D,E,F,G,U,JMAX,K,ALPHA,BETA,EPS)
      IMPLICIT REAL*8(A-H,O-Z)
      PARAMETER(JJ=100,KK=6,NRR=32,MAXITS=100,ZERO=0.D0,TWO=2.D0,HALF=.5
     *D0)
      DIMENSION A(JMAX,JMAX),B(JMAX,JMAX),C(JMAX,JMAX),D(JMAX,JMAX),
     *    E(JMAX,JMAX),F(JMAX,JMAX),G(JMAX,JMAX),U(JMAX,JMAX),
     *    AA(JJ),BB(JJ),CC(JJ),RR(JJ),UU(JJ),PSI(JJ,JJ),
     *    ALPH(KK),BET(KK),R(NRR),S(NRR,KK)
      IF(JMAX.GT.JJ)PAUSE 'Increase JJ'
      IF(K.GT.KK-1)PAUSE 'Increase KK'
      K1=K+1
      NR=2**K
      ALPH(1)=ALPHA
      BET(1)=BETA
      DO 11 J=1,K
        ALPH(J+1)=SQRT(ALPH(J)*BET(J))
        BET(J+1)=HALF*(ALPH(J)+BET(J))
11    CONTINUE
      S(1,1)=SQRT(ALPH(K1)*BET(K1))
      DO 13 J=1,K
        AB=ALPH(K1-J)*BET(K1-J)
        DO 12 N=1,2**(J-1)
          DISC=SQRT(S(N,J)**2-AB)
          S(2*N,J+1)=S(N,J)+DISC
          S(2*N-1,J+1)=AB/S(2*N,J+1)
12      CONTINUE
13    CONTINUE
      DO 14 N=1,NR
        R(N)=S(N,K1)
14    CONTINUE
      ANORMG=ZERO
      DO 16 J=2,JMAX-1
        DO 15 L=2,JMAX-1
          ANORMG=ANORMG+ABS(G(J,L))
          PSI(J,L)=-D(J,L)*U(J,L-1)+(R(1)-E(J,L))*U(J,L)
     *        -F(J,L)*U(J,L+1)
15      CONTINUE
16    CONTINUE
      NITS=MAXITS/NR
      DO 27 KITS=1,NITS
        DO 24 N=1,NR
          IF(N.EQ.NR)THEN
            NEXT=1
          ELSE
            NEXT=N+1
          ENDIF
          RFACT=R(N)+R(NEXT)
          DO 19 L=2,JMAX-1
            DO 17 J=2,JMAX-1
              AA(J-1)=A(J,L)
              BB(J-1)=B(J,L)+R(N)
              CC(J-1)=C(J,L)
              RR(J-1)=PSI(J,L)-G(J,L)
17          CONTINUE
            CALL TRIDAG(AA,BB,CC,RR,UU,JMAX-2)
            DO 18 J=2,JMAX-1
              PSI(J,L)=-PSI(J,L)+TWO*R(N)*UU(J-1)
18          CONTINUE
19        CONTINUE
          DO 23 J=2,JMAX-1
            DO 21 L=2,JMAX-1
              AA(L-1)=D(J,L)
              BB(L-1)=E(J,L)+R(N)
              CC(L-1)=F(J,L)
              RR(L-1)=PSI(J,L)
21          CONTINUE
            CALL TRIDAG(AA,BB,CC,RR,UU,JMAX-2)
            DO 22 L=2,JMAX-1
              U(J,L)=UU(L-1)
              PSI(J,L)=-PSI(J,L)+RFACT*UU(L-1)
22          CONTINUE
23        CONTINUE
24      CONTINUE
        ANORM=ZERO
        DO 26 J=2,JMAX-1
          DO 25 L=2,JMAX-1
            RESID=A(J,L)*U(J-1,L)+(B(J,L)+E(J,L))*U(J,L)
     *          +C(J,L)*U(J+1,L)+D(J,L)*U(J,L-1)
     *          +F(J,L)*U(J,L+1)+G(J,L)
            ANORM=ANORM+ABS(RESID)
25        CONTINUE
26      CONTINUE
        IF(ANORM.LT.EPS*ANORMG)RETURN
27    CONTINUE
      PAUSE 'MAXITS exceeded'
      END
                 amoeba.for                                                                                          100664  061334  061324  00000004320 06321132532 013121  0                                                                                                    ustar 00stephan                         ck                              000000  000000                                                                                                                                                                               SUBROUTINE AMOEBA(P,Y,MP,NP,NDIM,FTOL,FUNK,ITER)
      PARAMETER (NMAX=20,ALPHA=1.0,BETA=0.5,GAMMA=2.0,ITMAX=500)
      DIMENSION P(MP,NP),Y(MP),PR(NMAX),PRR(NMAX),PBAR(NMAX)
      MPTS=NDIM+1
      ITER=0
1     ILO=1
      IF(Y(1).GT.Y(2))THEN
        IHI=1
        INHI=2
      ELSE
        IHI=2
        INHI=1
      ENDIF
      DO 11 I=1,MPTS
        IF(Y(I).LT.Y(ILO)) ILO=I
        IF(Y(I).GT.Y(IHI))THEN
          INHI=IHI
          IHI=I
        ELSE IF(Y(I).GT.Y(INHI))THEN
          IF(I.NE.IHI) INHI=I
        ENDIF
11    CONTINUE
      RTOL=2.*ABS(Y(IHI)-Y(ILO))/(ABS(Y(IHI))+ABS(Y(ILO)))
      IF(RTOL.LT.FTOL)RETURN
      IF(ITER.EQ.ITMAX) PAUSE 'Amoeba exceeding maximum iterations.'
      ITER=ITER+1
      DO 12 J=1,NDIM
        PBAR(J)=0.
12    CONTINUE
      DO 14 I=1,MPTS
        IF(I.NE.IHI)THEN
          DO 13 J=1,NDIM
            PBAR(J)=PBAR(J)+P(I,J)
13        CONTINUE
        ENDIF
14    CONTINUE
      DO 15 J=1,NDIM
        PBAR(J)=PBAR(J)/NDIM
        PR(J)=(1.+ALPHA)*PBAR(J)-ALPHA*P(IHI,J)
15    CONTINUE
      YPR=FUNK(PR)
      IF(YPR.LE.Y(ILO))THEN
        DO 16 J=1,NDIM
          PRR(J)=GAMMA*PR(J)+(1.-GAMMA)*PBAR(J)
16      CONTINUE
        YPRR=FUNK(PRR)
        IF(YPRR.LT.Y(ILO))THEN
          DO 17 J=1,NDIM
            P(IHI,J)=PRR(J)
17        CONTINUE
          Y(IHI)=YPRR
        ELSE
          DO 18 J=1,NDIM
            P(IHI,J)=PR(J)
18        CONTINU