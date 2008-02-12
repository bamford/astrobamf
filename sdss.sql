GO
DROP FUNCTION asinh
DROP FUNCTION sinh
DROP FUNCTION cosh
DROP FUNCTION asinh_mag_from_flux
DROP FUNCTION asinh_magerr_from_flux
DROP FUNCTION flux_from_asinh_mag
DROP FUNCTION fluxerr_from_asinh_mag
DROP FUNCTION calc_cmodel
DROP FUNCTION calc_cmodelerr

GO
CREATE FUNCTION asinh
(@z float )
RETURNS float
AS
BEGIN
    RETURN (log(@z + sqrt(1+@z*@z)))
END

GO
CREATE FUNCTION sinh
(@z float )
RETURNS float
AS
BEGIN
    RETURN (0.5*(exp(@z) - exp(-@z)))
END

GO
CREATE FUNCTION cosh
(@z float )
RETURNS float
AS
BEGIN
    RETURN (0.5*(exp(@z) + exp(-@z)))
END

GO
CREATE FUNCTION asinh_mag_from_flux
(@f float, @b float)
RETURNS float
AS
BEGIN
    RETURN (-1.08573620*(dbo.asinh(0.5*@f/@b) + log(@b)))
END

GO
CREATE FUNCTION asinh_magerr_from_flux
(@ferr float, @f float, @b float)
RETURNS float
AS
BEGIN
    RETURN abs(-1.08573620*@ferr/(@b*sqrt(4 + (@f*@f)/(@b*@b))))
END

GO
CREATE FUNCTION flux_from_asinh_mag
(@mag float, @b float)
RETURNS float
AS
BEGIN
    RETURN (dbo.sinh(-0.92103404*@mag - log(@b))*2*@b)
END

GO
CREATE FUNCTION fluxerr_from_asinh_mag
(@magerr float, @mag float, @b float)
RETURNS float
AS
BEGIN
    RETURN abs(@magerr * dbo.cosh(-0.92103404*@mag - log(@b)) * (-1.84206807)*@b)
END

GO
CREATE FUNCTION calc_cmodel
(@deVMag float, @expMag float, @fracDev float, @b float)
RETURNS float
AS
BEGIN
    IF @devMag is null or @deVMag < -50.0 or @devMag > 50.0
    RETURN null;
    declare @fdeV float, @fexp float, @fcmodel float, @cmodelMag float
    set @fdeV = dbo.flux_from_asinh_mag(@devMag, @b)
    set @fexp = dbo.flux_from_asinh_mag(@expMag, @b)
    set @fcmodel = @fracDev * @fdeV + (1-@fracDev) * @fexp
    set @cmodelMag = dbo.asinh_mag_from_flux(@fcmodel, @b)
    RETURN (@cmodelMag)
END

GO
CREATE FUNCTION calc_cmodelerr
(@deVMagErr float, @expMagErr float, @deVMag float, @expMag float,
@fracDev float, @b float)
RETURNS float
AS
BEGIN
    IF @devMag is null or @deVMag < -50.0 or @devMag > 50.0
    RETURN null;
    declare @fdeVErr float, @fexpErr float, @fcmodelErr float
    declare @fdeV float, @fexp float, @fcmodel float
    declare @cmodelMagErr float
    set @fdeVErr = dbo.fluxerr_from_asinh_mag(@devMagErr, @devMag, @b)
    set @fexpErr = dbo.fluxerr_from_asinh_mag(@expMagErr, @expMag, @b)
    set @fcmodelErr = sqrt(power(@fracDev * @fdeVErr, 2) + power((1-@fracDev) * @fexpErr, 2))
    set @fdeV = dbo.flux_from_asinh_mag(@devMag, @b)
    set @fexp = dbo.flux_from_asinh_mag(@expMag, @b)
    set @fcmodel = @fracDev * @fdeV + (1-@fracDev) * @fexp
    set @cmodelMagErr = dbo.asinh_magerr_from_flux(@fcmodelErr, @fcmodel, @b)
    RETURN (@cmodelMagErr)
END
