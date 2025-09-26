# Mental Disorders Analysis - Interactive D3.js Visualizations

This repository contains interactive data visualizations analyzing mental disorder prevalence across countries and age groups from 1990-2021.

## 🎯 **Analysis Overview**

**Question 4: Which countries and age groups have shown the highest average prevalence of mental disorders from 1990 to 2021?**

### **Sub-question 1: Top Countries by Prevalence**
- Interactive bar charts showing countries with highest mental disorder rates
- Filterable by disorder type and country count
- Both horizontal and vertical chart options

### **Sub-question 2: Age Group Analysis**
- Age group prevalence patterns across different mental disorders
- Bar charts and line charts for trend analysis
- Comparison across all disorders

## 📊 **Interactive Visualizations**

### **1. Country Analysis (Sub-question 1)**
🔗 **[Live Demo: Top Countries Bar Chart](Q4_subquestion1_bar_chart.html)**
- Top countries by mental disorder prevalence
- Interactive filtering and chart type selection
- Hover tooltips with detailed statistics

### **2. Age Group Analysis (Sub-question 2)**
🔗 **[Live Demo: Age Groups Chart](Q4_subquestion2_age_chart.html)**
- Mental disorder prevalence by age group
- Bar chart and line chart options
- Age-ordered display (5-14 to 50-54)

### **3. Advanced D3.js Visualizations**
🔗 **[Live Demo: Bubble Chart & Sankey Diagram](Q4_new_visualizations.html)**
- Interactive bubble chart for countries
- Sankey diagram showing age group to disorder flow
- Modern D3.js templates and animations

🔗 **[Live Demo: Network & Chord Diagrams](Q4_network_visualization.html)**
- Interactive network diagram
- Chord diagram for disorder relationships
- Draggable nodes and force simulation

## 🛠 **Technical Details**

### **Technologies Used:**
- **D3.js v7** - Data visualization library
- **HTML5/CSS3** - Modern web standards
- **CSV Data** - Mental disorders dataset (1990-2021)
- **Responsive Design** - Works on all devices

### **Data Sources:**
- `Q4_country_data.csv` - Country-level prevalence data
- `Q4_age_data.csv` - Age group prevalence data
- **204 countries** analyzed
- **10 mental disorders** tracked
- **32-year time period** (1990-2021)

## 🎨 **Key Features**

### **Interactive Elements:**
- **Real-time filtering** by disorder type
- **Dynamic chart switching** (bar/line/horizontal/vertical)
- **Hover tooltips** with detailed information
- **Adjustable parameters** (country count, thresholds)
- **Professional styling** with gradients and animations

### **Visualization Types:**
- **Bar Charts** - Country and age group rankings
- **Line Charts** - Trend analysis across age groups
- **Bubble Charts** - Country prevalence with size encoding
- **Sankey Diagrams** - Flow between age groups and disorders
- **Network Diagrams** - Country-disorder relationships
- **Chord Diagrams** - Disorder interconnections

## 📈 **Key Insights**

### **Geographic Patterns:**
- **Portugal** shows highest anxiety disorder prevalence (5.56%)
- **204 countries** included in analysis
- **Average prevalence** of 1.02% across all countries

### **Age Group Patterns:**
- **Younger age groups** (15-19, 20-24) show higher prevalence
- **Developmental disorders** (ADHD, Autism) peak in childhood
- **Anxiety disorders** remain prominent across all ages

### **Disorder-Specific Trends:**
- **Anxiety disorders** are most widespread globally
- **ADHD** shows clear age-related patterns
- **Bipolar disorder** more common in adult age groups

## 🚀 **How to Run Locally**

1. **Clone the repository:**
   ```bash
   git clone [your-repo-url]
   cd Mental_Disorders
   ```

2. **Start a local server:**
   ```bash
   cd reports
   python3 -m http.server 8001
   ```

3. **Open in browser:**
   ```
   http://localhost:8001/Q4_subquestion1_bar_chart.html
   ```

## 📊 **Data Summary**

- **Total Records:** 2,040
- **Countries Analyzed:** 204
- **Mental Disorders:** 10
- **Average Prevalence:** 1.02%
- **Highest Prevalence:** 7.05%

## 🎯 **Portfolio Value**

This project demonstrates:
- **Advanced D3.js skills** with multiple chart types
- **Interactive data visualization** capabilities
- **Professional web development** practices
- **Data analysis** and insight generation
- **Modern UI/UX design** principles

## 📝 **Files Structure**

```
reports/
├── Q4_subquestion1_bar_chart.html      # Countries analysis
├── Q4_subquestion2_age_chart.html      # Age groups analysis
├── Q4_new_visualizations.html          # Bubble & Sankey charts
├── Q4_network_visualization.html       # Network & chord diagrams
├── Q4_country_data.csv                 # Country prevalence data
├── Q4_age_data.csv                     # Age group prevalence data
├── working_bar_chart.html              # Simplified working version
├── test_simple.html                    # Basic functionality test
└── README.md                           # This file
```

## 🔗 **Live Demo Links**

Once deployed to GitHub Pages, your visualizations will be accessible at:
- `https://yourusername.github.io/Mental_Disorders/Q4_subquestion1_bar_chart.html`
- `https://yourusername.github.io/Mental_Disorders/Q4_subquestion2_age_chart.html`
- `https://yourusername.github.io/Mental_Disorders/Q4_new_visualizations.html`
- `https://yourusername.github.io/Mental_Disorders/Q4_network_visualization.html`

---

**Created with D3.js templates and modern web technologies for professional data visualization.**