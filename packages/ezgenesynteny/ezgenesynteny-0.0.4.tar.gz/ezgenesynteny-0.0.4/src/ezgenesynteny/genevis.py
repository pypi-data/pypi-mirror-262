"""
File: genevis.py
Author: Jake Leyhr
GitHub: https://github.com/jakeleyhr/EZgenesynteny/
Date: March 2024
Description: Produce gene order plot and save to PDF file
"""
# Import dependencies
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def plot_genes(species_genes, title, format, upgenes):
    start_y=0.5
    y_increment=0.15

    fig, ax = plt.subplots()

    for species, genes_data in species_genes.items():
        genes = genes_data['genes']
        strand_directions = genes_data['strand_directions']
        gene_positions = genes_data['gene_positions']
        
        gene_positions = [pos + 0.5 for pos in gene_positions]
        
        for gene, strand, position in zip(genes, strand_directions, gene_positions):
            if position == upgenes + 1.5:
                width = len(gene)
                arrow = Polygon([(position*2 - 0.95, start_y - 0.05), 
                                 (position*2 + 0.6, start_y - 0.05), 
                                 (position*2 + 0.95, start_y), 
                                 (position*2 + 0.6, start_y + 0.05), 
                                 (position*2 - 0.95, start_y + 0.05)], 
                                 closed=True, edgecolor="black", facecolor="red", zorder=2)
            elif strand == "+":
                width = len(gene)
                arrow = Polygon([(position*2 - 0.95, start_y - 0.05), 
                                 (position*2 + 0.6, start_y - 0.05), 
                                 (position*2 + 0.95, start_y), 
                                 (position*2 + 0.6, start_y + 0.05), 
                                 (position*2 - 0.95, start_y + 0.05)], 
                                 closed=True, edgecolor="black", facecolor="gold", zorder=2)
            elif strand == "-":
                width = len(gene)
                arrow = Polygon([(position*2 + 0.95, start_y - 0.05), 
                                 (position*2 - 0.6, start_y - 0.05), 
                                 (position*2 - 0.95, start_y), 
                                 (position*2 - 0.6, start_y + 0.05), 
                                 (position*2 + 0.95, start_y + 0.05)], 
                                 closed=True, edgecolor="black", facecolor="deepskyblue", zorder=2)
            
            ax.add_patch(arrow)
            
            # Adjust fontsize
            if width > 9:
                fontsize = 12/(width/9)
            else:
                fontsize = 12
            ax.text(position*2, start_y - 0.002, gene, ha='center', va='center', fontsize=fontsize, zorder=3)

        # Add black line
        plt.hlines(y=start_y, xmin=1, xmax=max(gene_positions) * 2 + 2, color='black', linestyle='-', linewidth=1, zorder=1)

        # Add species names to the left side of the plot
        species_name = species
        speciesnamewidth = len(species_name)
        if speciesnamewidth > 9:
            speciesfontsize = 14/(speciesnamewidth/9)
        else:
            speciesfontsize = 14
        ax.text(0.1, start_y, species_name, ha='center', va='center', fontsize=speciesfontsize, zorder=3)

        # Advance increment
        start_y += y_increment

    largest_gene_positions = max(max(species_data["gene_positions"]) for species_data in species_genes.values()) + 0.5

    # Set plot limits and labels
    ax.set_xlim(0, 2*largest_gene_positions + 2)  # Each gene is 2 units wide
    ax.set_ylim(0.35, start_y)
    ax.set_aspect('auto')  # Remove equal aspect ratio
    ax.axis('off')

    # Set custom height and width for the saved image
    fig.set_size_inches(2*largest_gene_positions, 4*start_y)
    # Save the plot as pdf
    plt.savefig(f"{title}", format=format, bbox_inches='tight')

    #plt.show()

if __name__ == '__main__':
    plot_genes(species_genes, title, format, upgenes)