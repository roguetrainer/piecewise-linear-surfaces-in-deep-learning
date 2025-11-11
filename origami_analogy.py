import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a figure with multiple subplots
fig = plt.figure(figsize=(16, 12))

# ============================================================
# Panel 1: "Unfolded" - Linear input space (flat paper)
# ============================================================
ax1 = fig.add_subplot(2, 3, 1, projection='3d')
x = np.linspace(-2, 2, 50)
y = np.linspace(-2, 2, 50)
X, Y = np.meshgrid(x, y)
Z = 0 * X  # Flat plane

ax1.plot_surface(X, Y, Z, alpha=0.7, cmap='gray', edgecolor='none')
ax1.set_xlabel('x₁')
ax1.set_ylabel('x₂')
ax1.set_zlabel('output')
ax1.set_title('Stage 0: "Unfolded Paper"\nFlat Linear Space', fontweight='bold', fontsize=11)
ax1.view_init(elev=20, azim=45)
ax1.set_zlim(-3, 3)

# ============================================================
# Panel 2: One fold (one ReLU neuron)
# ============================================================
ax2 = fig.add_subplot(2, 3, 2, projection='3d')

def one_neuron(X, Y):
    """One ReLU creates one fold"""
    return np.maximum(0, X + Y)

Z2 = one_neuron(X, Y)
ax2.plot_surface(X, Y, Z2, alpha=0.8, cmap='viridis', edgecolor='none')

# Draw the crease line
crease_x = np.linspace(-2, 2, 100)
crease_y = -crease_x
crease_z = np.zeros_like(crease_x)
ax2.plot(crease_x, crease_y, crease_z, 'r-', linewidth=4, label='Crease (fold line)')

ax2.set_xlabel('x₁')
ax2.set_ylabel('x₂')
ax2.set_zlabel('output')
ax2.set_title('Stage 1: "One Fold"\nOne ReLU Neuron', fontweight='bold', fontsize=11)
ax2.view_init(elev=20, azim=45)
ax2.set_zlim(-3, 3)

# ============================================================
# Panel 3: Two folds (two ReLU neurons)
# ============================================================
ax3 = fig.add_subplot(2, 3, 3, projection='3d')

def two_neurons(X, Y):
    """Two ReLUs create two folds"""
    h1 = np.maximum(0, X + Y)
    h2 = np.maximum(0, X - Y)
    return 0.5 * h1 + 0.5 * h2

Z3 = two_neurons(X, Y)
ax3.plot_surface(X, Y, Z3, alpha=0.8, cmap='plasma', edgecolor='none')

ax3.set_xlabel('x₁')
ax3.set_ylabel('x₂')
ax3.set_zlabel('output')
ax3.set_title('Stage 2: "Two Folds"\nTwo ReLU Neurons', fontweight='bold', fontsize=11)
ax3.view_init(elev=20, azim=45)
ax3.set_zlim(-3, 3)

# ============================================================
# Panel 4: Complex origami (many folds)
# ============================================================
ax4 = fig.add_subplot(2, 3, 4, projection='3d')

def complex_network(X, Y):
    """Multiple ReLUs create complex folded structure"""
    np.random.seed(42)
    h1 = np.maximum(0, 0.8*X + 0.6*Y + 0.5)
    h2 = np.maximum(0, -0.7*X + 0.7*Y - 0.3)
    h3 = np.maximum(0, 0.5*X - 0.9*Y + 0.4)
    h4 = np.maximum(0, -0.6*X - 0.8*Y - 0.2)
    h5 = np.maximum(0, 0.9*X + 0.3*Y - 0.6)
    return 0.3*h1 - 0.4*h2 + 0.35*h3 - 0.25*h4 + 0.3*h5

Z4 = complex_network(X, Y)
ax4.plot_surface(X, Y, Z4, alpha=0.9, cmap='coolwarm', edgecolor='none')

ax4.set_xlabel('x₁')
ax4.set_ylabel('x₂')
ax4.set_zlabel('output')
ax4.set_title('Stage 3: "Complex Origami"\nMany ReLU Neurons', fontweight='bold', fontsize=11)
ax4.view_init(elev=20, azim=45)
ax4.set_zlim(-3, 3)

# ============================================================
# Panel 5: Crease pattern visualization (top view)
# ============================================================
ax5 = fig.add_subplot(2, 3, 5)

# Create a contour plot showing the "crease pattern"
Z_complex = complex_network(X, Y)
contour = ax5.contour(X, Y, Z_complex, levels=20, cmap='coolwarm', linewidths=2)
ax5.clabel(contour, inline=True, fontsize=8)

ax5.set_xlabel('x₁', fontweight='bold')
ax5.set_ylabel('x₂', fontweight='bold')
ax5.set_title('The "Crease Pattern"\n(Activation Boundaries)', fontweight='bold', fontsize=11)
ax5.grid(True, alpha=0.3)
ax5.set_aspect('equal')

