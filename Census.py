from census import Census
from us import states
cvname = {'B01003_001E':'TotPop'}

nametup = tuple([v for v in cvname.keys()])


# Easily get API key here: https://api.census.gov/data/key_signup.html
c = Census("ed40f8afbcd5fd0a7547b40e597b82b574925de5")

cty = 1
out = c.acs5.get(nametup,{'for':'block group:*','in':'state:{} county:{:03} tract:*'.format(
                                                                            states.CA.fips,cty)})

out2 = c.acs5.get(nametup,{'for':'tract:*','in':'state:{} county:{:03}'.format(
                                                                            states.CA.fips,cty)})
print(out)