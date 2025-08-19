from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import os # Make sure os is imported

from sklearn.preprocessing import StandardScaler # Likely used in preprocessor, not directly here
from src.pipeline.predict_pipeline import CustomData,PredictPipeline
from src.utils import load_object # Ensure load_object is imported

application=Flask(__name__)

app=application

# Define paths to your saved preprocessor and model
PREPROCESSOR_PATH = os.path.join('artifacts', 'preprocessor.pkl')
MODEL_PATH = os.path.join('artifacts', 'model.pkl')

# Load the preprocessor and model when the app starts
# This avoids reloading them on every request and speeds up predictions
preprocessor = None
model = None
try:
    preprocessor = load_object(PREPROCESSOR_PATH)
    model = load_object(MODEL_PATH)
    print("DEBUG (app.py): Preprocessor and model loaded successfully at app startup.")
except Exception as e:
    print(f"ERROR (app.py): Failed to load preprocessor or model at startup: {e}")
    # You might want to handle this more gracefully in a production app,
    # e.g., show a maintenance page or log a critical error.

## Route for a home page
@app.route('/')
def index():
    # Render the home page initially without any prediction results
    return render_template('home.html') # Assuming home.html is your main form page

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        # If someone directly navigates to /predictdata, just show the form
        return render_template('home.html')
    else:
        try:
            # Check if preprocessor and model were loaded successfully at startup
            if preprocessor is None or model is None:
                return render_template('home.html', results="Error: Prediction service not ready. Model or preprocessor failed to load.")

            # Collect data from the form
            data=CustomData(
                gender=request.form.get('gender'),
                # FIX 1: Corrected form field name from 'ethnicity' to 'race_ethnicity'
                race_ethnicity=request.form.get('race_ethnicity'), 
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                # FIX 2: Corrected swapped reading_score and writing_score
                reading_score=float(request.form.get('reading_score')), 
                writing_score=float(request.form.get('writing_score'))
            )
            
            pred_df=data.get_data_as_data_frame()
            print("DEBUG (app.py): DataFrame from form data:")
            print(pred_df)
            print("DEBUG (app.py): DataFrame columns:", pred_df.columns.tolist())
            print("DEBUG (app.py): DataFrame dtypes:", pred_df.dtypes)
            print("Before Prediction")

            # The PredictPipeline now uses the already loaded preprocessor and model
            # No need to re-load them inside PredictPipeline if they are loaded globally
            # However, your PredictPipeline class reloads them, so let's stick to that for now
            # but it's less efficient.
            predict_pipeline=PredictPipeline() 
            print("Mid Prediction")
            
            results=predict_pipeline.predict(pred_df)
            print("After Prediction")
            print(f"DEBUG (app.py): Raw prediction results: {results}")

            # Ensure results is not empty and is a number
            if isinstance(results, np.ndarray) and results.size > 0:
                final_result = round(float(results[0]), 2)
            else:
                final_result = "N/A (Prediction failed or returned unexpected format)"
            
            return render_template('home.html',results=final_result)
        
        except Exception as e:
            print(f"ERROR (app.py): An error occurred during prediction: {e}")
            # This will display the error message on the home page
            return render_template('home.html', results=f"Prediction Error: {e}")
    
if __name__ == '__main__':
    app.run(host="0.0.0.0") # Ensure debug is set to True