import numpy as np 
import pvlib 

tmy3_data, tmy3_metadata = pvlib.iotools.read_tmy3('722780TYA.CSV')
tmy3_data.index.name = 'Time'

loc = pvlib.location.Location.from_tmy(tmy3_metadata,tmy3_data);

surface_tilt = tmy3_metadata['latitude'];

if tmy3_metadata['longitude'] < 0:
	surface_azimuth = 180;
else:
	surface_azimuth = 0;

sun_position = pvlib.solarposition.get_solarposition(tmy3_data.index,loc.latitude,loc.longitude,loc.altitude,pressure=None,method='nrel_numpy',temperature=12)

POA = pvlib.irradiance.get_total_irradiance(surface_tilt,surface_azimuth,sun_position.zenith,sun_position.azimuth,dni=tmy3_data.DNI,ghi=tmy3_data.GHI,dhi=tmy3_data.DHI,dni_extra=tmy3_data.ETRN,airmass=None,albedo=tmy3_data.Alb,surface_type=None,model='isotropic',model_perez='allsitescomposite1990');



a = -2.81
b = -0.0455

expo = 2.71828182846**(a + b*tmy3_data.Wspd)

module_temp = np.multiply(POA.poa_global,expo) + tmy3_data.DryBulb;

poa_dummy = POA[['poa_global']]
print(poa_dummy.iloc[ 9 , 0 ])
print(module_temp[2])
"""poa_dummy['module_temp'] = module_temp
poa_dummy['ambient_temp'] = tmy3_data.DryBulb

poa_dummy.index = pd.DatetimeIndex(poa_dummy.index)
poa_dummy.index  =  poa_dummy.index + pd.DateOffset(year=2020)

poa_dummy['Date'] = poa_dummy.index.date
poa_dummy['Month'] = poa_dummy.index.month 


#print(poa_dummy)

max_ambient = tmy3_data.DryBulb.max();
max_module = poa_dummy['module_temp'].max();

print('Maximum Module Temperature is ',max_module,' Degree Celsius')

max_index = poa_dummy[['module_temp']].idxmax()
print(max_index)

print(poa_dummy)

poa_energy = poa_dummy[poa_dummy['poa_global']>0]
poa_energy.index = range(4609);

print(poa_energy.sum(axis = 0, skipna = True))


print(poa_energy);


poa_energy.to_csv('poa.csv', sep='\t',encoding ='utf-8',header=True)

# print(poa_dummy.iat[max_index], ' POA at maximum Module Temp')

# print(poa_dummy.get_value(max_index,'poa_global'), ' Ambient Temperature at maximum Module Temp')

ax1 = poa_energy.plot.scatter(x='poa_global',y='module_temp',c='DarkBlue')

plt.show();"""




