# Streamlit
import streamlit as st 

# import the Sqlite database
from users_database import *

# Processing packages
import pandas as pd 
import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')

# Additional tools
import lime
import lime.lime_tabular
import os
import joblib 
import hashlib
# passlib,bcrypt



html_page = """
		<div style="background-color:Thistle;padding:20px;border-radius:20px">
		<h1 style="color:white;size ="40";text-align:center;">Hepatitis B Virus Mortality </h1>
		</div>
		"""

html_hpv_info ="""
	<div style="background-color:AliceBlue;overflow-x: auto; padding:20px;border-radius:10px;margin:10px;">
		<h3 style="text-align:justify;color:black;padding:20px">What is Hepatitis B & How is it diagnosised?</h3>
		<p>Hepatitis B Virus is a small (diameter of 42 nm), incompletely double-stranded DNA hepadnavirus. Substantial genetic variations occur within distinct regions, globally facilitating classification of eight distinguishable genotypes (A through H), which have treatment implications.<p>
		<p>The diagnosis of hepatitis B virus infection requires the evaluation of the patient's blood for hepatitis B surface antigen, hepatitis B surface antibody, and hepatitis B core antibody.</p>
	</div>
	"""


used_featureNames = ['age', 'sex', 'steroid', 'antivirals', 'fatigue', 'spiders', 'ascites','varices', 'bilirubin', 'alk_phosphate', 'sgot', 'albumin', 'protime','histology']


# Load all models to be used on app 
def load_model(model_file):
	loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
	return loaded_model


# Generate hashes for password security 
def generate_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()


# Verify creasted password matches entered password
def verify_hashes(password,hashed_text):
	if generate_hashes(password) == hashed_text:
		return hashed_text
	return False


# function to convert user input to bool
yesNo_dict = {"No":1,"Yes":2}
def get_yesNo_val(val):
	yesNo_dict = {"No":1,"Yes":2}
	for key,value in yesNo_dict.items():
		if val == key:
			return value 

# function to get user input keys
def get_key(val,my_dict):
	for key,value in my_dict.items():
		if val == key:
			return key

# function to get user input values
def get_value(val,my_dict):
	for key,value in my_dict.items():
		if val == key:
			return value 

# use to convert user input to bool
gender_dict = {"male":1,"female":2}