# Add text annotation
ax5.text(0.5, 0.95, 'Each line is a fold\n(where neurons activate)', 
         transform=ax5.transAxes, ha='center', va='top',
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
         fontsize=9)

# ============================================================
# Panel 6: Cross-section showing the folds
# ============================================================
ax6 = fig.add_subplot(2, 3, 6)

x_line = np.linspace(-2, 2, 500)
y_fixed = 0.5

# Compute outputs along the line
X_line = np.column_stack([x_line, np.full_like(x_line, y_fixed)])
z_line = complex_network(x_line, y_fixed)

ax6.plot(x_line, z_line, linewidth=3, color='darkblue', label='Network Output')

# Mark the "folds" (kinks in the function)
# Find approximate locations of kinks by looking at derivative changes
dz = np.diff(z_line)
d2z = np.diff(dz)
kink_threshold = np.percentile(np.abs(d2z), 90)
kink_indices = np.where(np.abs(d2z) > kink_threshold)[0]

for idx in kink_indices[::5]:  # Show some of the folds
    if idx < len(x_line) - 2:
        ax6.axvline(x_line[idx], color='red', linestyle='--', alpha=0.3, linewidth=1)

ax6.set_xlabel('x₁', fontweight='bold')
ax6.set_ylabel('Network Output', fontweight='bold')
ax6.set_title('Cross-Section: The Folded Structure\n(Red lines = fold locations)', 
              fontweight='bold', fontsize=11)
ax6.grid(True, alpha=0.3)
ax6.legend()

# Add text annotation
ax6.text(0.5, 0.05, 'Like cutting through origami,\nwe see the folds!', 
         transform=ax6.transAxes, ha='center', va='bottom',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7),
         fontsize=9)

plt.suptitle('Neural Networks as Origami: Folding Space with ReLU Activations\n'\
             'Each ReLU neuron creates a "fold" in the function space', 
             fontsize=15, fontweight='bold', y=0.995)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/ai_as_origami.png', dpi=150, bbox_inches='tight')
print("✓ Origami visualization created!")

# ============================================================
# Create a comparison table
# ============================================================
print("\n" + "="*70)
print("ORIGAMI vs NEURAL NETWORKS: The Comparison")
print("="*70)

comparison = [
    ("Property", "Origami", "Neural Networks"),
    ("-"*20, "-"*20, "-"*30),
    ("Starting point", "Flat paper", "Linear input space"),
    ("Basic operation", "Fold along line", "ReLU activation (hyperplane)"),
    ("Crease type", "Straight lines", "Linear boundaries"),
    ("Complexity growth", "Exponential (2^n)", "Exponential (up to 2^n regions)"),
    ("No smooth curves", "Only folds, no curves", "Piecewise linear, not smooth"),
    ("Dimensionality", "2D → 3D", "n-D → m-D"),
    ("Reversibility", "Can unfold", "Can trace back through layers"),
    ("Final result", "Complex 3D shape", "Complex decision function"),
]

for row in comparison:
    print(f"{row[0]:<20} | {row[1]:<20} | {row[2]:<30}")

print("="*70)

# ============================================================
# Quantitative analysis
# ============================================================
print("\n" + "="*70)
print("QUANTITATIVE ANALYSIS: Counting Regions")
print("="*70)

print("\nWith N neurons/folds, maximum number of distinct regions:\n")
for n in [1, 2, 3, 4, 5, 10, 20, 100]:
    regions = 2**n
    print(f"  {n:3d} neurons/folds → up to {regions:,} regions")
    if n <= 5:
        print(f"      (Each region is a flat piece)")

print("\nThis exponential growth explains why deep networks are so powerful!")
print("More 'folds' = more expressive power")

print("\n" + "="*70)
print("KEY INSIGHTS")
print("="*70)
print("""
1. BOTH USE PIECEWISE LINEAR OPERATIONS
   - Origami: fold along straight lines
   - Neural nets: activate along hyperplanes

2. BOTH CREATE COMPLEXITY THROUGH COMPOSITION
   - Origami: multiple folds create complex shapes
   - Neural nets: multiple layers create complex functions

3. BOTH ARE "LOCALLY FLAT"
   - Origami: each face is flat paper
   - Neural nets: each region is linear

4. BOTH HAVE EXPONENTIAL EXPRESSIVITY
   - More folds = exponentially more possible configurations
   - More neurons = exponentially more linear regions

5. NEITHER USES SMOOTH CURVES
   - Origami: only creases, no curved folds
   - Neural nets: only kinks, no smooth transitions (with ReLU)

The analogy is not just poetic - it's mathematically precise!
""")
