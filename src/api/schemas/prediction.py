from pydantic import BaseModel, Field

class DiabetesInput(BaseModel):
    # Standard physiological measurements (Raw Values)
    age: float = Field(..., description="Age in years", example=59.0)
    sex: float = Field(..., description="Sex (1: Male, 2: Female)", example=2.0)
    bmi: float = Field(..., description="Body Mass Index (BMI)", example=32.1)
    bp: float = Field(..., description="Average Blood Pressure (mm Hg)", example=101.0)
    
    # Blood serum measurements (s1 - s6) in mg/dL or standard units
    s1: float = Field(..., description="s1: Total Serum Cholesterol (tc)", example=157.0)
    s2: float = Field(..., description="s2: Low-Density Lipoproteins (LDL)", example=93.2)
    s3: float = Field(..., description="s3: High-Density Lipoproteins (HDL)", example=38.0)
    s4: float = Field(..., description="s4: Total Cholesterol / HDL Ratio (tch)", example=4.0)
    s5: float = Field(..., description="s5: Serum Triglycerides Level (ltg)", example=4.85)
    s6: float = Field(..., description="s6: Blood Sugar Level (Glucose - glu)", example=87.0)