# Question 4: Interactive D3.js Mental Disorders Visualization

## Overview
This interactive dashboard provides a comprehensive analysis of mental disorder prevalence across countries and age groups from 1990-2021, built using D3.js templates and best practices.

## Features

### 🎯 Interactive Dashboard Components

1. **Statistics Overview**
   - Total countries analyzed
   - Number of mental disorders
   - Average prevalence percentage
   - Highest prevalence recorded

2. **Top Countries Chart**
   - Horizontal bar chart showing countries with highest prevalence
   - Filterable by specific mental disorders
   - Adjustable number of countries displayed (5-50)
   - Interactive tooltips with detailed information

3. **Age Group Analysis**
   - Line chart showing prevalence trends across age groups
   - Filterable by mental disorder type
   - Interactive data points with hover effects
   - Age-ordered display (5-14 to 85-89)

4. **Interactive Heatmap**
   - Two modes: Countries vs Disorders or Age Groups vs Disorders
   - Color-coded intensity based on prevalence levels
   - Hover tooltips for detailed values
   - Top 15 countries or all age groups

5. **Distribution Analysis**
   - Histogram showing prevalence distribution
   - Frequency analysis of all data points
   - Interactive bars with range information

## 🎨 Design Features

### Modern UI/UX
- **Gradient backgrounds** with professional color schemes
- **Responsive design** that adapts to different screen sizes
- **Smooth animations** and transitions
- **Interactive tooltips** with rich information
- **Color-coded legends** for easy interpretation

### D3.js Best Practices
- **Modular code structure** with reusable functions
- **Data-driven visualizations** using D3's data binding
- **Scalable vector graphics** (SVG) for crisp rendering
- **Event-driven interactions** for user engagement
- **Responsive scaling** and proper margins

## 📊 Data Sources

The visualization uses two main datasets:
- `Q4_country_data.csv`: Country-level prevalence data
- `Q4_age_data.csv`: Age group prevalence data

Both datasets contain:
- Mental disorder types
- Geographic/age categories
- Average prevalence percentages (1990-2021)

## 🚀 How to Use

### Prerequisites
- Modern web browser with JavaScript enabled
- Local web server (for loading CSV files)

### Running the Visualization

1. **Option 1: Simple HTTP Server**
   ```bash
   cd /Users/qinqin/Desktop/Mental_Disorders/reports
   python -m http.server 8000
   ```
   Then open: `http://localhost:8000/Q4_d3_visualization.html`

2. **Option 2: Live Server (VS Code)**
   - Install "Live Server" extension
   - Right-click on `Q4_d3_visualization.html`
   - Select "Open with Live Server"

3. **Option 3: Direct File Opening**
   - Some browsers may block CSV loading for security
   - Use a local server for best results

### Interactive Controls

1. **Disorder Selection**: Choose specific mental disorders or view all
2. **Country Limit**: Adjust number of countries displayed (5-50)
3. **Heatmap Type**: Switch between country and age group views
4. **Hover Effects**: Mouse over any element for detailed information

## 🔧 Technical Implementation

### D3.js Libraries Used
- **D3 v7**: Core visualization library
- **D3 Scales**: For data mapping and color schemes
- **D3 Axes**: For chart axes and labels
- **D3 Selections**: For DOM manipulation
- **D3 Transitions**: For smooth animations

### Chart Types Implemented
- **Horizontal Bar Charts**: For country rankings
- **Line Charts**: For age group trends
- **Heatmaps**: For multi-dimensional data
- **Histograms**: For distribution analysis

### Color Schemes
- **Category10**: For disorder differentiation
- **Set3**: For country identification
- **Blues**: For heatmap intensity
- **Custom gradients**: For modern aesthetics

## 📈 Key Insights

The visualization reveals several important patterns:

1. **Geographic Variations**: Portugal shows highest anxiety disorder prevalence (5.56%)
2. **Age Patterns**: Mental disorders peak in younger age groups (15-19 years)
3. **Disorder Types**: Anxiety and depressive disorders are most prevalent
4. **Distribution**: Most prevalence values cluster in the 1-4% range

## 🎯 Advantages Over Static Charts

### Interactivity
- **Dynamic filtering** by disorder type
- **Adjustable parameters** for different views
- **Hover tooltips** with contextual information
- **Responsive controls** for user exploration

### Visual Appeal
- **Modern design** with gradients and shadows
- **Smooth animations** for better user experience
- **Professional color schemes** for clarity
- **Responsive layout** for different devices

### Data Exploration
- **Multiple chart types** for different perspectives
- **Integrated statistics** for quick insights
- **Flexible filtering** for focused analysis
- **Comprehensive tooltips** for detailed information

## 🔮 Future Enhancements

Potential improvements could include:
- **Time series animation** showing trends over years
- **Geographic mapping** with country boundaries
- **Advanced filtering** with multiple criteria
- **Export functionality** for charts and data
- **Mobile optimization** for touch interactions

## 📝 Files Created

- `Q4_d3_visualization.html`: Main interactive dashboard
- `Q4_country_data.csv`: Country prevalence data
- `Q4_age_data.csv`: Age group prevalence data
- `Q4_D3_README.md`: This documentation

## 🎉 Conclusion

This D3.js visualization transforms the static Question 4 analysis into an engaging, interactive experience that allows users to explore mental disorder prevalence data from multiple angles. The modern design and smooth interactions make data exploration both informative and enjoyable.
