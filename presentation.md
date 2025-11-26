# Cybersecurity Threat Intelligence Dashboard Presentation

## Part 1: Your Formal Presentation (8 minutes)

### 1. The Hook (1 minute)

- **What problem are you addressing?**
  - We are addressing the challenge of understanding and detecting cybersecurity threats by analyzing two distinct datasets: one focusing on global cybersecurity incidents and the other on network intrusion data.
  - Our central question is: Can we derive actionable intelligence by integrating macro-level threat trends with micro-level network analysis?

- **Why should we care?**
  - As cyberattacks grow in frequency and sophistication, understanding their patterns is critical for any organization's defense.
  - This dashboard provides a visual and interactive tool to identify these patterns, which can lead to better-informed security strategies, more effective resource allocation, and a stronger overall security posture.

- **Who is your audience?**
  - The dashboard is designed for a diverse audience, including:
    - **Decision-Makers:** CISOs and executives who need a high-level overview of the threat landscape.
    - **Security Analysts:** Domain experts who can use the tool for deep-dive analysis and threat hunting.
    - **Data Scientists:** Who can use the insights to build and refine predictive models.

### 2. Data Journey (2 minutes)

- **What are your data sources?**
  - **Global Cybersecurity Threats:** A dataset capturing major reported cybersecurity incidents from 2015 to 2024.
  - **Network Intrusion Data:** A dataset containing records of network traffic, including normal and malicious activity.

- **How did you integrate them?**
  - The datasets are not directly merged but are analyzed in parallel within a unified dashboard.
  - The "Comparative Insights" page provides a conceptual bridge, mapping macro-level attack types (e.g., Ransomware) to micro-level network indicators (e.g., high encryption usage).

- **Key cleaning decisions:**
  - **Data Standardization:** Ensured the 'Year' column in the global threats dataset was consistently numeric.
  - **Duplicate Removal:** Removed duplicate records from the global threats dataset to ensure accurate analysis.
  - **Data Integrity:** Checked for and handled issues like negative values in numeric columns.

- **Missing data approach:**
  - For the global threats dataset, we used **MICE (Multiple Imputation by Chained Equations)** to handle missing financial loss data.
  - This method was chosen because our analysis suggested the data was **Missing Completely At Random (MCAR)**, and MICE is a robust technique for such scenarios. The imputation process and its quality metrics are documented in the "IDA/EDA Analysis" page.

### 3. Live App Demo (4 minutes)

- **Navigate through your app:**
  - Start with the **Dashboard Overview** for a high-level summary.
  - Move to the **Global Threat Landscape** and **Intrusion Detection** pages for detailed analysis of each dataset.
  - Showcase the **IDA/EDA Analysis** page for a deeper dive into the data quality and statistical properties.
  - Conclude with the **Comparative Insights** page, which synthesizes the findings from both datasets.

- **Highlight 2-3 key visualizations:**
  - **Attack Frequency Over Time:** On the "Dashboard Overview," this chart shows the clear upward trend of cyberattacks over the last decade.
  - **Attack Type × Industry Heatmap:** On the "Global Threat Landscape" page, this reveals which industries are most targeted by specific attack types, helping to prioritize sector-specific defenses.
  - **Login Attempts vs Failed Logins:** On the "Intrusion Detection" page, this scatter plot helps identify suspicious login patterns that may indicate a brute-force attack.

- **Demonstrate interactive elements:**
  - Use the sidebar filters to narrow down the data by year, country, and attack type.
  - Demonstrate the interactive features of the charts, such as hovering for details, zooming, and clicking on legend items to filter data.

- **Show the narrative:**
  - The app follows a logical flow from a high-level overview to deep-dive analysis.
  - The "Comparative Insights" page serves as the climax of the story, bringing together the macro and micro perspectives to provide actionable recommendations.

- **Point out documentation:**
  - The **Methodology** page provides a data dictionary and an overview of the analysis methods, ensuring new users can understand the data and the insights presented.

### 4. Reflection (1 minute)

- **What's working well?**
  - The dashboard provides a comprehensive and interactive way to explore two complex datasets.
  - The consistent theme and clear visualizations make the information accessible and easy to digest.
  - The "Comparative Insights" page successfully bridges the gap between strategic threat intelligence and tactical network analysis.

- **What are you still refining?**
  - The performance of the app could be optimized, especially when loading and filtering large datasets.
  - I plan to add more advanced analytics, such as anomaly detection models, to provide more proactive threat intelligence.

- **"Above and Beyond" plans?**
  - Integrate a real-time threat intelligence feed to provide up-to-the-minute insights.
  - Develop and deploy machine learning models for attack prediction and classification based on the patterns identified in this analysis.

## Part 2: Structured Q&A (4-5 minutes)

### 🎭 Role-Based Questions (Preparation)

**Questioner #1: The User Advocate**

- **Potential Confusion:** A user might be confused about the distinction between the two datasets and why they are not merged.
- **Where to get lost:** The "IDA/EDA Analysis" page might be too technical for a general user.
- **Helpful Documentation:** A glossary of cybersecurity terms and a more detailed "How to use this app" guide would be beneficial.

**Questioner #2: The Data Skeptic**

- **Assumptions:** I assumed that the reported financial loss data is accurate and that the network intrusion data is representative of a typical corporate network.
- **Imputation Method:** I chose MICE over simpler methods like mean/median imputation because it provides more realistic and less biased estimates by modeling each variable as a function of the others.
- **Lurking Data Quality Issues:** There might be reporting biases in the global threats dataset, where certain types of attacks or attacks in certain regions are over-represented.

**Questioner #3: The Design Critic**

- **Weakest Visualization:** The "Network Attack Indicators (Micro)" bar chart could be improved by normalizing the values to make them more comparable.
- **Visual Encodings:** The color schemes are chosen to be consistent and accessible, but I could explore using more perceptually uniform color maps for some of the continuous data.
- **New Visualization:** A Sankey diagram showing the flow from attack source to target industry and attack type could be a powerful addition.

**Questioner #4: The Technical Reviewer**

- **Streamlit Trouble:** Managing session state across different pages and filter components was challenging. I solved this by creating a centralized `init_filter_state` function.
- **App Organization:** The app is organized into modules for each page and a separate module for the theme and filter components, which makes the code modular and easy to navigate.
- **Most Ambitious Thing:** The custom-styled components, like the observation boxes and the filter summary chips, required a good amount of HTML and CSS within Streamlit, which was technically challenging but rewarding.
