import numpy as np
import matplotlib.pyplot as plt

# Ultra-simple example: 1D input -> 3 hidden neurons -> 1 output
def tiny_network(x):
    """
    Manually designed network to make piecewise linearity obvious
    """
    # Hidden layer: 3 neurons with ReLU
    h1 = np.maximum(0, x + 1)    # Activates when x > -1
    h2 = np.maximum(0, x)         # Activates when x > 0
    h3 = np.maximum(0, x - 1)     # Activates when x > 1
    
    # Output: weighted sum
    # Using simple weights to make regions clear
    output = 0.5 * h1 - 1.0 * h2 + 0.5 * h3
    return output

# Generate data
x = np.linspace(-2, 2, 1000)
y = tiny_network(x)

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: The complete function
ax1 = axes[0, 0]
ax1.plot(x, y, linewidth=2.5, color='darkblue')
ax1.axvline(-1, color='red', linestyle='--', alpha=0.5, label='Neuron 1 activates')
ax1.axvline(0, color='green', linestyle='--', alpha=0.5, label='Neuron 2 activates')
ax1.axvline(1, color='purple', linestyle='--', alpha=0.5, label='Neuron 3 activates')
ax1.set_xlabel('Input (x)', fontsize=12)
ax1.set_ylabel('Output', fontsize=12)
ax1.set_title('Piecewise Linear Function\n(Notice the kinks at activation boundaries)', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Plot 2: Overlay the individual linear pieces
ax2 = axes[0, 1]
ax2.plot(x, y, linewidth=3, color='darkblue', label='Complete function')

# Highlight each linear region with different colors
regions = [
    (x < -1, 'Region 1:\nx < -1'),
    ((x >= -1) & (x < 0), 'Region 2:\n-1 ≤ x < 0'),
    ((x >= 0) & (x < 1), 'Region 3:\n0 ≤ x < 1'),
    (x >= 1, 'Region 4:\nx ≥ 1')
]

colors = ['red', 'green', 'blue', 'orange']
for (mask, label), color in zip(regions, colors):
    ax2.plot(x[mask], y[mask], 'o', markersize=3, alpha=0.6, color=color, label=label)

ax2.set_xlabel('Input (x)', fontsize=12)
ax2.set_ylabel('Output', fontsize=12)
ax2.set_title('Same Function: Different Linear Pieces Highlighted', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(loc='best', fontsize=9)

# Plot 3: Show slopes in each region
ax3 = axes[1, 0]

# Compute numerical derivative
dy_dx = np.gradient(y, x)
ax3.plot(x, dy_dx, linewidth=2, color='darkred')
ax3.axvline(-1, color='red', linestyle='--', alpha=0.5)
ax3.axvline(0, color='green', linestyle='--', alpha=0.5)
ax3.axvline(1, color='purple', linestyle='--', alpha=0.5)
ax3.set_xlabel('Input (x)', fontsize=12)
ax3.set_ylabel('Slope (dy/dx)', fontsize=12)
ax3.set_title('Derivative: Constant Within Each Region\n(Piecewise constant = original is piecewise linear)', 
              fontsize=13, fontweight='bold')
ax3.grid(True, alpha=0.3)

# Plot 4: Show second derivative (should be zero except at boundaries)
ax4 = axes[1, 1]
d2y_dx2 = np.gradient(dy_dx, x)
ax4.plot(x, d2y_dx2, linewidth=2, color='darkgreen')
ax4.axhline(0, color='black', linestyle='-', alpha=0.3)
ax4.axvline(-1, color='red', linestyle='--', alpha=0.5)
ax4.axvline(0, color='green', linestyle='--', alpha=0.5)
ax4.axvline(1, color='purple', linestyle='--', alpha=0.5)
ax4.set_xlabel('Input (x)', fontsize=12)
ax4.set_ylabel('Second Derivative (d²y/dx²)', fontsize=12)
ax4.set_title('Second Derivative: Zero Except at Kinks\n(Proof of piecewise linearity)', 
              fontsize=13, fontweight='bold')
ax4.grid(True, alpha=0.3)
ax4.set_ylim(-0.5, 0.5)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/simple_piecewise_linear.png', dpi=150, bbox_inches='tight')

# Print analytical slopes for each region
print("="*70)
print("ANALYTICAL VERIFICATION: Slopes in Each Linear Region")
print("="*70)
print("\nFor the network: output = 0.5*max(0,x+1) - 1.0*max(0,x) + 0.5*max(0,x-1)")
print("\nRegion-by-region analysis:\n")

print("Region 1 (x < -1):")
print("  All neurons off → output = 0")
print("  Slope = 0")

print("\nRegion 2 (-1 ≤ x < 0):")
print("  Only neuron 1 active → output = 0.5(x+1)")
print("  Slope = 0.5")

print("\nRegion 3 (0 ≤ x < 1):")
print("  Neurons 1,2 active → output = 0.5(x+1) - 1.0(x) = -0.5x + 0.5")
print("  Slope = -0.5")

print("\nRegion 4 (x ≥ 1):")
print("  All neurons active → output = 0.5(x+1) - 1.0(x) + 0.5(x-1)")
print("  Simplifies to: 0")
print("  Slope = 0")

# Verify numerically
print("\n" + "="*70)
print("NUMERICAL VERIFICATION")
print("="*70)

test_points = [
    (-1.5, "Region 1"),
    (-0.5, "Region 2"),
    (0.5, "Region 3"),
    (1.5, "Region 4")
]

for x_test, region in test_points:
    # Compute numerical slope
    epsilon = 1e-6
    y1 = tiny_network(x_test)
    y2 = tiny_network(x_test + epsilon)
    numerical_slope = (y2 - y1) / epsilon
    print(f"\n{region} (x={x_test}):")
    print(f"  Numerical slope: {numerical_slope:.6f}")

print("\n" + "="*70)
print("\n✓ Within each region, the function is perfectly linear!")
print("✓ The overall function is a composition of linear pieces!")
print("\nThis is the fundamental geometric structure of ReLU networks.")
