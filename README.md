# Automated JAR File Extraction & Software Package Update Analysis
# Note
This repository contains a partial representation of the project, as the complete solution has been integrated into the company’s production environment which is confidential.

**Project Overview**
This project automates the extraction and analysis of JAR files from multiple software versions to streamline software package updates. It provides a reliable method for comparing different product versions, identifying JAR upgrades, and automating silent installations. The project increases analysis efficiency by 40% and is fully integrated into a Jenkins pipeline for continuous delivery.

**Key Features**
Automated JAR File Extraction: Extracts data from 500+ JAR files in multiple folders and subfolders.
Version Comparison: Identifies differences between two software versions, highlighting which JAR files have been updated.
Silent Installation: Automates silent product installations for easier deployment and testing.
Jenkins Integration: Configured within Jenkins, utilizing a cloud-based virtual machine for storage and results generation.
**Project Flow**
Automation.py:
This script extracts JAR files from all folders and subfolders, automating the data extraction process.

DIFFauto.py:
Compares two different versions of the product, both extracted using Automation.py, to identify which JAR files have been upgraded between versions A and B.

silent128.py:
Automates the silent installation of the product. It runs a silent installation command and prepares the product for further use by the Automation.py script.

**Jenkins Configuration:**
The entire project is configured within Jenkins, which uses a cloud-based virtual machine to store extracted data and generate the result. Jenkins outputs a detailed list of upgraded JAR files and license information.

**Technologies Used**
Language: Python
Automation & Comparison: Automation.py, DIFFauto.py
Installation Automation: silent128.py
Continuous Integration: Jenkins
Cloud Storage: Virtual Machine (cloud-based) for data storage and results generation

