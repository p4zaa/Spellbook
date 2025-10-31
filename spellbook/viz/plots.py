import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from scipy.interpolate import make_interp_spline

def plot_data_over_time(
    x_data, y_data, group_labels=None, time_labels=None, figsize=(10, 6), smooth_line=False, 
    colors=None, x_label="Time", y_label="Value", title="Data Over Time", grid_alpha=0.3, 
    display_y_ticks=True, hspace=0.3, show_vertical_grid=True, show_horizontal_grid=True, 
    grid_color='gray', title_pos=(0.5, 0.95), y_label_pos=(0.95, 0.5), 
    display_peak_number_annotation=False,):
    """
    Plot line charts for each group over time with optional smoothing, customizable grid, and peak number annotation.

    Parameters:
    - x_data: List or NumPy array of x-axis values (e.g., time or months).
    - y_data: List or NumPy array of y-axis values (e.g., data points or measurements corresponding to x_data).
    - group_labels: List or NumPy array of labels (e.g., categories, groups, or entities) for each data point (optional).
    - time_labels: List or NumPy array of time points (e.g., months or time steps, should match x_data length).
    - smooth_line: Boolean to specify whether to plot a smooth line (default: False).
    - colors: List of colors for each group’s line and fill (default: None for automatic colors).
    - x_label: Label for the x-axis (default: "Time").
    - y_label: Label for the y-axis (default: "Value").
    - title: Title for the plot (default: "Data Over Time").
    - grid_alpha: Transparency of grid lines (default: 0.3).
    - display_y_ticks: Boolean to display y-ticks (default: True).
    - hspace: Vertical space between subplots (default: 0.3).
    - show_vertical_grid: Boolean to display vertical grid lines (default: True).
    - show_horizontal_grid: Boolean to display horizontal grid lines (default: True).
    - grid_color: Color of the grid lines (default: 'gray').
    - title_pos: Tuple (x, y) for title position (default: (0.5, 0.95)).
    - y_label_pos: Tuple (x, y) for y-axis label position (default: (0.95, 0.5)).
    - display_peak_number_annotation: Boolean to display the peak number annotation at the highest peak (default: False).

    Returns:
    - None
    """

    # If group_labels are provided, find unique groups
    if group_labels is not None:
        unique_groups = np.unique(group_labels)
    else:
        unique_groups = [""]  # Use a single group if none are provided

    # Create subplots with shared x-axis
    fig, axes = plt.subplots(len(unique_groups), 1, figsize=figsize, sharex=True)

    # If only one group, make axes a list to iterate
    if len(unique_groups) == 1:
        axes = [axes]

    # Set the color palette if none is provided
    if colors is None:
        colors = plt.cm.viridis(np.linspace(0, 1, len(unique_groups)))

    # Create a dictionary mapping each group to its color
    group_to_color = dict(zip(unique_groups, colors))

    # Find the min and max values of y_data across all groups to set y-axis limits
    min_y = min(y_data)
    max_y = max(y_data) + max(y_data) * 0.1 # Add 10% padding

    # Plot each group in a separate subplot
    for i, (ax, group) in enumerate(zip(axes, unique_groups)):
        # Filter data for the current group
        if group_labels is not None:
            group_x_data = np.array([x_data[i] for i in range(len(group_labels)) if group_labels[i] == group])
            group_y_data = np.array([y_data[i] for i in range(len(group_labels)) if group_labels[i] == group])
        else:
            group_x_data = np.array(x_data)
            group_y_data = np.array(y_data)

        # Sort by x_data (time labels)
        sorted_indices = np.argsort(group_x_data)
        group_x_data = group_x_data[sorted_indices]
        group_y_data = group_y_data[sorted_indices]

        # Get color for the current group
        color = group_to_color[group]

        if smooth_line:
            # Smooth the line using cubic spline interpolation
            spline = make_interp_spline(group_x_data, group_y_data, k=3, bc_type='clamped')
            smooth_x_data = np.linspace(group_x_data.min(), group_x_data.max(), 500)
            smooth_y_data = spline(smooth_x_data)

            # Fill the area under the smooth line
            ax.fill_between(smooth_x_data, smooth_y_data, color=color, alpha=0.4)
            ax.plot(smooth_x_data, smooth_y_data, label=group, color=color, lw=2)
        else:
            # Plot the raw data points and connect them with a line
            ax.fill_between(group_x_data, group_y_data, color=color, alpha=0.4)
            ax.plot(group_x_data, group_y_data, label=group, color=color, lw=2, marker='o')

        # Move y-axis label and ticks to the right
        ax.yaxis.set_label_position('right')

        # Control visibility of y-ticks and display them on the right side only
        if display_y_ticks:
            ax.tick_params(axis='y', right=True, labelright=True)  # Display y-ticks on the right
            ax.tick_params(axis='y', left=False, labelleft=False)  # Hide y-ticks on the left
        else:
            ax.tick_params(axis='y', labelleft=False, left=False)  # Hide y-ticks entirely

        # Add the group name to the left y-tick label
        ax.text(-0.02, 0, group, transform=ax.transAxes, va='center', ha='right', fontsize=12, weight='bold')

        # Set y-limits and grid
        ax.set_ylim(min_y, max_y)  # Set same y-axis scale for all subplots

        # Set grid lines for vertical and/or horizontal
        if show_vertical_grid:
            ax.grid(True, axis='x', alpha=grid_alpha, color=grid_color)
        if show_horizontal_grid:
            ax.grid(True, axis='y', alpha=grid_alpha, color=grid_color)

        # Hide top, left, and right spines (borders), except for the bottom one
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Set the background of each subplot to transparent
        ax.set_facecolor('none')  # Transparent background for each subplot

        # Annotate the highest peak
        max_y_value = np.max(group_y_data)
        max_y_index = np.argmax(group_y_data)
        max_x_value = group_x_data[max_y_index]

        if display_peak_number_annotation:
          ax.annotate(f'{max_y_value:.2f}',
                      xy=(max_x_value, max_y_value),
                      xytext=(max_x_value, max_y_value + 0),
                      textcoords='data',
                      arrowprops=dict(arrowstyle='simple', color=color),
                      fontsize=11, color=color, fontweight='bold')


    # Set common x-axis label and title
    axes[-1].set_xlabel(x_label)
    plt.xticks(time_labels, rotation=90)  # Ensure all time labels are displayed
    plt.suptitle(title, x=title_pos[0], y=title_pos[1], fontsize=14)

    # Add y_label at the custom position
    fig.text(y_label_pos[0], y_label_pos[1], y_label, va='center', ha='center', rotation=270, fontsize=10)

    # Adjust layout with hspace to control vertical spacing between subplots
    plt.subplots_adjust(hspace=hspace)

    # Show plot with transparent background for the figure
    fig.patch.set_facecolor('none')  # Set the figure background to transparent
    plt.show()

