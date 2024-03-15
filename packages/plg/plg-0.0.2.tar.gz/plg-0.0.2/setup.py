from setuptools import setup, find_packages       
print('!')
setup(
    name = "plg",      
    version = "0.0.2",  
    keywords = ("pip", "plg","featureextraction"),
    description = "print plg sb",
    long_description = "print plg sb",
    license = "MIT Licence",

    url = "https://github.com/chenlike/plg-test",    
    author = "plg", 
    author_email = "617682513@qq.com",

    
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []       
)