def main():


	menu = ["Home","Login","SignUp"]
	submenu = ["Exploratory Data Analysis","Prediction","SignUp"]

	choice = st.sidebar.selectbox("Menu",menu)
	if choice == "Home":
		st.subheader("Home")

		st.markdown(html_page.format('royalblue'),unsafe_allow_html=True)
		# Images
		from PIL import Image
		img = Image.open("HepB-AgeAdjRateDeaths.jpg")
		st.image(img,width=700,caption="https://www.cdc.gov/hepatitis/policy/NPR/2021/NationalProgressReport-HepB-ReduceDeaths.htm/")

		st.markdown(html_hpv_info,unsafe_allow_html=True)


	elif choice == "Login":
		username = st.sidebar.text_input("Username")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			create_usertable()
			hashed_pswd = generate_hashes(password)
			result = login_user(username,verify_hashes(password,hashed_pswd))
			
			if result:
				st.success(" {} has successfully signed in".format(username))
				st.subheader("Please Select An Action")
				activity = st.selectbox(" ",submenu)
				if activity == "Exploratory Data Analysis":
					st.subheader("Exploratory Data Analysis Visualization")
					df = pd.read_csv("data/clean_hepatitis_dataset.csv")
					st.dataframe(df)

					df['class'].value_counts().plot(kind='bar')
					st.pyplot()
					st.set_option('deprecation.showPyplotGlobalUse', False)


					# Freq Dist Plot
					freq_df = pd.read_csv("data/freq_df_hepatitis_dataset.csv")
					st.bar_chart(freq_df['count'])


					if st.checkbox("Area Chart"):
						all_columns = df.columns.to_list()
						feat_choices = st.multiselect("Choose a Feature",all_columns)
						new_df = df[feat_choices]
						st.area_chart(new_df)
						


				elif activity == "Prediction":
					st.subheader("Please Enter Patient Results")

					age = st.number_input("Age (Please enter an age: between 7 & 80",7,80)
					sex = st.radio("Sex",tuple(gender_dict.keys()))
					steroid = st.radio("Does patient take Steroids?",tuple(yesNo_dict.keys()))
					antivirals = st.radio("Does patient take Antivirals?",tuple(yesNo_dict.keys()))
					fatigue = st.radio("Does patient have Fatigue?",tuple(yesNo_dict.keys()))
					spiders = st.radio("Was Spider Naevi present?",tuple(yesNo_dict.keys()))
					ascites = st.selectbox("Was Ascites present?",tuple(yesNo_dict.keys()))
					varices = st.selectbox("Was Varices present?",tuple(yesNo_dict.keys()))
					bilirubin = st.number_input("Please enter the bilirubin level: between 0.0 & 8.0",0.0,8.0)
					alk_phosphate = st.number_input("Please enter the Alkaline Phosphate level: between 0.0 & 296.0",0.0,296.0)
					sgot = st.number_input("Please enter the Sgot level: betwee 0.0 & 648.0",0.0,648.0)
					albumin = st.number_input("Please enter the Albumin level: between 0.0 & 6.4",0.0,6.4)
					protime = st.number_input("Please enter the Prothrombin Time: between 0.0 & 100.0",0.0,100.0)
					histology = st.selectbox("Was there presence of Histology?",tuple(yesNo_dict.keys()))

					feature_list = [age,get_value(sex,gender_dict),get_yesNo_val(steroid),get_yesNo_val(antivirals),get_yesNo_val(fatigue),get_yesNo_val(spiders),get_yesNo_val(ascites),get_yesNo_val(varices),bilirubin,alk_phosphate,sgot,albumin,int(protime),get_yesNo_val(histology)]
					single_sample = np.array(feature_list).reshape(1,-1)

					# Selecting which Algorithm to run
					model_choice = st.selectbox("Please select an algorithm to use",["LogisticRegression","DecisionTree"])
					if st.button("Predict"):
						if model_choice == "DecisionTree":
							loaded_model = load_model("models/decision_tree_clf_hepB_model.pkl")
							prediction = loaded_model.predict(single_sample)
							pred_prob = loaded_model.predict_proba(single_sample)
						elif model_choice == "LogisticRegression":
							loaded_model = load_model("models/logistic_regression_hepB_model.pkl")
							prediction = loaded_model.predict(single_sample)
							pred_prob = loaded_model.predict_proba(single_sample)

						if prediction == 1:
							st.warning("Unfortunately, The Patient is likely to Die!")
							pred_probability_score = {"Die":pred_prob[0][0]*100,"Live":pred_prob[0][1]*100}
							st.subheader("{}'s probablity rate for this patient is:".format(model_choice))
							st.json(pred_probability_score)
							
						else:
							st.success("Great News, The Patient will survive")
							pred_probability_score = {"Die":pred_prob[0][0]*100,"Live":pred_prob[0][1]*100}
							st.subheader("{}'s probablity rate for this patient is:".format(model_choice))
							st.json(pred_probability_score)
							
					if st.button("Patient Result Details"):
						if model_choice == "DecisionTree":
							loaded_model = load_model("models/decision_tree_clf_hepB_model.pkl")
							
						else:
							loaded_model = load_model("models/logistic_regression_hepB_model.pkl")
							

							df = pd.read_csv("data/clean_hepatitis_dataset.csv")
							x = df[['age', 'sex', 'steroid', 'antivirals','fatigue','spiders', 'ascites','varices', 'bilirubin', 'alk_phosphate', 'sgot', 'albumin', 'protime','histology']]
							feature_names = ['age', 'sex', 'steroid', 'antivirals','fatigue','spiders', 'ascites','varices', 'bilirubin', 'alk_phosphate', 'sgot', 'albumin', 'protime','histology']
							class_names = ['Die(1)','Live(2)']
							result_details = lime.lime_tabular.LimeTabularExplainer(x.values,feature_names=feature_names, class_names=class_names,discretize_continuous=True)
							
							# Details of results
							detail_instance = result_details.explain_instance(np.array(feature_list), loaded_model.predict_proba,num_features=13, top_labels=1)
							detail_instance.show_in_notebook(show_table=True, show_all=False)

							st.write(detail_instance.as_list())
							new_exp = detail_instance.as_list()

							label_limits = [i[0] for i in new_exp]
							label_scores = [i[1] for i in new_exp]

							plt.barh(label_limits,label_scores)
							st.pyplot()
							st.set_option('deprecation.showPyplotGlobalUse', False)
							
							plt.figure(figsize=(20,10))
							fig = detail_instance.as_pyplot_figure()
							st.pyplot()
							st.set_option('deprecation.showPyplotGlobalUse', False)



					


			else:
				st.warning("Incorrect Username/Password! Please try again")


	elif choice == "SignUp":
		new_username = st.text_input("User name")
		new_password = st.text_input("Password", type='password')

		confirm_password = st.text_input("Confirm Password",type='password')
		if new_password == confirm_password:
			st.success("Password Confirmed")
		else:
			st.warning("Passwords not the same")

		if st.button("Submit"):
			create_usertable()
			hashed_new_password = generate_hashes(new_password)
			add_userdata(new_username,hashed_new_password)
			st.success("You have successfully created a new account")
			st.info("Login to Get Started")







if __name__ == '__main__':
	main()

