# Hepatitis-B-Mortality
---

### Abstract:


The goal of this project is to build a classification machine learning model to predict Hepatitis B mortality. 

For this project, a pipeline was built to collect the data and store it in an SQL database then performing machine learning to predict if the patient will die or survive based on the patients's blood work results. A pipeline was built to allow for a user to create an account and store user information in a Sqlite3 database. Once the user is able to create and login, they are able to input the test results allowing them to see patient's survival rate. 



![alt text](homePage.png)


---



### Design:


 A pipeline was built to collect the data and perform machine learning to predict if the transaction was fraud and deployed an app to show the results. 

![alt text](prediction.png)


---



### Data


The data is from Vesta who is an eCommerce payment solution corporation. 
-	Multiple csv files
-	Over 590,000 Transactions & 394 Features
-	The features include data card information, amount, fraud/notFraud, time/date and many more features engineered by Vesta. 

To access and view a detailed description of the dataset, [Vesta Transactions Data](https://www.kaggle.com/c/ieee-fraud-detection)



---


### Machine Learning Algorithms


Machine Learning classification algorithms:
1.	Logistic Regression
2.	DecisionTree






---



### **TOOLS**

The following tools were used in this project:
1.	SQL, Python & Pandas to clean, explore and generate the final modeling data
2.	Matplotlib and Seaborn to generate visualizations
3.	SKLearn to build Machine Learning classification models and measuring metrics
4.	Streamlit to develop the app
5.	Heroku to deploy the app
6.	Docker to create a smooth pipeline


---

### Communication


The findings and slide deck accompanying this project's presentation are accessible in this GitHub repository.



