import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import json
import os


def load_json(filename):
    """Load data from a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)


def generate_timeline(approaches_file='approaches.json',
                      milestones_file='milestones.json',
                      config_file='config.json',
                      output_dir='output'):
    """
    Generate a timeline visualization of software integration approaches.

    Parameters:
    -----------
    approaches_file : str
        Path to the JSON file containing integration approaches data
    milestones_file : str
        Path to the JSON file containing milestone data
    config_file : str
        Path to the JSON file containing configuration settings
    output_dir : str
        Directory where the output image will be saved
    """
    # Load data
    approaches = load_json(approaches_file)
    milestones = load_json(milestones_file)
    config = load_json(config_file)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Set up the figure and axis with plenty of room at bottom
    fig, ax = plt.subplots(figsize=config.get('figsize', [15, 8]))

    # Draw the timeline segments
    for i, approach in enumerate(approaches):
        width = approach["end"] - approach["start"]
        rect = Rectangle((approach["start"], i-0.4), width, 0.8,
                         edgecolor='black', facecolor=approach["color"])
        ax.add_patch(rect)

        # Add short text in the middle of each timeline segment
        ax.text(approach["start"] + width/2, i, approach["name"],
                ha='center', va='center', fontweight='bold', fontsize=9,
                bbox=dict(facecolor='white', alpha=0.7, pad=2, edgecolor='none'))

    # Set the axis limits
    ax.set_xlim(config.get('xlim', [1955, 2030]))
    ax.set_ylim(-1, len(approaches))

    # Set the y-axis labels
    ax.set_yticks([])  # Remove default ticks
    ax.set_xticks(np.arange(config['xlim'][0] + 5,
                  config['xlim'][1], config.get('xticks', 10)))

    # Add key milestones as vertical lines
    for milestone in milestones:
        ax.axvline(x=milestone["year"], color='red', linestyle='--', alpha=0.7)
        # Use right alignment for early years to prevent overlap
        if milestone["year"] < 2005:
            ax.text(milestone["year"] + 0.2, 6.0, milestone["label"],
                    rotation=90, ha='left', fontsize=8, va='bottom')
        else:
            ax.text(milestone["year"]+0.2, -0.8, milestone["label"],
                    rotation=90, ha='left', fontsize=8)

    # Add titles and labels
    ax.set_title(config.get(
        'title', 'Evolution of Software System Integration Approaches'), fontsize=16, pad=20)
    ax.set_xlabel('Year', fontsize=12)
    fig.text(0.02, 0.5, 'Integration Approaches',
             va='center', rotation='vertical', fontsize=12)

    # Add a grid on the x-axis only
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # Create legend patches
    handles = []
    labels = []
    for approach in approaches:
        patch = Rectangle((0, 0), 1, 1, color=approach["color"])
        handles.append(patch)
        labels.append(approach["desc"])

    # Place legend at the bottom, outside the plot
    ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15),
              ncol=2, fontsize=9)

    # Add the note as horizontal text at the bottom
    fig.text(0.5, 0.02, config.get('note', ''),
             ha="center", fontsize=10, style='italic')

    # Adjust layout to make room for note and legend at bottom
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.30)

    # Save the figure
    output_path = os.path.join(output_dir, config.get(
        'output_filename', 'timeline.png'))
    plt.savefig(output_path, dpi=config.get('dpi', 300), bbox_inches='tight')
    print(f"Timeline saved to {output_path}")

    return plt


def main():

    # Generate the timeline
    plt = generate_timeline(
        approaches_file="data/approaches.json",
        milestones_file="data/milestones.json",
        config_file="data/config.json",
        output_dir="output"
    )

    # Show the plot if running interactively
    plt.show()


if __name__ == "__main__":
    main()
