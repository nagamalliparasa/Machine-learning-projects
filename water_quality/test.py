from water_quality.training import Training

tra=Training()

val=tra.train('water_quality/data/water_potability.csv')
print(val)