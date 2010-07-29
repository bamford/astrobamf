      FUNCTION IRBIT1(ISEED)
      LOGICAL NEWBIT
      PARAMETER (IB1=1,IB2=2,IB5=16,IB18=131072)
      NEWBIT=IAND(ISEED,IB18).NE.0
      IF(IAND(ISEED,IB5).NE.0)NEWBIT=.NOT.NEWBIT
      IF(IAND(ISEED,IB2).NE.0)NEWBIT=.NOT.NEWBIT
      IF(IAND(ISEED,IB1).NE.0)NEWBIT=.NOT.NEWBIT
      IRBIT1=0
      ISEED=IAND(ISHFT(ISEED,1),NOT(IB1))
      IF(NEWBIT)THEN
        IRBIT1=1
        ISEED=IOR(ISEED,IB1)
      ENDIF
      RETURN
      END