def plot_keyword_heatmap(timestamps, texts, target_keywords, fontpath=None, figsize=(10, 6), cmap='YlGnBu', time_tick='hour', hide_minute_text=False, title=None, axis_fontsize=12, max_y_scale=0):
    """
    Plot a heatmap showing the frequency of target keywords in texts at different times of day.
    
    Parameters:
    - timestamps: List of datetime objects representing when each comment was made.
    - texts: List of comment text data.
    - target_keywords: List of target keywords to track.
    - fontpath: Optional path to a custom font for labels (if None, default font is used).
    - figsize: Tuple specifying the size of the figure (default is (10, 6)).
    - cmap: String specifying the color map to use for the heatmap (default is 'YlGnBu').
    - time_tick: Option for time granularity: 'hour' for hourly intervals or 'hour_minute' for 10-minute intervals (default is 'hour').
    - hide_minute_text: Boolean to hide minute text (default is False).
    - title: Optional title for the heatmap.
    - axis_fontsize: Font size for axis labels and title.
    - max_y_scale: Maximum value for the heatmap color scale (0 for no limit).
    """
    # Extract the hour and minute from each timestamp (assuming timestamp is in datetime format)
    if time_tick == 'hour':
        time_values = [timestamp.hour for timestamp in timestamps]  # Extract hour from timestamp
        time_labels = [str(i) for i in range(10, 25)]  # Labels for hours 10-24
        ticks = 15  # 15 time intervals (for each hour from 10 to 24)
    elif time_tick == 'hour_minute':
        time_values = [timestamp.hour * 60 + timestamp.minute for timestamp in timestamps]  # Extract hour and minute
        time_labels = []
        for h in range(10, 25):
            for m in range(0, 60, 10):
                if m == 0:
                    time_labels.append(f'{h}:00')  # Show full hour for 00 minute
                else:
                    time_labels.append('' if hide_minute_text else f':{m:02}')  # Show only minute for other values
        ticks = len(time_labels)  # Calculate the number of 10-minute intervals from 10:00 to 24:00
    elif time_tick == 'day':
        time_values = [timestamp.weekday() for timestamp in timestamps]
        time_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        ticks = 7
    elif time_tick == 'date':
        unique_dates = sorted(list(set(ts.date() for ts in timestamps)))
        date_to_index = {date: i for i, date in enumerate(unique_dates)}
        time_values = [date_to_index.get(ts.date()) for ts in timestamps]
        time_labels = [d.strftime('%Y-%m-%d') for d in unique_dates]
        ticks = len(unique_dates)

    # Initialize a dictionary to store counts of keywords per time
    keyword_counts = {keyword: np.zeros(ticks) for keyword in target_keywords}

    # Count occurrences of each keyword for each time interval
    for idx, text in enumerate(texts):
        time_value = time_values[idx]
        if time_value is None:
            continue
        
        # Check for keyword presence in text
        for keyword in target_keywords:
            if keyword in text:
                if time_tick == 'hour':
                    if 10 <= time_value < 25:
                        keyword_counts[keyword][time_value - 10] += 1
                elif time_tick == 'hour_minute':
                    if time_value >= 10 * 60:
                        time_index = (time_value - (10 * 60)) // 10
                        if time_index < ticks:
                            keyword_counts[keyword][time_index] += 1
                elif time_tick in ['day', 'date']:
                    keyword_counts[keyword][time_value] += 1

    # Create the heatmap matrix
    heatmap_data = np.array([keyword_counts[keyword] for keyword in target_keywords])

    # Plotting
    fig, ax = plt.subplots(figsize=figsize)
    if max_y_scale and max_y_scale > 0:
        cax = ax.imshow(heatmap_data, aspect='auto', cmap=cmap, interpolation='nearest', vmin=0, vmax=max_y_scale)
    else:
        cax = ax.imshow(heatmap_data, aspect='auto', cmap=cmap, interpolation='nearest')
    
    ax.set_xticks(np.arange(ticks))
    ax.set_xticklabels(time_labels, rotation=90)

    ax.set_yticks(np.arange(len(target_keywords)))
    ax.set_yticklabels(target_keywords)
    
    if time_tick in ['hour', 'hour_minute']:
        xlabel = 'Time of Day'
    elif time_tick == 'day':
        xlabel = 'Day of the Week'
    else:
        xlabel = 'Date'
    ax.set_xlabel(xlabel, fontsize=axis_fontsize)
    ax.set_ylabel('Target Keywords', fontsize=axis_fontsize)
    
    
    if title:
        ax.set_title(title, fontsize=axis_fontsize)
    else:
        ax.set_title(f'Heatmap of Keyword Occurrences in Texts by {time_tick.capitalize()}', fontsize=axis_fontsize)

    # Apply custom font if provided
    if fontpath:
        labelpad = 20
        prop = font_manager.FontProperties(fname=fontpath, size=axis_fontsize)
        ax.set_xlabel(xlabel, fontproperties=prop, fontsize=axis_fontsize, labelpad=labelpad)
        ax.set_ylabel('Target Keywords', fontproperties=prop, fontsize=axis_fontsize, labelpad=labelpad)
        if title:
            ax.set_title(title, fontproperties=prop, fontsize=axis_fontsize, pad=30)
        else:
            ax.set_title(f'Heatmap of Keyword Occurrences in Texts by {time_tick.capitalize()}', fontproperties=prop, fontsize=axis_fontsize, pad=30)
        
        for tick in ax.get_xticklabels():
            tick.set_fontproperties(prop)
        for tick in ax.get_yticklabels():
            tick.set_fontproperties(prop)

    # Adjust the font properties for bold hour labels and smaller minute labels
    for tick in ax.get_xticklabels():
        if ':00' in tick.get_text():  # Check if it's an hour
            tick.set_fontweight('bold')  # Make the hour labels bold
            tick.set_fontsize(axis_fontsize - 2)
        else:
            tick.set_fontsize(axis_fontsize - 4)  # Make minute labels smaller

    cbar = fig.colorbar(cax, pad=0.02)
    cbar.set_label('Frequency', fontsize=axis_fontsize//2)
    cbar.ax.tick_params(labelsize=axis_fontsize//2)
    
    plt.tight_layout()
    plt.grid(color='darkgrey', alpha=0.1, linestyle='--')
    plt.show()