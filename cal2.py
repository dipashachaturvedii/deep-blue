import gradio as gr
import requests

# Define the interface
def auto_claim_insurance(vin_number, car_model, car_year, claim_amount):
    # Call the NHTSA API to get the car's make and model based on its VIN number
    response = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/{vin_number}?format=json")
    if response.status_code != 200:
        return "Error: Invalid VIN number"
    make = response.json()["Results"][0]["Make"]
    model = response.json()["Results"][0]["Model"]
    
    # Perform some calculations to determine the insurance claim amount
    base_claim = 0.01 * claim_amount * car_year
    model_factor = 1.0 if car_model.lower() == model.lower() else 0.8
    claim_factor = 1.0 if base_claim <= 5000 else 0.5
    total_claim = base_claim * model_factor * claim_factor
    
    # Return the result
    return f"Based on your {car_year} {make} {model}, your insurance claim amount is ${total_claim:,.2f}"

interface = gr.Interface(fn=auto_claim_insurance, 
                          inputs=["text", "text", "number", "number"], 
                          outputs="text", 
                          title="Auto Claim Insurance Calculator",
                          description="Calculate your insurance claim amount based on your car's VIN number, model, year, and the amount of the claim.")

# Run the interface
interface.launch()
