import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# Simple 2-layer neural network with ReLU activation
def simple_nn(x, W1, b1, W2, b2):
    """
    2-layer network: input -> hidden (ReLU) -> output (linear)
    """
    # First layer with ReLU
    h = np.maximum(0, x @ W1 + b1)  # ReLU activation
    # Output layer (linear)
    y = h @ W2 + b2
    return y

# Set random seed for reproducibility
np.random.seed(42)

# Network architecture: 2 inputs -> 4 hidden units -> 1 output
input_dim = 2
hidden_dim = 4
output_dim = 1

# Random weights
W1 = np.random.randn(input_dim, hidden_dim) * 0.5
b1 = np.random.randn(hidden_dim) * 0.5
W2 = np.random.randn(hidden_dim, output_dim) * 0.5
b2 = np.random.randn(output_dim) * 0.5

# Create a grid of input points
x1_range = np.linspace(-2, 2, 200)
x2_range = np.linspace(-2, 2, 200)
X1, X2 = np.meshgrid(x1_range, x2_range)

# Flatten for computation
X_flat = np.column_stack([X1.ravel(), X2.ravel()])

# Compute network output
Y_flat = simple_nn(X_flat, W1, b1, W2, b2)
Y = Y_flat.reshape(X1.shape)

# Create visualization
fig = plt.figure(figsize=(16, 5))

# 3D surface plot
ax1 = fig.add_subplot(131, projection='3d')
surf = ax1.plot_surface(X1, X2, Y, cmap=cm.viridis, alpha=0.8, 
                         linewidth=0, antialiased=True)
ax1.set_xlabel('x1')
ax1.set_ylabel('x2')
ax1.set_zlabel('Network Output')
ax1.set_title('3D View: Piecewise Linear Surface')
fig.colorbar(surf, ax=ax1, shrink=0.5)

# Contour plot to see linear regions
ax2 = fig.add_subplot(132)
contour = ax2.contour(X1, X2, Y, levels=20, cmap='viridis')
ax2.clabel(contour, inline=True, fontsize=8)
ax2.set_xlabel('x1')
ax2.set_ylabel('x2')
ax2.set_title('Contour Plot: Linear Regions Visible')
ax2.grid(True, alpha=0.3)

# Cross-section to see piecewise linearity clearly
ax3 = fig.add_subplot(133)
# Take a cross-section at x2 = 0
x2_fixed = 0
idx = np.argmin(np.abs(x2_range - x2_fixed))
cross_section = Y[idx, :]
ax3.plot(x1_range, cross_section, linewidth=2)
ax3.set_xlabel('x1')
ax3.set_ylabel('Network Output')
ax3.set_title(f'Cross-section at x2={x2_fixed}: Clearly Piecewise Linear')
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/piecewise_linear_demo.png', dpi=150, bbox_inches='tight')
print("Visualization saved!")

# Now let's verify piecewise linearity numerically
print("\n" + "="*60)
print("NUMERICAL VERIFICATION OF PIECEWISE LINEARITY")
print("="*60)

# Check that within a region, the function is perfectly linear
# We'll sample points along a line and check if second derivative is zero

def check_linearity_along_line(start, end, n_points=100):
    """Check if function is linear between two points"""
    # Generate points along the line
    t = np.linspace(0, 1, n_points)[:, np.newaxis]
    points = start + t * (end - start)
    
    # Evaluate network
    outputs = simple_nn(points, W1, b1, W2, b2).ravel()
    
    # Compute second differences (discrete second derivative)
    # If perfectly linear, all second differences should be ~0
    first_diff = np.diff(outputs)
    second_diff = np.diff(first_diff)
    
    max_second_diff = np.max(np.abs(second_diff))
    return max_second_diff, outputs

# Test several random line segments
print("\nTesting linearity along random line segments:")
print("(If max second difference ≈ 0, the function is linear in that region)\n")

for i in range(5):
    start = np.random.randn(2) * 2
    end = np.random.randn(2) * 2
    max_sd, _ = check_linearity_along_line(start, end)
    print(f"Line segment {i+1}: max |second difference| = {max_sd:.2e}")
    if max_sd < 1e-10:
        print(f"  → PIECEWISE LINEAR (within numerical precision)")
    else:
        print(f"  → Contains activation boundaries (switches between pieces)")

# Show activation patterns
print("\n" + "="*60)
print("ACTIVATION PATTERN ANALYSIS")
print("="*60)
print(f"Number of hidden units: {hidden_dim}")
print(f"Maximum possible linear regions: 2^{hidden_dim} = {2**hidden_dim}")
print("(Each unit can be 'on' or 'off', creating different linear regions)\n")

# Sample some points and show their activation patterns
sample_points = np.array([
    [-2, -2],
    [0, 0],
    [2, 2],
    [-1, 1],
    [1, -1]
])

print("Sample points and their hidden unit activation patterns:")
for point in sample_points:
    hidden = np.maximum(0, point @ W1 + b1)
    pattern = (hidden > 0).astype(int)
    output = simple_nn(point.reshape(1, -1), W1, b1, W2, b2)[0, 0]
    print(f"  {point}: activations={pattern} → output={output:.3f}")

print("\nEach different activation pattern corresponds to a different linear piece!")
