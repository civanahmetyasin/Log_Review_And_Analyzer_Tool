# categorical.py - Enhanced non-numeric data handling module

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import Counter
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QLabel
from PyQt6 import QtGui
import re


def handle_non_numeric_data(window_obj, lines, column, lineName, slipLineCharacter):
    """
    Handle non-numeric data by detecting type and creating appropriate visualization
    Enhanced version with PyQt6 integration
    """
    
    # print("handle_non_numeric_data fonksiyonuna girildi")
    raw_data = []
    
    # Extract raw data (normalize NaN-like values to "N/A")
    for i in range(1, len(lines)):  # Skip header
        try:
            cell_data = lines[i].split(slipLineCharacter)[column].strip()
            
            # Convert to string and normalize
            cell_str = str(cell_data).strip()
            
            # Ultra comprehensive check for empty or NaN-like values
            if (not cell_str or 
                len(cell_str) == 0 or
                cell_str.isspace() or
                cell_str in ['', ' ', '  ', 'None', 'none', 'NONE', 'null', 'NULL', 'Null'] or
                re.match(r'^n\s*a\s*n?$', cell_str, re.IGNORECASE) or  # nan, n/a, na patterns
                re.match(r'^n\s*/\s*a$', cell_str, re.IGNORECASE) or   # n/a with spaces
                cell_str.replace(' ', '').lower() in ['nan', 'na', 'n/a', 'null', 'none', 'nil', 'empty'] or
                cell_str.replace(' ', '').upper() in ['NAN', 'NA', 'N/A', 'NULL', 'NONE', 'NIL', 'EMPTY'] or
                cell_str in ['-', '--', '---', '....', '???', 'undefined', 'UNDEFINED']):
                raw_data.append("N/A")
            else:
                # Ensure it's properly converted to string
                raw_data.append(str(cell_str))
        except Exception as e:
            raw_data.append("N/A")  # Add N/A for parsing errors too
    
    if len(raw_data) == 0:
        # print("No valid data found")
        return False

    # Detect data type (exclude N/A values from date detection)
    date_count = 0
    text_count = 0
    sample_size = min(50, len(raw_data))

    date_patterns = [
        '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d',
        '%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M',
        '%d.%m.%Y', '%d-%m-%Y',
        # Additional common date + time formats:
        '%m/%d/%Y %H:%M',
        '%m/%d/%Y %H:%M:%S',
        '%d.%m.%Y %H:%M',
        '%d.%m.%Y %H:%M:%S',
        '%d-%m-%Y %H:%M',
        '%d-%m-%Y %H:%M:%S',
        '%Y/%m/%d %H:%M:%S'
    ]

    # Sample data to detect type (exclude N/A values from date detection)
    for item in raw_data[:sample_size]:
        # Skip N/A values for date detection
        if item == "N/A":
            text_count += 1
            continue
            
        is_date = False
        for pattern in date_patterns:
            try:
                datetime.strptime(item, pattern)
                date_count += 1
                is_date = True
                break
            except:
                continue
        if not is_date:
            text_count += 1


    # Decide visualization type and create it
    if date_count > sample_size * 0.6:
        # print(f"Tarih verisi tespit edildi ({date_count}/{sample_size})")
        visualize_date_column(raw_data, lineName, date_patterns)
    else:
        # print(f"Kategorik veri tespit edildi ({text_count}/{sample_size})")
        visualize_categorical_column(raw_data, lineName)

    if window_obj.openRawData.isChecked():
        create_raw_data_table(window_obj, raw_data, lineName, date_count, sample_size, date_patterns)

    return True


