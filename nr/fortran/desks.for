      SUBROUTINE KS(KEY,N,KN)
      DIMENSION KEY(64),KN(48),ICD(56),IPC1(56),IPC2(48)
      DATA IPC1/57,49,41,33,25,17,9,1,58,50,42,34,26,18
     *  ,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15
     *  ,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4/
      DATA IPC2/14,17,11,24,1,5,3,28,15,6,21,10
     *  ,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55
     *  ,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32/
      IF(N.EQ.1)THEN
        DO 11 J=1,56
          ICD(J)=KEY(IPC1(J))
11      CONTINUE
      ENDIF
      IT=2
      IF(N.EQ.1.OR.N.EQ.2.OR.N.EQ.9.OR.N.EQ.16)IT=1
      DO 13 I=1,IT
        IC=ICD(1)
        ID=ICD(29)
        DO 12 J=1,27
          ICD(J)=ICD(J+1)
          ICD(J+28)=ICD(J+29)
12      CONTINUE
        ICD(28)=IC
        ICD(56)=ID
13    CONTINUE
      DO 14 J=1,48
        KN(J)=ICD(IPC2(J))
14    CONTINUE
      RETURN
      END
      
      SUBROUTINE CYFUN(IR,K,IOUT)
C Rev. 12/13/85
C PROFORT compatibility via breaking IS into 4 pieces
      DIMENSION IR(32),K(48),IOUT(32),IE(48),IET(48),IP(32)
     *  ,ITMP(32),IS(16,4,8),IBIN(4,16)
      DIMENSION ISH1(16,4,2),ISH2(16,4,2),ISH3(16,4,2),ISH4(16,4,2)
      EQUIVALENCE (IS(1,1,1),ISH1(1,1,1)),(IS(1,1,3),ISH2(1,1,1)),
     *   (IS(1,1,5),ISH3(1,1,1)),(IS(1,1,7),ISH4(1,1,1))
      DATA IET/32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13
     *  ,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24
     *  ,25,24,25,26,27,28,29,28,29,30,31,32,1/
      DATA IP/16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10
     *  ,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25/
      DATA ISH1 /14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7
     *  ,0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8
     *  ,4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0
     *  ,15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13
     *  ,15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10
     *  ,3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5
     *  ,0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15
     *  ,13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9/
      DATA ISH2 /10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8
     *  ,13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1
     *  ,13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7
     *  ,1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12
     *  ,7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15
     *  ,13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9
     *  ,10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4
     *  ,3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14/
      DATA ISH3 /2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9
     *  ,14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6
     *  ,4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14
     *  ,11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3
     *  ,12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11
     *  ,10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8
     *  ,9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6
     *  ,4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13/
      DATA ISH4 /4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1
     *  ,13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6
     *  ,1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2
     *  ,6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12
     *  ,13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7
     *  ,1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2
     *  ,7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8
     *  ,2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11/
      DATA IBIN/0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,1
     *  ,0,1,0,0,0,1,0,1,0,1,1,0,0,1,1,1,1,0,0,0,1,0,0,1
     *  ,1,0,1,0,1,0,1,1,1,1,0,0,1,1,0,1,1,1,1,0,1,1,1,1/
      DO 15 J=1,48
        IE(J)=IAND(IR(IET(J))+K(J),1)
C       IE(J)=MOD(MOD(IR(IET(J))+K(J),2)+2,2)
15    CONTINUE
      DO 17 JJ=1,8
        J=6*JJ-5
        IROW=IOR(IE(J+5),ISHFT(IE(J),1))
        ICOL=IOR(IE(J+4),ISHFT(IOR(IE(J+3),ISHFT(IOR(IE(J+2),
     *      ISHFT(IE(J+1),1)),1)),1))
C       IROW=2*IE(J)+IE(J+5)
C       ICOL=8*IE(J+1)+4*IE(J+2)+2*IE(J+3)+IE(J+4)
        ISS=IS(ICOL+1,IROW+1,JJ)
        KK=4*(JJ-1)
        DO 16 KI=1,4
          ITMP(KK+KI)=IBIN(KI,ISS+1)
16      CONTINUE
17    CONTINUE
      DO 18 J=1,32
        IOUT(J)=ITMP(IP(J))
18    CONTINUE
      RETURN
      END