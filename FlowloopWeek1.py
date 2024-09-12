import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Constants
epsilon = 0.0000025 # m
gamma_water = 9800 # N/m^3
viscosity = 0.001 # Pa*s
density = 1000 # kg/m^3
ideal_value_globe = 6.0
ideal_value_ball = 0.05
ideal_value_f = 0.02 #ideal friction factor from moody diagram

# Lengths in inches (convert to meters for calculations)
lengthstra = 96 * 0.0254 # inches to meters
lengthglobe = 96 * 0.0254 # inches to meters
lengthball = 89 * 0.0254 # inches to meters

# Load the CSV file into a pandas DataFrame
file_path = 'Unit Ops Lab/FlowLoopDataWeek1.csv'
df = pd.read_csv(file_path)

# Extract the relevant columns from the DataFrame and convert to NumPy arrays
index = df['Index'].to_numpy()
FlowRate = df['Flow Rate (gal/min)'].to_numpy()
dia = df['Diameter (inch)'].to_numpy()
Presstra = df['Pressure Stra (psi)'].to_numpy()
Presglobe = df['Pressure Globe (psi)'].to_numpy()
Presball = df['Pressure Ball (psi)'].to_numpy()

# Copy three index values for the three sets of data
index1 = np.copy(index)
index2 = np.copy(index)
index3 = np.copy(index)

# Diameters in inches (convert to meters for calculations)
dia = dia * 0.0254 # inches to meters

# Flow rates in gallons per minute (convert to cubic meters per second)
FlowRate = FlowRate * 6.30902e-5 # gal/min to m^3/s

# Pressures in inches of water (convert to pascals)
convert = 249.08891 # 1 inch of water = 249.08891 Pa
Presstra = Presstra * convert # inches of water to Pa
Presglobe = Presglobe * convert # inches of water to Pa
Presball = Presball * convert # inches of water to Pa


# Inner area of the pipes (circular cross-section) in m^2
InnerArea = np.pi * (dia / 2)**2

# Flow speeds in m/s
FlowSpeed = FlowRate / InnerArea
print("Flow Speed:", FlowSpeed)

# Remove outliers method
def remove_outliers(data, index):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    mask = (data >= lower_bound) & (data <= upper_bound)
    return data[mask], index[mask]

def STD_remove_outliers(data, index):
    mean = np.mean(data)
    std = np.std(data)
    threshold = 3 * std
    lower_bound = mean - threshold
    upper_bound = mean + threshold
    mask = (data >= lower_bound) & (data <= upper_bound)
    return data[mask], index[mask]

# Friction factor calculation (Darcy-Weisbach equation) for both sets
f = 2 * dia / ((lengthstra) * (FlowSpeed**2)*density)*Presstra

# Remove outliers and combine both sets
FrictionFactors, index1 = remove_outliers(f, index1)

#Print the combined results
Ave_value_f = np.average(FrictionFactors)


# Minor loss coefficients for globe and ball valves 
# Bernoulli equations - Head loss calculations for set 1
h_mg = (Presglobe / gamma_water) - f * (lengthglobe / dia)*((FlowSpeed**2)/( 2 * 9.8))
h_mb = (Presball / gamma_water) - f * (lengthball / dia)*((FlowSpeed**2)/( 2 * 9.8))

# Minor loss coefficients for globe and ball valves for both sets
kfg = h_mg * 2 * 9.8 / (FlowSpeed**2)
kfb = h_mb * 2 * 9.8 / (FlowSpeed**2)


# Combine results from sets and remove outliers
MinorLossCoefficient_globe, index2 = remove_outliers(kfg, index2)
MinorLossCoefficient_ball, index3 = remove_outliers(kfb, index3)
Average_globe = np.average(MinorLossCoefficient_globe)
Average_ball = np.average(MinorLossCoefficient_ball)

# Calculate relative errors
relative_error_f = np.abs((Ave_value_f - ideal_value_f) / ideal_value_f) * 100
relative_error_globe = np.abs((Average_globe - ideal_value_globe) / ideal_value_globe) * 100
relative_error_ball = np.abs((Average_ball - ideal_value_ball) / ideal_value_ball) * 100


#Print the combined results
print("Friction Factor:",Ave_value_f,"Relative Error: {:.2f}%".format(relative_error_f))
print("Minor Loss Coefficient - Globe Valve:", Average_globe,"Relative Error: {:.2f}%".format(relative_error_globe))
print("Minor Loss Coefficient - Ball Valve:", Average_ball,"Relative Error: {:.2f}%".format(relative_error_ball))


# Calculate Root Mean Squared Error (RMSE)
rmse_f = np.sqrt(np.mean((FrictionFactors - ideal_value_f)**2))
rmse_ball = np.sqrt(np.mean((MinorLossCoefficient_ball- ideal_value_ball)**2))
rmse_globe = np.sqrt(np.mean((MinorLossCoefficient_globe - ideal_value_globe)**2))
mean_f = np.mean(FrictionFactors)
mean_globe = np.mean(MinorLossCoefficient_globe)
mean_ball = np.mean(MinorLossCoefficient_ball)
rmse_f_relative = rmse_f *100/ mean_f
rmse_globe_relative = rmse_globe *100/ mean_globe
rmse_ball_relative = rmse_ball *100/ mean_ball
print("Relative RMSE - Friction Factor:{:.2f}%".format(rmse_f_relative))
print("Relative RMSE - Globe Valve:{:.2f}%".format(rmse_globe_relative))
print("Relative RMSE - Ball Valve:{:.2f}%".format(rmse_ball_relative))


# Plot for Friction Factors
plt.figure(figsize=(10, 6))
plt.scatter(index1, FrictionFactors, color='b')
plt.title('Scatter Plot of Friction Factors')
plt.axhline(y=ideal_value_f, color='k', linestyle='--', label='Ideal Value')
plt.axhline(y=np.average(FrictionFactors), color='magenta', linestyle='--', label='Average Value')
plt.xlabel('Sample Index')
plt.ylabel('Friction Factor')
plt.grid(True)
plt.legend()
plt.show()

# Plot for Minor Loss Coefficient - Globe Valve
plt.figure(figsize=(10, 6))
plt.scatter(index2, MinorLossCoefficient_globe, color='g')
plt.title('Scatter Plot of Minor Loss Coefficients - Globe Valve')
plt.axhline(y=ideal_value_globe, color='k', linestyle='--', label='Ideal Value')
plt.axhline(y=np.average(MinorLossCoefficient_globe), color='magenta', linestyle='--', label='Average Value')
plt.xlabel('Sample Index')
plt.ylabel('Minor Loss Coefficient (Globe Valve)')
plt.grid(True)
plt.legend()
plt.show()

# Plot for Minor Loss Coefficient - Ball Valve
plt.figure(figsize=(10, 6))
plt.scatter(index3, MinorLossCoefficient_ball, color='r')
plt.axhline(y=ideal_value_ball, color='k', linestyle='--', label='Ideal Value')
plt.axhline(y=np.average(MinorLossCoefficient_ball), color='magenta', linestyle='--', label='Average Value')
plt.title('Scatter Plot of Minor Loss Coefficients - Ball Valve')
plt.xlabel('Sample Index')
plt.ylabel('Minor Loss Coefficient (Ball Valve)')
plt.grid(True)
plt.legend()
plt.show()