def create_raw_data_table(window_obj, raw_data, lineName, date_count, sample_size, date_patterns):
    """Create PyQt6 table for raw data display"""
    
    window_obj.tableColumnCounter = 0
    window_obj.rawDataWidget = QWidget()
    window_obj.rawDataWidget.setWindowTitle(f"{lineName} - Raw Data & Statistics")
    window_obj.rawDataWidget.setWindowIcon(QtGui.QIcon('icon.ico'))
    window_obj.rawDataWidget.resize(500, 500)
    window_obj.rawDataWidget.show()
    
    # Create layout
    layout = QVBoxLayout()
    
    # Add detailed statistics
    if date_count > sample_size * 0.6:
        # Date statistics
        dates = []
        for item in raw_data:
            if item == "N/A":
                continue
            for pattern in date_patterns:
                try:
                    date_obj = datetime.strptime(item, pattern)
                    dates.append(date_obj)
                    break
                except:
                    continue
        
        if dates:
            dates.sort()
            min_date = min(dates)
            max_date = max(dates)
            duration_hours = int((max_date - min_date).total_seconds() / 3600)
            
            stats_text = f"""{lineName} - Date/Time Statistics:
Total Records: {len(dates):,}
Min Date: {min_date.strftime('%Y-%m-%d %H:%M:%S')}
Max Date: {max_date.strftime('%Y-%m-%d %H:%M:%S')}
Duration: {duration_hours:,} hours"""
        else:
            stats_text = f"{lineName} - Date/Time Statistics: No valid dates found"
    else:
        # Categorical statistics
        value_counts = Counter(raw_data)
        total_items = len(raw_data)
        unique_items = len(value_counts)
        
        stats_text = f"""{lineName} - Categorical Statistics:
Total Records: {total_items:,}
Unique Categories: {unique_items:,}"""
    
    # Add info label with statistics
    info_label = QLabel(stats_text)
    info_label.setStyleSheet("""
        QLabel {
            background-color: #E1E1E1;
            color: black;
            border: 1px solid #1E1E1E;
            border-radius: 5px;
            font: bold 11px;
            padding: 10px;
            margin: 5px;
        }
    """)
    layout.addWidget(info_label)
    
    # Create table
    table = QTableWidget()
    table.setColumnCount(2)
    table.setRowCount(len(raw_data))
    table.setHorizontalHeaderLabels(["Row #", lineName])
    
    # Fill table with data
    for i, data_item in enumerate(raw_data):
        table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
        # Ensure data_item is properly converted to string and handle any special characters
        try:
            safe_data = str(data_item) if data_item is not None else "N/A"
            # Remove any potential problematic characters
            safe_data = safe_data.replace('\x00', '').strip()
            table.setItem(i, 1, QTableWidgetItem(safe_data))
        except Exception as e:
            table.setItem(i, 1, QTableWidgetItem("N/A"))
    
    # Style the table
    table.setAlternatingRowColors(True)
    table.setStyleSheet("""
        QTableWidget {
            gridline-color: #1E1E1E;
            background-color: white;
            alternate-background-color: #F0F0F0;
        }
        QHeaderView::section {
            background-color: #E1E1E1;
            color: black;
            border: 1px solid #1E1E1E;
            font: bold 12px;
            padding: 5px;
        }
    """)
    
    # Add export button
    export_button = QPushButton("Export Analysis to File")
    export_button.setStyleSheet("""
        QPushButton {
            background-color: #E1E1E1;
            color: black;
            border: 1px solid #1E1E1E;
            border-radius: 10px;
            font: bold 14px;
            padding: 8px;
            margin: 5px;
        }
        QPushButton:hover {
            background-color: #1E1E1E;
            color: #6ECC78;
        }
    """)
    
    export_button.clicked.connect(lambda: export_data_to_file(window_obj, raw_data, lineName))
    layout.addWidget(export_button)
    
    layout.addWidget(table)
    window_obj.rawDataWidget.setLayout(layout)


def visualize_date_column(raw_data, column_name, date_patterns):
    """Create clean date/time visualization with minute precision"""
    
    # Convert to datetime objects (skip N/A values)
    dates = []
    for item in raw_data:
        if item == "N/A":
            continue
        converted = False
        for pattern in date_patterns:
            try:
                date_obj = datetime.strptime(item, pattern)
                dates.append(date_obj)
                converted = True
                break
            except:
                continue
    
    if len(dates) == 0:
        # print("No dates could be converted")
        return
    
    # Sort dates
    dates.sort()
    
    # Create single beautiful hourly distribution chart
    plt.figure()
    
    decimal_hours = [d.hour + d.minute/60.0 for d in dates]  # Convert to decimal hours
    
    # Create bins for every 15 minutes (0.25 hour intervals)
    bins = np.arange(0, 24.25, 0.25)  # 0, 0.25, 0.5, 0.75, 1.0, etc.
    counts, bin_edges = np.histogram(decimal_hours, bins=bins)
    
    # Create beautiful smooth area chart instead of bars
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Create gradient colors based on activity level
    colors = plt.cm.viridis(counts / max(counts) if max(counts) > 0 else [0] * len(counts))
    
    # Plot smooth area chart
    plt.plot(bin_centers, counts, linewidth=3, color='#2E86C1', alpha=0.9)
    plt.fill_between(bin_centers, counts, alpha=0.4, color='#85C1E9')
    
    # Add subtle bars for better readability
    plt.bar(bin_centers, counts, width=0.15, alpha=0.6, color=colors, edgecolor='white', linewidth=0.5)
    
    plt.title(f'{column_name} - Hourly Distribution', fontweight='bold', fontsize=18, pad=40)
    plt.xlabel('Hour of Day', fontsize=14)
    plt.ylabel('Activity Count', fontsize=14)
    
    # Better x-axis labels showing hours
    plt.xticks(range(0, 25, 2), [f'{h:02d}:00' for h in range(0, 25, 2)], fontsize=12, rotation=45)
    plt.yticks(fontsize=12)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xlim(0, 24)
    
    # Find peak information for bottom display
    if len(counts) > 0 and max(counts) > 0:
        max_val = max(counts)
        max_idx = np.argmax(counts)
        peak_decimal_hour = bin_centers[max_idx]
        peak_hour = int(peak_decimal_hour)
        peak_minute = int((peak_decimal_hour - peak_hour) * 60)
        
        # Mark peak point
        plt.plot(peak_decimal_hour, max_val, 'ro', markersize=12, markerfacecolor='#E74C3C', markeredgecolor='darkred', markeredgewidth=2)
        
        # Add peak info at bottom of chart
        plt.text(0.02, 0.95, f'Peak Activity: {peak_hour:02d}:{peak_minute:02d} ({max_val} records)', 
                transform=plt.gca().transAxes, fontweight='bold', color='#E74C3C', fontsize=6,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='#E74C3C'))
    
    plt.tight_layout(pad=3.0)
    plt.show()


