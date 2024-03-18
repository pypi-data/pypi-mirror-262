from setuptools import find_packages, setup                                                                                                                                                                                  
                                                                                                                                                                                                               
setup(                                                                                                                                                                                                        
     name="Gemini-cli_by_Yoru-cyber",                                                                                                                                                                                        
     version="1.0.0",                                                                                                                                                                                          
     description="A small Python package to use Gemini on your terminal.",                                                                                                                                                                    
     author="Carlos",                                                                                                                                                                                       
     author_email="carlosmendez170210@gmail.com",                                                                                                                                                                            
     packages=find_packages(),                                                                                                                                                                                 
     include_package_data=True,                                                                                                                                                                                  
     install_requires=["protobuf", "rich", "google-generativeai", "protobuf"],                                                                                                                                                          
     license="MIT",
     classifiers= [
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     python_requires=">=3.6",                                                                                                                                                                                                                                                                                                                                                                         
 )   