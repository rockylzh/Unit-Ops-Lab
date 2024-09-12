#data import
load(".RData")
index <- FLowLoopDataWeek2[[1]]
dia <- FLowLoopDataWeek2[[2]]
flowrate <- FLowLoopDataWeek2[[3]]
pres1 <- FLowLoopDataWeek2[[4]]
pres2 <- FLowLoopDataWeek2[[5]]
pres3 <- FLowLoopDataWeek2[[6]]
pres4 <- FLowLoopDataWeek2[[7]]

#Constants
epsilon <- 0.0000025 # m
gamma_water <- 9800 # N/m^3
viscosity <- 0.001 # Pa*s
density <- 1000 # kg/m^3
ideal_value_globe <- 6.0
ideal_value_ball <- 0.05
ideal_value_f <- 0.02 #ideal friction factor from moody diagram

# Lengths in inches (convert to meters for calculations) 
length1 <- 1 * 0.0254 # inches to meters
length2 <- 1 * 0.0254 # inches to meters
length3 <- 1 * 0.0254 # inches to meters
length4 <- 1 * 0.0254 # inches to meters