def visualize_categorical_column(raw_data, column_name):
    """Create clean categorical data visualization"""
    
    # Count frequencies (N/A values are now normalized)
    value_counts = Counter(raw_data)
    total_unique = len(value_counts)
    
    # Get top 20 for main chart
    top_items = value_counts.most_common(20)
    categories = [str(item[0])[:25] for item in top_items]
    counts = [item[1] for item in top_items]
    
    # Create single bar chart visualization with better spacing
    plt.figure()
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
    bars = plt.bar(categories, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    
    plt.title(f'{column_name} - Category Distribution (Top 20)', fontweight='bold', fontsize=18, pad=40)
    plt.xlabel('Categories', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, alpha=0.3, axis='y')
    
    # Show max value with better positioning
    if counts:
        max_val = max(counts)
        max_idx = counts.index(max_val)
        
        # Max value annotation
        plt.text(max_idx, max_val + max_val * 0.05, f'Max: {max_val}', 
                ha='center', va='bottom', fontweight='bold', color='red', fontsize=12,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9))
    
    plt.tight_layout(pad=5.0)
    plt.show()


def export_data_to_file(window_obj, raw_data, column_name):
    """Export data to text file with analysis"""
    try:
        if window_obj.selectedPath == '':
            QMessageBox.warning(window_obj, 'Error', 'No file selected')
            return
        
        # Create export file path
        base_path = window_obj.selectedPath.rsplit('/', 1)[0]
        export_file = f"{base_path}/{column_name}_analysis.txt"
        
        # Count frequencies
        value_counts = Counter(raw_data)
        total_items = len(raw_data)
        unique_items = len(value_counts)
        
        # Write to file
        with open(export_file, 'w', encoding='utf-8') as f:
            f.write(f"Data Analysis for: {column_name}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Summary Statistics:\n")
            f.write(f"   Total Records: {total_items:,}\n")
            f.write(f"   Unique Values: {unique_items:,}\n")
            f.write(f"   Average Frequency: {total_items/unique_items:.2f}\n\n")
            
            f.write(f"Top 20 Most Frequent Values:\n")
            f.write("-" * 50 + "\n")
            
            for i, (value, freq) in enumerate(value_counts.most_common(20), 1):
                percentage = (freq / total_items) * 100
                f.write(f"{i:2d}. {value}: {freq:,} times ({percentage:.2f}%)\n")
            
            f.write(f"\nComplete Frequency Distribution:\n")
            f.write("-" * 50 + "\n")
            
            for value, freq in sorted(value_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = (freq / total_items) * 100
                f.write(f"{value}: {freq} ({percentage:.2f}%)\n")
            
            f.write(f"\nRaw Data:\n")
            f.write("-" * 20 + "\n")
            for i, item in enumerate(raw_data, 1):
                f.write(f"{i:4d}: {item}\n")
        
        QMessageBox.information(window_obj, "Export Success", 
                              f"Data analysis exported to:\n{export_file}")
        
    except Exception as e:
        QMessageBox.critical(window_obj, "Export Error", f"Failed to export data:\n{str(e)}")


# Backward compatibility function (without window_obj parameter)
def handle_non_numeric_data_simple(lines, column, lineName, slipLineCharacter):
    """Simple version without PyQt6 integration for backward compatibility"""
    
    class DummyWindow:
        def __init__(self):
            self.openRawData = type('obj', (object,), {'isChecked': lambda: False})()
            self.selectedPath = ''
    
    dummy_window = DummyWindow()
    return handle_non_numeric_data(dummy_window, lines, column, lineName, slipLineCharacter)